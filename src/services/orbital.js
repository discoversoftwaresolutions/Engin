const MU_EARTH = 398600.4418; // Gravitational constant in km³/s²

function computeOrbit(semiMajorAxisKm, eccentricity, inclinationDeg = 0.0, numPoints = 360) {
  const theta = Array.from({ length: numPoints }, (_, i) => (i * (2 * Math.PI)) / numPoints);
  const r = theta.map(t => semiMajorAxisKm * (1 - eccentricity ** 2) / (1 + eccentricity * Math.cos(t)));

  // Convert to Cartesian coordinates
  const x = r.map((radius, i) => radius * Math.cos(theta[i]));
  const y = r.map((radius, i) => radius * Math.sin(theta[i]));

  // Apply inclination (2D simplification)
  const inclinationRad = (Math.PI / 180) * inclinationDeg;
  const yInclined = y.map(yValue => yValue * Math.cos(inclinationRad));

  return {
    x: x,
    y: yInclined,
    details: {
      semiMajorAxisKm,
      eccentricity,
      inclinationDeg,
      apoapsisKm: semiMajorAxisKm * (1 + eccentricity),
      periapsisKm: semiMajorAxisKm * (1 - eccentricity),
      orbitalPeriodMin: (2 * Math.PI * Math.sqrt(semiMajorAxisKm ** 3 / MU_EARTH)) / 60
    }
  };
}

function computeHohmannTransfer(r1Km, r2Km) {
  const v1 = Math.sqrt(MU_EARTH / r1Km);
  const v2 = Math.sqrt(MU_EARTH / r2Km);

  // Compute transfer velocities
  const vTransfer1 = Math.sqrt((2 * MU_EARTH * r2Km) / (r1Km * (r1Km + r2Km)));
  const vTransfer2 = Math.sqrt((2 * MU_EARTH * r1Km) / (r2Km * (r1Km + r2Km)));

  return {
    deltaV1KmS: vTransfer1 - v1,
    deltaV2KmS: v2 - vTransfer2,
    totalDeltaVKmS: Math.abs(vTransfer1 - v1) + Math.abs(v2 - vTransfer2),
    timeOfFlightMin: (Math.PI * Math.sqrt(((r1Km + r2Km) ** 3) / (8 * MU_EARTH))) / 60
  };
}

module.exports = { computeOrbit, computeHohmannTransfer };
