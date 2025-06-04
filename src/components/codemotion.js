import React, { useState } from "react";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "https://enginuity-production.up.railway.app";

const CodeMotion = () => {
  const [firmwareTarget, setFirmwareTarget] = useState("ESP32");
  const [uploadedFile, setUploadedFile] = useState(null);
  const [simulationLogs, setSimulationLogs] = useState(false);
  const [resourceMetrics, setResourceMetrics] = useState(false);
  const [responseData, setResponseData] = useState(null);

  const handleFileUpload = (event) => {
    setUploadedFile(event.target.files[0]);
  };

  const executeTask = async (taskEndpoint) => {
    if (!uploadedFile) {
      alert("⚠️ Please upload a code file first.");
      return;
    }

    const payload = { filename: uploadedFile.name, platform: firmwareTarget };

    try {
      const response = await fetch(`${API_BASE_URL}/${taskEndpoint}`, {
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

  return (
    <div className="codemotion-dashboard">
      <h1>🤖 CodeMotion – Robotics & Embedded Systems</h1>
      <p>Generate firmware, compose ROS2 trees, and simulate robotic logic.</p>

      <select value={firmwareTarget} onChange={(e) => setFirmwareTarget(e.target.value)}>
        <option>ESP32</option>
        <option>STM32</option>
        <option>Arduino</option>
        <option>Raspberry Pi</option>
      </select>

      <input type="file" onChange={handleFileUpload} accept=".yaml,.json,.ino,.c,.cpp" />

      <button onClick={() => executeTask("generate-firmware")}>⚙️ Generate Firmware</button>
      <button onClick={() => executeTask("compose-ros2")}>🌐 Compose ROS2 Behavior Tree</button>
      <button onClick={() => executeTask("simulate-behavior")}>🔄 Run Behavior Simulation</button>

      {responseData && <pre>{JSON.stringify(responseData, null, 2)}</pre>}

      <h2>🎯 Simulation Settings</h2>
      <label>
        <input type="checkbox" checked={simulationLogs} onChange={(e) => setSimulationLogs(e.target.checked)} />
        📜 Enable Detailed Execution Logs
      </label>
      <label>
        <input type="checkbox" checked={resourceMetrics} onChange={(e) => setResourceMetrics(e.target.checked)} />
        📊 Show Resource Utilization Metrics
      </label>
    </div>
  );
};

export default CodeMotion;
