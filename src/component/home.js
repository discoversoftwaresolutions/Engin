import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import AeroIQ from "./modules/aeroiq";
import FlowCore from "./modules/flowcore";
import FusionX from "./modules/fusionx";
import SimulAI from "./modules/simulai";
import VisuAI from "./modules/visuai";
import ProtoPrint from "./modules/protoprint";
import CircuitIQ from "./modules/circuitiq";
import CodeMotion from "./modules/codemotion";

const Home = () => {
  return (
    <Router>
      <div className="home-dashboard">
        <h1>🧠 Enginuity Demo Marketplace</h1>
        <p>Explore each module below:</p>

        <nav>
          <ul>
            <li><Link to="/aeroiq">🚀 AeroIQ</Link></li>
            <li><Link to="/flowcore">🔄 FlowCore</Link></li>
            <li><Link to="/fusionx">⚙️ FusionX</Link></li>
            <li><Link to="/simulai">🧩 SimulAI</Link></li>
            <li><Link to="/visuai">🎨 VisuAI</Link></li>
            <li><Link to="/protoprint">🖨️ ProtoPrint</Link></li>
            <li><Link to="/circuitiq">🔬 CircuitIQ</Link></li>
            <li><Link to="/codemotion">🤖 CodeMotion</Link></li>
          </ul>
        </nav>

        <Routes>
          <Route path="/aeroiq" element={<AeroIQ />} />
          <Route path="/flowcore" element={<FlowCore />} />
          <Route path="/fusionx" element={<FusionX />} />
          <Route path="/simulai" element={<SimulAI />} />
          <Route path="/visuai" element={<VisuAI />} />
          <Route path="/protoprint" element={<ProtoPrint />} />
          <Route path="/circuitiq" element={<CircuitIQ />} />
          <Route path="/codemotion" element={<CodeMotion />} />
        </Routes>
      </div>
    </Router>
  );
};

export default Home;
