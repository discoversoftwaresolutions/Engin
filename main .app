import React, { useState, useEffect } from "react";
import EnginuityDashboard from "./components/enginuity";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "https://enginuity-production.up.railway.app";

const moduleMap = {
  "Home": "home",
  "AeroIQ - Aerospace": "aeroiq",
  "FlowCore - Digital Twin & Compliance": "flowcore",
  "FusionX - Energy & Plasma": "fusionx",
  "Simulai - Simulation AI": "simulai",
  "VisuAI - Visual Intelligence": "visuai",
  "ProtoPrint - Additive MFG": "protoprint",
  "CircuitIQ - Electronics": "circuitiq",
  "CodeMotion - Robotics Code": "codemotion",
};

const EnginuityDashboard = () => {
  const [selectedModule, setSelectedModule] = useState("Home");
  const [moduleContent, setModuleContent] = useState(null);
  const [apiStatus, setApiStatus] = useState("Checking API...");

  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/status`);
        if (response.ok) {
          setApiStatus("✅ Connected to Enginuity API");
        } else {
          setApiStatus("⚠️ API connection issue");
        }
      } catch (error) {
        setApiStatus("❌ Unable to connect to API");
        console.error("API status error:", error);
      }
    };

    checkApiStatus();
  }, []);

  useEffect(() => {
    const loadModule = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/${moduleMap[selectedModule]}/dashboard`);
        if (response.ok) {
          const data = await response.json();
          setModuleContent(data.html); // Assume API returns HTML
        } else {
          setModuleContent(`<p>❌ Failed to load ${selectedModule} module.</p>`);
        }
      } catch (error) {
        setModuleContent(`<p>❌ Error loading module: ${error.message}</p>`);
      }
    };

    loadModule();
  }, [selectedModule]);

  return (
    <div className="enginuity-dashboard">
      <h1>🧠 Enginuity Agentic Suite</h1>
      <p>{apiStatus}</p>

      <select value={selectedModule} onChange={(e) => setSelectedModule(e.target.value)}>
        {Object.keys(moduleMap).map((module) => (
          <option key={module} value={module}>{module}</option>
        ))}
      </select>

      <div dangerouslySetInnerHTML={{ __html: moduleContent }} />
    </div>
  );
};

export default EnginuityDashboard;
