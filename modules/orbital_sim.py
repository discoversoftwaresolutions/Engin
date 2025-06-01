import numpy as np

def compute_orbit(semi_major_axis_km: float, eccentricity: float, num_points: int = 360):
    mu = 398600.4418  # Earth's gravitational parameter, km^3/s^2
    a = semi_major_axis_km
    e = eccentricity

    theta = np.linspace(0, 2 * np.pi, num_points)
    r = a * (1 - e**2) / (1 + e * np.cos(theta))

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    return x, y, {
        "semi_major_axis_km": a,
        "eccentricity": e,
        "apoapsis_km": a * (1 + e),
        "periapsis_km": a * (1 - e)
    }
