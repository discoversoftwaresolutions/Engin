import React, { useState } from "react";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "https://enginuity-production.up.railway.app";

const VisuAI = () => {
  const [model, setModel] = useState(null);
  const [renderStyle, setRenderStyle] = useState("Photorealism");
  const [percentile, setPercentile] = useState(50);
  const [showStressZones, setShowStressZones] = useState(false);
  const [renderResult, setRenderResult] = useState(null);

  const handleFileUpload = (event) => {
    setModel(event.target.files[0]);
  };

  const generateRender = async () => {
    if (!model) return alert("Please upload a model first.");

    const formData = new FormData();
    formData.append("file", model);
    formData.append("style", renderStyle);

    try {
      const response = await fetch(`${API_BASE_URL}/generate-render`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setRenderResult(data.render_url || "https://fallback-image-url.com/default.png");
    } catch (error) {
      console.error("Render failed:", error);
    }
  };

  const runErgonomicEvaluation = async () => {
    if (!model) return alert("Please upload a model first.");

    try {
      const response = await fetch(`${API_BASE_URL}/ergonomic-evaluation`, {
        method: "POST",
        body: JSON.stringify({ model_name: model.name }),
        headers: { "Content-Type": "application/json" },
      });
      if (response.ok) {
        alert("✅ Ergonomic evaluation completed.");
      } else {
        alert("❌ Evaluation failed.");
      }
    } catch (error) {
      console.error("Ergonomic evaluation failed:", error);
    }
  };

  return (
    <div className="visuai-dashboard">
      <h1>🎨 VisuAI – Rendering & Ergonomic Design</h1>
      <p>Generate photorealistic renders, optimize product forms, and evaluate ergonomic fit in 3D environments.</p>

      <input type="file" onChange={handleFileUpload} accept=".obj,.stl,.fbx" />
      <select value={renderStyle} onChange={(e) => setRenderStyle(e.target.value)}>
        <option>Photorealism</option>
        <option>Sketch</option>
        <option>Wireframe</option>
      </select>

      <button onClick={generateRender}>🖼 Generate Render</button>
      <button onClick={runErgonomicEvaluation}>🔍 Run Ergonomic Fit Evaluation</button>

      {renderResult && <img src={renderResult} alt="Rendered Model" width="500" />}

      <h2>📏 Ergonomic Fit Parameters</h2>
      <input type="range" min="1" max="99" value={percentile} onChange={(e) => setPercentile(e.target.value)} />
      <label>Anthropometric Percentile: {percentile}</label>

      <input type="checkbox" checked={showStressZones} onChange={(e) => setShowStressZones(e.target.checked)} />
      <label>Highlight Ergonomic Stress Zones</label>
    </div>
  );
};

export default VisuAI;
