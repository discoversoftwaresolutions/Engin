import * as THREE from "three";

// Constants
const EARTH_RADIUS_KM = 6371;

/**
 * Compute orbital path in 3D space
 * @param {number} semiMajorAxisKm - Semi-major axis of the orbit in km
 * @param {number} eccentricity - Orbit eccentricity (0 = circular, 1 = parabolic)
 * @param {number} inclinationDeg - Inclination angle in degrees
 * @returns {Object} - 3D orbital coordinates { x, y, z }
 */
function computeOrbit3D(semiMajorAxisKm, eccentricity, inclinationDeg = 0.0, numPoints = 360) {
  const theta = Array.from({ length: numPoints }, (_, i) => (i * (2 * Math.PI)) / numPoints);
  const r = theta.map(t => semiMajorAxisKm * (1 - eccentricity ** 2) / (1 + eccentricity * Math.cos(t)));

  const x = r.map((radius, i) => radius * Math.cos(theta[i]));
  const y = r.map((radius, i) => radius * Math.sin(theta[i]));

  const inclinationRad = (Math.PI / 180) * inclinationDeg;
  const z = y.map(yValue => yValue * Math.sin(inclinationRad));
  const yInclined = y.map(yValue => yValue * Math.cos(inclinationRad));

  return { x, y: yInclined, z };
}

/**
 * Plot 3D Orbit using Three.js
 */
function plotOrbit3D(scene, semiMajorAxisKm, eccentricity, inclinationDeg) {
  const { x, y, z } = computeOrbit3D(semiMajorAxisKm, eccentricity, inclinationDeg);

  const geometry = new THREE.BufferGeometry();
  const vertices = new Float32Array(x.length * 3);

  x.forEach((_, i) => {
    vertices[i * 3] = x[i];
    vertices[i * 3 + 1] = y[i];
    vertices[i * 3 + 2] = z[i];
  });

  geometry.setAttribute("position", new THREE.BufferAttribute(vertices, 3));
  const material = new THREE.LineBasicMaterial({ color: "lime" });
  const line = new THREE.Line(geometry, material);

  scene.add(line);
}

/**
 * Get live satellite position from API (mock for now)
 */
async function getLiveSatellitePosition(tleLine1, tleLine2) {
  // TODO: Implement real-time API-based tracking
  return { x: Math.random() * 10000, y: Math.random() * 10000, z: Math.random() * 10000 };
}

export { computeOrbit3D, plotOrbit3D, getLiveSatellitePosition };
