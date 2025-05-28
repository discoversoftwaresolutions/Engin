import { Link } from "react-router-dom";

const modules = [
  { name: "FusionX", route: "/fusionx", description: "AI-enhanced CAD + CAM tools" },
  { name: "SimulAI", route: "/simulai", description: "Simulation, FEA, and load optimization" },
  { name: "ProtoPrint", route: "/protoprint", description: "3D printing and material recommendations" },
  { name: "CircuitIQ", route: "/circuitiq", description: "PCB layout and power integrity tools" },
  { name: "CodeMotion", route: "/codemotion", description: "Firmware and robotic orchestration" },
  { name: "VisuAI", route: "/visuai", description: "Photorealistic rendering and ergonomic analysis" },
  { name: "FlowCore", route: "/flowcore", description: "Digital twin and compliance lifecycle" },
];

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-4xl font-bold text-center text-gray-800 mb-8">Enginuity Engineering Suite</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {modules.map((mod) => (
          <Link to={mod.route} key={mod.name}>
            <div className="p-6 bg-white rounded-lg shadow hover:shadow-lg transition-shadow duration-200">
              <h2 className="text-xl font-semibold text-blue-700 mb-2">{mod.name}</h2>
              <p className="text-gray-600">{mod.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
