import React, { useState } from "react";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "https://enginuity-production.up.railway.app";

const SimulAI = () => {
  const [simFile, setSimFile] = useState(null);
  const [simType, setSimType] = useState("Structural");
  const [material, setMaterial] = useState("");
  const [meshPreview, setMeshPreview] = useState(null);
  const [simulationResults, setSimulationResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = (event) => {
    setSimFile(event.target.files[0]);
  };

  const runSimulation = async () => {
    if (!simFile) {
      alert("⚠️ Please upload a simulation model first.");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", simFile);
    formData.append("material", material || "Unknown");
    formData.append("quality", "medium");
    formData.append("simulationType", simType);

    try {
      const response = await fetch(`${API_BASE_URL}/simulai/run-simulation`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (response.ok) {
        setMeshPreview(data.mesh_preview_url || "https://fallback-image-url.com/default.png");
        setSimulationResults(data.results || []);
      } else {
        setError(`❌ Simulation failed: ${data.message || "Unknown error"}`);
      }
    } catch (error) {
      setError(`🚨 Simulation API error: ${error.message}`);
      console.error("Simulation API error:", error);
    } finally {
      setLoading(false);
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

      <button onClick={runSimulation} disabled={loading}>
        {loading ? "⏳ Running..." : "🔍 Run Simulation"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {meshPreview && <img src={meshPreview} alt="Mesh Preview" width="500" />}

      <h2>📊 Simulation Results</h2>
      {simulationResults ? (
        <table>
          <thead>
            <tr><th>Time (s)</th><th>Max Stress (MPa)</th></tr>
          </thead>
          <tbody>
            {simulationResults.map((result, idx) => (
              <tr key={idx}>
                <td>{result.time}</td>
                <td>{result.maxStress}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>⚡ No simulation results available yet.</p>
      )}

      <p>📋 AI Analysis: {simulationResults ? `Max stress of ${simulationResults?.[simulationResults.length - 1]?.maxStress} MPa observed.` : "Awaiting simulation data."}</p>
    </div>
  );
};

export default SimulAI;
