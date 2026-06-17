"""
deformation_velocity.py — Calculate surface speed from ice deformation alone
(no basal sliding) using Glen's flow law, and compare with ITS_LIVE observations.

Physics:
    For a parallel-sided slab of ice on a slope, with no basal sliding,
    the surface velocity due to internal deformation is:

        u_s = (2A / (n+1)) * tau_b^n * H

    where:
        tau_b = rho * g * H * sin(alpha)   (basal shear stress)
        H = ice thickness (m)
        alpha = surface slope
        rho = ice density (917 kg/m^3 for temperate ice)
        g = 9.81 m/s^2
        A = Glen's flow law rate factor (creep parameter)
        n = Glen's flow law exponent (= 3)

    For temperate ice at 0°C: A ≈ 2.4e-24 Pa^-3 s^-1
    (Cuffey & Paterson, 2010, Table 3.4)

    For a valley glacier (not an infinite slab), a shape factor f accounts
    for drag from valley walls:

        tau_b = f * rho * g * H * sin(alpha)

    For a parabolic cross-section with half-width W and depth H:
        f ≈ 1 / (1 + (H / W))     (Nye, 1965 approximation)

    With W = 2000 m (half of 4 km valley width).

Usage:
    python deformation_velocity.py

Output:
    images/bagley_deformation_vs_observed.png
    Prints comparison statistics
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CSV_PATH = Path(__file__).parent / "bagley_profile_with_velocity.csv"
OUTPUT_DIR = Path(__file__).parent / "images"

# Physical constants
RHO = 917.0        # ice density, kg/m^3
G = 9.81           # gravitational acceleration, m/s^2
N = 3              # Glen's flow law exponent
A = 2.4e-24        # rate factor for temperate ice (0°C), Pa^-3 s^-1
SECONDS_PER_YEAR = 365.25 * 24 * 3600

# Valley geometry
VALLEY_WIDTH = 4000.0   # full width, m
W = VALLEY_WIDTH / 2    # half-width for shape factor


def compute_surface_slope(distance_km, surface_elevation_m):
    """Compute local surface slope (radians) from the elevation profile."""
    dist_m = distance_km * 1000.0

    # Central difference for interior points, forward/backward at edges
    slope = np.gradient(surface_elevation_m, dist_m)

    # Slope is dz/dx (negative = downhill in direction of travel)
    # We want the magnitude of the slope angle
    alpha = np.arctan(np.abs(slope))

    return alpha


def shape_factor(H, half_width):
    """
    Nye shape factor for a valley glacier.
    Approximation: f = 1 / (1 + H/W)
    """
    return 1.0 / (1.0 + H / half_width)


def deformation_velocity(H, alpha, A=A, n=N, rho=RHO, g=G, half_width=W):
    """
    Surface velocity from internal deformation only (no basal sliding).

    u_s = (2A / (n+1)) * (f * rho * g * sin(alpha))^n * H^(n+1)

    Returns velocity in m/s.
    """
    f = shape_factor(H, half_width)
    tau_d = f * rho * g * H * np.sin(alpha)

    # Avoid issues where slope or thickness is zero/negative
    tau_d = np.maximum(tau_d, 0.0)

    u_s = (2.0 * A / (n + 1)) * (tau_d ** n) * H

    return u_s


if __name__ == "__main__":
    # Load profile data
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} points from {CSV_PATH.name}")

    dist_km = df["along_track_km"].values
    surface = df["surface_elevation_m"].values
    thickness = df["ice_thickness_m"].values

    # Check if observed velocity column exists
    if "median_velocity_m_yr" in df.columns:
        observed = df["median_velocity_m_yr"].values
        has_observed = True
    elif "velocity_m_yr" in df.columns:
        observed = df["velocity_m_yr"].values
        has_observed = True
    else:
        observed = None
        has_observed = False
        print("WARNING: No observed velocity column found. Plotting deformation only.")

    # Compute surface slope — use a single constant slope for the entire profile
    # (average gradient from start to end) to isolate the effect of thickness variations
    total_drop = surface[0] - surface[-1]  # elevation change start to end
    total_dist = (dist_km[-1] - dist_km[0]) * 1000.0  # in meters
    mean_slope = np.arctan(abs(total_drop) / total_dist)
    alpha = np.full_like(thickness, mean_slope)

    print(f"Using constant surface slope: {np.degrees(mean_slope):.3f}° "
          f"(drop of {total_drop:.0f} m over {total_dist/1000:.1f} km)")

    # Compute deformation velocity
    u_deform_m_s = deformation_velocity(thickness, alpha)
    u_deform_m_yr = u_deform_m_s * SECONDS_PER_YEAR

    print(f"Deformation velocity range: {u_deform_m_yr.min():.1f} – {u_deform_m_yr.max():.1f} m/yr")
    print(f"Deformation velocity mean:  {u_deform_m_yr.mean():.1f} m/yr")

    if has_observed:
        valid = ~np.isnan(observed)
        if np.any(valid):
            print(f"\nObserved velocity range:     {np.nanmin(observed):.1f} – {np.nanmax(observed):.1f} m/yr")
            print(f"Observed velocity mean:      {np.nanmean(observed):.1f} m/yr")

            ratio = observed[valid] / np.maximum(u_deform_m_yr[valid], 0.01)
            print(f"\nObserved / Deformation ratio: {np.nanmean(ratio):.2f} (mean)")
            print("  > 1 implies basal sliding contributes to the motion")
            print("  = 1 would mean all motion is from deformation")

    # Save deformation velocity to CSV
    df["deformation_velocity_m_yr"] = u_deform_m_yr
    df.to_csv(CSV_PATH, index=False)  # overwrite with new column
    print(f"\nUpdated {CSV_PATH.name} with deformation_velocity_m_yr column")

    # Plot
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(dist_km, u_deform_m_yr, color="green", linewidth=2,
            label="Deformation only (Glen's law, no basal sliding)")

    if has_observed:
        ax.plot(dist_km, observed, color="darkred", linewidth=2,
                label="Observed (ITS_LIVE median)")

    ax.set_xlabel("Distance along track (km)")
    ax.set_ylabel("Surface speed (m/yr)")
    ax.set_title("Bagley Ice Valley — Deformation Velocity vs. Observed\n"
                 f"(Glen's law: A={A:.1e} Pa⁻³s⁻¹, n={N}, "
                 f"temperate ice, constant slope, valley width={VALLEY_WIDTH/1000:.0f} km)")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, dist_km.max())
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "bagley_deformation_vs_observed.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Plot saved to: {out_path}")
    plt.close()
