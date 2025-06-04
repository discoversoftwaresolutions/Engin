import numpy as np
import plotly.graph_objects as go
from modules.orbital_sim import compute_orbit
from skyfield.api import load, EarthSatellite

def plot_orbit_3d(semi_major_axis_km, eccentricity, inclination_deg):
    x, y, meta = compute_orbit(semi_major_axis_km, eccentricity, inclination_deg)
    z = np.zeros_like(x)
    i_rad = np.radians(inclination_deg)
    z = y * np.sin(i_rad)
    y = y * np.cos(i_rad)

    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:25j]
    xe = 6371 * np.cos(u) * np.sin(v)
    ye = 6371 * np.sin(u) * np.sin(v)
    ze = 6371 * np.cos(v)

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name='Orbit Path', line=dict(color='lime')))
    fig.add_trace(go.Surface(x=xe, y=ye, z=ze, colorscale='Blues', opacity=0.6, showscale=False, name='Earth'))

    fig.update_layout(
        scene=dict(xaxis_title='X (km)', yaxis_title='Y (km)', zaxis_title='Z (km)', aspectmode='data'),
        title='3D Orbital Path',
        height=700,
        showlegend=True
    )
    return fig

def get_live_satellite_position(tle_line1, tle_line2):
    ts = load.timescale()
    satellite = EarthSatellite(tle_line1, tle_line2, "Live Satellite", ts)
    geocentric = satellite.at(ts.now()).position.km
    return geocentric.tolist()  # [x, y, z]
