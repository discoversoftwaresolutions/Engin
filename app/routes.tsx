import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "../pages/Dashboard";

// Module Panels
import FusionXPanel from "../modules/FusionX/FusionXPanel";
import SimulAIChart from "../modules/SimulAI/SimulAIChart";
import Proto3DView from "../modules/ProtoPrint/Proto3DView";
import CircuitValidator from "../modules/CircuitIQ/CircuitValidator";
import BehaviorComposer from "../modules/CodeMotion/BehaviorComposer";
import RenderPreview from "../modules/VisuAI/RenderPreview";
import ComplianceView from "../modules/FlowCore/ComplianceView";

export default function AppRoutes() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/fusionx" element={<FusionXPanel />} />
        <Route path="/simulai" element={<SimulAIChart />} />
        <Route path="/protoprint" element={<Proto3DView />} />
        <Route path="/circuitiq" element={<CircuitValidator />} />
        <Route path="/codemotion" element={<BehaviorComposer />} />
        <Route path="/visuai" element={<RenderPreview />} />
        <Route path="/flowcore" element={<ComplianceView />} />
      </Routes>
    </Router>
  );
}
