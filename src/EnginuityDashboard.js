import React, { useState, useEffect } from "react";
import SimulAI from "./simulai";
import ProtoPrint from "./protoprint";
import FusionX from "./fusionx";
import FlowCore from "./flowcore";
import CodeMotion from "./codemotion";
import CircuitIQ from "./circuitiq";
import { computeOrbit, computeHohmannTransfer } from "../services/orbital";
import { plotOrbit3D } from "../services/orbital3D";

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

const componentMap = {
  simulai: <SimulAI />,
  protoprint: <ProtoPrint />,
  fusionx: <FusionX />,
  flowcore: <FlowCore />,
  codemotion: <CodeMotion />,
  circuitiq: <CircuitIQ />,
};

const EnginuityDashboard = () => {
  const [selectedModule, setSelectedModule] = useState("Home");
  const [moduleContent, setModuleContent] = useState(null);
  const [apiStatus, setApiStatus] = useState("Checking API...");

  useEffect(() => {
    plotOrbit3D(8000, 0.2, 28.5); // visual startup render
  }, []);

  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/status`);
        setApiStatus(response.ok
          ? "✅ Connected to Enginuity API"
          : "⚠️ API connection issue"
        );
      } catch (error) {
        setApiStatus("❌ Unable to connect to API");
        console.error("API status error:", error);
      }
    };

    checkApiStatus();
  }, []);

  useEffect(() => {
    const loadModule = async () => {
      const key = moduleMap[selectedModule];
      if (componentMap[key]) {
        setModuleContent(null); // render local React component
        return;
      }

      try {
        const response = await fetch(`${API_BASE_URL}/${key}/dashboard`);
        if (response.ok) {
          const data = await response.json();
          setModuleContent(data.html || `<p>✅ ${selectedModule} loaded.</p>`);
        } else {
          setModuleContent(`<p>❌ Failed to load ${selectedModule} module.</p>`);
        }
      } catch (error) {
        setModuleContent(`<p>❌ Error loading module: ${error.message}</p>`);
      }
    };

    loadModule();
  }, [selectedModule]);

  const key = moduleMap[selectedModule];

  return (
    <div className="enginuity-dashboard">
      <h1>🧠 Enginuity Agentic Suite</h1>
      <p>{apiStatus}</p>

      <select value={selectedModule} onChange={(e) => setSelectedModule(e.target.value)}>
        {Object.keys(moduleMap).map((module) => (
          <option key={module} value={module}>{module}</option>
        ))}
      </select>

      <div className="module-render-area">
        {componentMap[key] || (
          <div dangerouslySetInnerHTML={{ __html: moduleContent }} />
        )}
      </div>
    </div>
  );
};

export default EnginuityDashboard;
