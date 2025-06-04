import React, { useState } from "react";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "https://enginuity-production.up.railway.app/circuitiq";

const CircuitIQ = () => {
  const [pcbData, setPcbData] = useState('{"components":[], "connections":[]}');
  const [powerData, setPowerData] = useState('{"voltage":3.3,"current":0.8,"trace_width":0.5}');
  const [bomData, setBomData] = useState('[{"part":"LM317","available":false}]');
  const [layoutPreview, setLayoutPreview] = useState(null);
  const [responseData, setResponseData] = useState(null);

  const executeTask = async (endpoint, payload) => {
    try {
      const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();

      if (response.ok) {
        setResponseData(data);
      } else {
        alert(`❌ API Error: ${response.status}`);
      }
    } catch (error) {
      console.error("🚨 Task Execution API error:", error);
    }
  };

  const fetchLayoutPreview = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/layout-preview`);
      const data = await response.json();

      if (response.ok) {
        setLayoutPreview(data.preview_url || "https://fallback-image-url.com/default.png");
      } else {
        alert("❌ Layout preview retrieval failed.");
      }
    } catch (error) {
      console.error("🚨 Layout preview API error:", error);
    }
  };

  return (
    <div className="circuitiq-dashboard">
      <h1>🧠 CircuitIQ – PCB Optimization & Supply Chain Intelligence</h1>
      <p>Enhance circuit layouts, analyze power integrity, and check supply chain availability.</p>

      <h2>🧩 Auto Layout Generator</h2>
      <textarea value={pcbData} onChange={(e) => setPcbData(e.target.value)} />
      <button onClick={() => executeTask("auto-layout", JSON.parse(pcbData))}>Generate PCB Layout</button>

      <h2>⚡ Power Integrity Checker</h2>
      <textarea value={powerData} onChange={(e) => setPowerData(e.target.value)} />
      <button onClick={() => executeTask("power-integrity", JSON.parse(powerData))}>Check Power Integrity</button>

      <h2>🚚 Supply Chain Availability</h2>
      <textarea value={bomData} onChange={(e) => setBomData(e.target.value)} />
      <button onClick={() => executeTask("supply-chain", JSON.parse(bomData))}>Check Supply Chain</button>

      <h2>📐 Layout Preview</h2>
      <button onClick={fetchLayoutPreview}>Fetch Layout Preview</button>
      {layoutPreview && <img src={layoutPreview} alt="Generated PCB Layout" width="500" />}

      {responseData && <pre>{JSON.stringify(responseData, null, 2)}</pre>}
    </div>
  );
};

export default CircuitIQ;
