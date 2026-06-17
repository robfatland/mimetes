"""
get_velocity.py — Retrieve ITS_LIVE surface velocities for Bagley Ice Valley
profile points directly from the Zarr data cubes.

Uses the ITS_LIVE datacube catalog to find the correct cube, opens it
via xarray, and extracts velocity time series at each profile point.

Usage:
    python get_velocity.py

Prerequisites:
    pip install xarray zarr s3fs pyproj pandas numpy matplotlib requests

Output:
    bagley_profile_with_velocity.csv
    images/bagley_velocity_profile.png
    images/bagley_velocity_timeseries.png
"""

import json
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import requests
from pyproj import Transformer
from pathlib import Path

CSV_PATH = Path(__file__).parent / "bagley_profile.csv"
OUTPUT_CSV = Path(__file__).parent / "bagley_profile_with_velocity.csv"
OUTPUT_DIR = Path(__file__).parent / "images"

# ITS_LIVE datacube catalog — GeoJSON index of all cubes worldwide
CATALOG_URL = "https://its-live-data.s3.amazonaws.com/datacubes/catalog_v02.json"


def find_cube_url(lat: float, lon: float) -> str:
    """Find the Zarr datacube URL covering a given lat/lon from the catalog."""
    print(f"Downloading datacube catalog...")
    resp = requests.get(CATALOG_URL)
    resp.raise_for_status()
    catalog = resp.json()

    from shapely.geometry import Point, shape

    point = Point(lon, lat)

    for feature in catalog["features"]:
        polygon = shape(feature["geometry"])
        if polygon.contains(point):
            zarr_url = feature["properties"]["zarr_url"]
            print(f"Found cube: {zarr_url}")
            return zarr_url

    raise RuntimeError(f"No datacube found covering ({lat}, {lon})")


def extract_velocities(zarr_url: str, lats: np.ndarray, lons: np.ndarray):
    """
    Open the Zarr datacube and extract velocity at each point.
    Returns mean speed per point and full time series at sample points.
    """
    print(f"Opening datacube: {zarr_url}")
    print("(First access may be slow — reading metadata from S3...)")

    # ITS_LIVE cubes are stored on S3, accessible via HTTP
    # Replace s3:// with http:// path if needed
    if zarr_url.startswith("s3://"):
        http_url = zarr_url.replace("s3://", "https://s3.amazonaws.com/")
    else:
        http_url = zarr_url

    import s3fs
    if zarr_url.startswith("s3://"):
        s3 = s3fs.S3FileSystem(anon=True)
        store = s3fs.S3Map(root=zarr_url, s3=s3)
        ds = xr.open_dataset(store, engine="zarr", consolidated=True)
    else:
        ds = xr.open_dataset(zarr_url, engine="zarr", consolidated=True)

    print(f"Dimensions: {dict(ds.dims)}")
    print(f"Variables: {list(ds.data_vars)[:15]}...")

    # Get the cube's projection from the 'mapping' or 'spatial_ref' variable
    if "mapping" in ds:
        epsg = ds["mapping"].attrs.get("spatial_epsg", None)
    elif "spatial_ref" in ds:
        epsg = ds["spatial_ref"].attrs.get("spatial_epsg", None)
    else:
        epsg = None

    if epsg is None:
        # Try to extract from crs_wkt
        for var in ["mapping", "spatial_ref"]:
            if var in ds:
                wkt = ds[var].attrs.get("crs_wkt", "")
                if "32607" in wkt:
                    epsg = 32607
                elif "32606" in wkt:
                    epsg = 32606
                break
        if epsg is None:
            epsg = 32607  # UTM 7N — common for south-central Alaska
            print(f"WARNING: Could not determine EPSG, defaulting to {epsg}")

    print(f"Cube projection: EPSG:{epsg}")

    # Transform lat/lon to the cube's projected coordinates
    transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True)
    xs, ys = transformer.transform(lons, lats)

    print(f"Projected X range: {xs.min():.0f} – {xs.max():.0f}")
    print(f"Projected Y range: {ys.min():.0f} – {ys.max():.0f}")
    print(f"Cube X range: {float(ds.x.min()):.0f} – {float(ds.x.max()):.0f}")
    print(f"Cube Y range: {float(ds.y.min()):.0f} – {float(ds.y.max()):.0f}")

    # Verify our points are within the cube's extent
    x_in = (xs >= float(ds.x.min())) & (xs <= float(ds.x.max()))
    y_in = (ys >= float(ds.y.min())) & (ys <= float(ds.y.max()))
    print(f"Points within cube extent: {np.sum(x_in & y_in)}/{len(xs)}")

    # Extract velocity at each point — use sel with method="nearest"
    # 'v' is the velocity magnitude variable in ITS_LIVE cubes
    vel_var = "v" if "v" in ds.data_vars else None
    if vel_var is None:
        for candidate in ["v_avg", "speed", "velocity"]:
            if candidate in ds.data_vars:
                vel_var = candidate
                break
    if vel_var is None:
        raise RuntimeError(f"No velocity variable found. Available: {list(ds.data_vars)}")

    print(f"Velocity variable: '{vel_var}'")
    print(f"Extracting velocities at {len(xs)} points...")

    mean_speeds = []
    time_series_list = []

    for i, (x, y) in enumerate(zip(xs, ys)):
        try:
            # Select the nearest grid cell for this point
            point_data = ds[vel_var].sel(x=x, y=y, method="nearest")

            # This gives us the full time series at this point
            values = point_data.values.astype(float)
            valid = values[~np.isnan(values)]

            if len(valid) > 0:
                mean_speeds.append(np.nanmedian(valid))
            else:
                mean_speeds.append(np.nan)

            # Store time series for plotting
            if "mid_date" in point_data.dims:
                time_series_list.append(point_data)
            else:
                time_series_list.append(None)

        except Exception as e:
            mean_speeds.append(np.nan)
            time_series_list.append(None)
            if i == 0:
                print(f"  Error at point 0: {e}")

    ds.close()
    return np.array(mean_speeds), time_series_list


def plot_velocity_profile(df: pd.DataFrame, output_path: Path):
    """Plot median velocity along the profile track."""
    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(df["along_track_km"], df["median_velocity_m_yr"],
            color="darkred", linewidth=1.5, marker=".", markersize=4)
    ax.set_xlabel("Distance along track (km)")
    ax.set_ylabel("Median surface speed (m/yr)")
    ax.set_title("Bagley Ice Valley — Surface Flow Speed Along Profile\n"
                 "(ITS_LIVE, median of all observations 1985–present)")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, df["along_track_km"].max())

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Velocity profile plot saved to: {output_path}")
    plt.close()


def plot_combined_profile(df: pd.DataFrame, output_path: Path):
    """Combined chart: ice thickness cross-section + velocity on secondary axis,
    with a smaller panel below showing theoretical deformation velocity."""

    # Check if deformation velocity has been computed
    has_deformation = "deformation_velocity_m_yr" in df.columns

    if has_deformation:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7),
                                        height_ratios=[5, 2],
                                        sharex=True)
    else:
        fig, ax1 = plt.subplots(figsize=(12, 5))

    dist = df["along_track_km"]
    surface = df["surface_elevation_m"]
    bed = df["bed_elevation_m"]
    velocity = df["median_velocity_m_yr"]

    # Top panel: ice cross-section + observed velocity
    ax1.fill_between(dist, bed, surface, alpha=0.25, color="deepskyblue", label="Ice")
    ax1.plot(dist, surface, color="blue", linewidth=1.0, label="Surface")
    ax1.plot(dist, bed, color="brown", linewidth=1.0, label="Bed")
    ax1.axhline(0, color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
    ax1.set_ylabel("Elevation (m)", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.set_xlim(0, dist.max())
    ax1.grid(True, alpha=0.2)

    ax1_twin = ax1.twinx()
    ax1_twin.plot(dist, velocity, color="darkred", linewidth=1.8, label="Observed speed (ITS_LIVE)")
    ax1_twin.set_ylabel("Surface speed (m/yr)", color="darkred")
    ax1_twin.tick_params(axis="y", labelcolor="darkred")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    ax1.set_title("Bagley Ice Valley — Ice Thickness Profile + Surface Flow Speed\n"
                  "(OIB-AK radar + ITS_LIVE)")

    # Bottom panel: theoretical deformation velocity
    if has_deformation:
        deform = df["deformation_velocity_m_yr"]
        ax2.plot(dist, deform, color="green", linewidth=1.5,
                 label="Deformation only (Glen's law, no basal sliding)")
        ax2.set_xlabel("Distance along track (km)")
        ax2.set_ylabel("Speed (m/yr)")
        ax2.legend(loc="upper left", fontsize=9)
        ax2.grid(True, alpha=0.2)
        ax2.set_xlim(0, dist.max())
        ax2.set_ylim(bottom=0)
    else:
        ax1.set_xlabel("Distance along track (km)")

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Combined profile plot saved to: {output_path}")
    plt.close()


def plot_time_series(time_series_list, df: pd.DataFrame, output_path: Path):
    """Plot velocity time series at sample points."""
    n = len(time_series_list)
    indices = [n // 6, n // 2, 5 * n // 6]

    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    for ax, idx in zip(axes, indices):
        ts = time_series_list[idx]
        if ts is not None and "mid_date" in ts.dims:
            times = pd.to_datetime(ts["mid_date"].values)
            speeds = ts.values.astype(float)
            mask = ~np.isnan(speeds)

            ax.scatter(times[mask], speeds[mask], s=2, alpha=0.4, color="steelblue")
            ax.set_ylabel("Speed (m/yr)")
            km = df.iloc[idx]["along_track_km"]
            ax.set_title(f"km {km:.1f} along track", fontsize=10)
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, "No data", transform=ax.transAxes, ha="center")

    axes[-1].set_xlabel("Date")
    fig.suptitle("Bagley Ice Valley — Velocity Time Series (ITS_LIVE)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Time series plot saved to: {output_path}")
    plt.close()


if __name__ == "__main__":
    # Load profile
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} points from {CSV_PATH.name}\n")

    lats = df["latitude"].values
    lons = df["longitude"].values

    # Find the datacube covering the profile midpoint
    mid_lat = lats[len(lats) // 2]
    mid_lon = lons[len(lons) // 2]
    print(f"Profile midpoint: ({mid_lat:.4f}, {mid_lon:.4f})")

    try:
        from shapely.geometry import Point, shape
    except ImportError:
        print("Need shapely: pip install shapely")
        raise SystemExit(1)

    zarr_url = find_cube_url(mid_lat, mid_lon)

    # Extract velocities
    mean_speeds, time_series_list = extract_velocities(zarr_url, lats, lons)

    valid = np.sum(~np.isnan(mean_speeds))
    print(f"\nValid velocity points: {valid}/{len(mean_speeds)}")
    if valid > 0:
        print(f"Speed range: {np.nanmin(mean_speeds):.1f} – {np.nanmax(mean_speeds):.1f} m/yr")

    # Save
    df["median_velocity_m_yr"] = mean_speeds
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved to: {OUTPUT_CSV.name}")

    # Plots
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plot_velocity_profile(df, OUTPUT_DIR / "bagley_velocity_profile.png")
    plot_combined_profile(df, OUTPUT_DIR / "bagley_combined_profile.png")
    plot_time_series(time_series_list, df, OUTPUT_DIR / "bagley_velocity_timeseries.png")
