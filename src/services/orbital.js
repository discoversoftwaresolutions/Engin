import numpy as np
from typing import Tuple

# Gravitational constant for Earth (mu) in km^3/s^2
MU_EARTH = 398600.4418

def compute_orbit(semi_major_axis_km: float, eccentricity: float, inclination_deg: float = 0.0, num_points: int = 360) -> Tuple[np.ndarray, np.ndarray, dict]:
    """
    Compute 2D orbital coordinates (Keplerian ellipse) with optional inclination.
    """
    a = semi_major_axis_km
    e = eccentricity
    i = np.radians(inclination_deg)

    theta = np.linspace(0, 2 * np.pi, num_points)
    r = a * (1 - e**2) / (1 + e * np.cos(theta))

    # Orbital plane coordinates
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Rotate by inclination (simple 2D projection, not full 3D)
    x_inclined = x
    y_inclined = y * np.cos(i)

    return x_inclined, y_inclined, {
        "semi_major_axis_km": a,
        "eccentricity": e,
        "inclination_deg": inclination_deg,
        "apoapsis_km": a * (1 + e),
        "periapsis_km": a * (1 - e),
        "orbital_period_min": 2 * np.pi * np.sqrt(a**3 / MU_EARTH) / 60  # in minutes
    }

def compute_hohmann_transfer(r1_km: float, r2_km: float) -> dict:
    """
    Computes delta-v and time of flight for Hohmann transfer between circular orbits.
    """
    v1 = np.sqrt(MU_EARTH / r1_km)
    v_transfer1 = np.sqrt(2 * MU_EARTH * r2_km / (r1_km * (r1_km + r2_km)))
    dv1 = v_transfer1 - v1

    v2 = np.sqrt(MU_EARTH / r2_km)
    v_transfer2 = np.sqrt(2 * MU_EARTH * r1_km / (r2_km * (r1_km + r2_km)))
    dv2 = v2 - v_transfer2

    a_transfer = 0.5 * (r1_km + r2_km)
    tof_sec = np.pi * np.sqrt(a_transfer**3 / MU_EARTH)

    return {
        "delta_v1_km_s": dv1,
        "delta_v2_km_s": dv2,
        "total_delta_v_km_s": abs(dv1) + abs(dv2),
        "time_of_flight_min": tof_sec / 60
    }
