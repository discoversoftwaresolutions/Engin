import React, { useState, useEffect } from "react";
// import SimulAI from "./simulai";
// import ProtoPrint from "./protoprint";
// import FusionX from "./fusionx";
// import FlowCore from "./flowcore";
// import CodeMotion from "./codemotion";
// import CircuitIQ from "./circuitiq";
// import { computeOrbit, computeHohmannTransfer } from "./services/orbital";
// import { plotOrbit3D } from "./services/orbital3D";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "https://enginuity-production.up.railway.app";

const EnginuityDashboard = () => {
  const [selectedModule, setSelectedModule] = useState("Home");
  const [moduleContent, setModuleContent] = useState(null);
  const [apiStatus, setApiStatus] = useState("Checking API...");

  // Commented out to isolate errors
  // useEffect(() => {
  //   plotOrbit3D(8000, 0.2, 28.5);
  // }, []);

  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/status`);
        setApiStatus(response.ok ? "✅ Connected to Enginuity API" : "⚠️ API connection issue");
      } catch (error) {
        setApiStatus("❌ Unable to connect to API");
        console.error("API status error:", error);
      }
    };
    checkApiStatus();
  }, []);

  return (
    <div className="enginuity-dashboard">
      <h1>🧠 Enginuity Agentic Suite</h1>
      <p>{apiStatus}</p>
      <p>Module content temporarily disabled for isolation test.</p>
    </div>
  );
};

export default EnginuityDashboard;
