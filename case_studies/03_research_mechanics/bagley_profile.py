"""
bagley_profile.py — Extract and plot a longitudinal ice thickness profile
along the Bagley Ice Valley from the KML data.

This demonstrates producing a scientific artifact directly from the
repository data — a key point in the presentation narrative.

Usage:
    python bagley_profile.py

Output:
    images/bagley_profile.png
"""

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

KML_PATH = Path(__file__).parent / "IRUAFHF2_IRARES2_250m_mean.kml"
OUTPUT_DIR = Path(__file__).parent / "images"

# Bagley Ice Valley approximate bounding box
# The Bagley is roughly east-west, centered around lat 60.4, lon -141.5 to -143
LAT_MIN = 60.2
LAT_MAX = 60.7
LON_MIN = -143.5
LON_MAX = -141.0


def haversine_km(lat1, lon1, lat2, lon2):
    """Distance in km between two lat/lon points."""
    R = 6371.0
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = (np.sin(dlat / 2) ** 2 +
         np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) *
         np.sin(dlon / 2) ** 2)
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))


def parse_kml(kml_path: Path) -> list:
    """Parse KML and extract all placemarks with coordinates and data."""
    tree = ET.parse(kml_path)
    root = tree.getroot()

    # Handle KML namespace
    ns = {"kml": "http://www.opengis.net/kml/2.2"}

    points = []
    for pm in root.iter("{http://www.opengis.net/kml/2.2}Placemark"):
        desc_el = pm.find("kml:description", ns)
        coord_el = pm.find(".//kml:coordinates", ns)

        if desc_el is None or coord_el is None:
            continue

        desc = desc_el.text or ""
        coords = coord_el.text.strip()

        # Parse coordinates: lon,lat,alt
        parts = coords.split(",")
        if len(parts) < 2:
            continue
        lon, lat = float(parts[0]), float(parts[1])

        # Parse description fields
        surface_elev = None
        bed_elev = None
        thickness = None
        for line in desc.split("\n"):
            line = line.strip()
            if line.startswith("Surface Elevation:"):
                surface_elev = float(line.split(":")[1].replace("m", "").strip())
            elif line.startswith("Bed Elevation:"):
                bed_elev = float(line.split(":")[1].replace("m", "").strip())
            elif line.startswith("Ice Thickness:"):
                thickness = float(line.split(":")[1].replace("m", "").strip())

        if all(v is not None for v in [surface_elev, bed_elev, thickness]):
            points.append({
                "lat": lat, "lon": lon,
                "surface": surface_elev,
                "bed": bed_elev,
                "thickness": thickness,
            })

    return points


def filter_bagley(points: list) -> list:
    """Filter points to the Bagley Ice Valley bounding box."""
    return [p for p in points
            if LAT_MIN <= p["lat"] <= LAT_MAX
            and LON_MIN <= p["lon"] <= LON_MAX]


def extract_single_flight_line(points: list) -> list:
    """
    The KML contains multiple intersecting flight lines.
    Sorting by longitude alone interleaves them (comb function).

    Strategy: Group points by source file (flight), pick the longest
    east-west flight line that spans the Bagley.
    """
    from collections import defaultdict

    # Group by flight file if available in description, otherwise by proximity
    # Since we parsed coordinates but not the file name, let's extract it
    # We need to re-parse with file names — but for now, use a spatial approach:
    # Pick points within a narrow latitude band to isolate one flight line.

    # The Bagley centerline is roughly at lat ~60.4
    # Narrow the latitude window to catch a single pass
    CENTER_LAT = 60.42
    LAT_TOLERANCE = 0.05  # ~5.5 km north-south window

    narrow = [p for p in points
              if abs(p["lat"] - CENTER_LAT) < LAT_TOLERANCE]

    if len(narrow) < 20:
        # Try wider
        LAT_TOLERANCE = 0.1
        narrow = [p for p in points
                  if abs(p["lat"] - CENTER_LAT) < LAT_TOLERANCE]

    # Sort by longitude (west to east)
    narrow.sort(key=lambda p: p["lon"])

    # Remove large gaps (>2 km between consecutive points = different flight)
    # Keep the longest continuous segment
    segments = []
    current = [narrow[0]]

    for i in range(1, len(narrow)):
        dist = haversine_km(narrow[i-1]["lat"], narrow[i-1]["lon"],
                            narrow[i]["lat"], narrow[i]["lon"])
        if dist < 2.0:  # less than 2 km gap = same segment
            current.append(narrow[i])
        else:
            segments.append(current)
            current = [narrow[i]]
    segments.append(current)

    # Pick the longest segment
    longest = max(segments, key=len)
    return longest


def compute_along_track_distance(points: list) -> np.ndarray:
    """Compute cumulative distance along track from westernmost point."""
    distances = [0.0]
    for i in range(1, len(points)):
        d = haversine_km(points[i-1]["lat"], points[i-1]["lon"],
                         points[i]["lat"], points[i]["lon"])
        distances.append(distances[-1] + d)

    return np.array(distances)


def plot_profile(points: list, distances: np.ndarray, output_path: Path):
    """Plot surface and bed elevation as a cross-section."""
    surface = np.array([p["surface"] for p in points])
    bed = np.array([p["bed"] for p in points])

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.fill_between(distances, bed, surface, alpha=0.3, color="deepskyblue",
                    label="Ice")
    ax.plot(distances, surface, color="blue", linewidth=1.2,
            label="Surface elevation")
    ax.plot(distances, bed, color="brown", linewidth=1.2,
            label="Bed elevation")
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.5, label="Sea level")

    ax.set_xlabel("Distance along track (km)")
    ax.set_ylabel("Elevation (m)")
    ax.set_title("Bagley Ice Valley — Longitudinal Profile\n"
                 "(from OIB-AK_radar KML, 250m downsampled)")
    ax.legend(loc="upper right")
    ax.set_xlim(0, distances[-1])
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Profile saved to: {output_path}")
    plt.close()


if __name__ == "__main__":
    print("Parsing KML...")
    all_points = parse_kml(KML_PATH)
    print(f"Total data points: {len(all_points):,}")

    bagley = filter_bagley(all_points)
    print(f"Points in Bagley region: {len(bagley):,}")

    if len(bagley) < 10:
        print("WARNING: Very few points found. Adjust bounding box.")
        print(f"  Lat range: {LAT_MIN}–{LAT_MAX}")
        print(f"  Lon range: {LON_MIN}–{LON_MAX}")
        raise SystemExit(1)

    # Extract a single continuous flight line
    profile = extract_single_flight_line(bagley)
    print(f"Longest continuous segment: {len(profile)} points")

    distances = compute_along_track_distance(profile)
    print(f"Profile length: {distances[-1]:.1f} km")

    output = OUTPUT_DIR / "bagley_profile.png"
    plot_profile(profile, distances, output)

    # Export CSV for downstream use (e.g. framing research questions for Asta)
    import csv
    csv_path = Path(__file__).parent / "bagley_profile.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["along_track_km", "latitude", "longitude",
                         "surface_elevation_m", "bed_elevation_m", "ice_thickness_m"])
        for pt, d in zip(profile, distances):
            writer.writerow([f"{d:.3f}", f"{pt['lat']:.6f}", f"{pt['lon']:.6f}",
                             f"{pt['surface']:.2f}", f"{pt['bed']:.2f}",
                             f"{pt['thickness']:.2f}"])
    print(f"CSV saved to: {csv_path.name} ({len(profile)} rows)")
