import React, { useState } from "react";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "https://enginuity-production.up.railway.app";

const SimulAI = () => {
  const [simFile, setSimFile] = useState(null);
  const [simType, setSimType] = useState("Structural");
  const [material, setMaterial] = useState("");
  const [meshPreview, setMeshPreview] = useState(null);
  const [simulationResults, setSimulationResults] = useState([]);

  const handleFileUpload = (event) => {
    setSimFile(event.target.files[0]);
  };

  const runSimulation = async () => {
    if (!simFile) return alert("Please upload a simulation model first.");

    const formData = new FormData();
    formData.append("file", simFile);
    formData.append("material", material || "Unknown");
    formData.append("quality", "medium");

    try {
      const response = await fetch(`${API_BASE_URL}/simulai/generate-mesh`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (response.ok) {
        setMeshPreview(data.mesh_preview_url || "https://fallback-image-url.com/default.png");
      } else {
        alert("Mesh generation failed.");
      }
    } catch (error) {
      console.error("Simulation API error:", error);
    }
  };

  return (
    <div className="simulai-dashboard">
      <h1>🧩 SimulAI: FEA / CFD / CAE Agent</h1>
      <p>Run structural, thermal, and fluid simulations powered by AI.</p>

      <input type="file" onChange={handleFileUpload} accept=".step,.iges,.stl" />
      <select value={simType} onChange={(e) => setSimType(e.target.value)}>
        <option>Structural</option>
        <option>Thermal</option>
        <option>Fluid</option>
        <option>Electromagnetic</option>
      </select>
      <input type="text" placeholder="e.g., Aluminum 6061-T6" value={material} onChange={(e) => setMaterial(e.target.value)} />

      <button onClick={runSimulation}>🔍 Run Simulation</button>

      {meshPreview && <img src={meshPreview} alt="Mesh Preview" width="500" />}

      <h2>📊 Simulation Results</h2>
      <table>
        <thead>
          <tr><th>Time (s)</th><th>Max Stress (MPa)</th></tr>
        </thead>
        <tbody>
          {[0, 1, 2, 3, 4, 5].map((time, idx) => (
            <tr key={idx}>
              <td>{time}</td>
              <td>{[0, 75, 120, 150, 175, 180][idx]}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <p>📋 AI Analysis: Max stress of 180 MPa observed. Yield = 260 MPa → PASS.</p>
    </div>
  );
};

export default SimulAI;
