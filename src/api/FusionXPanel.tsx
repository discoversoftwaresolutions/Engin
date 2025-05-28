import { useState } from "react";
import { runAgentTask } from "../../api/agentClient";

export default function FusionXPanel() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState("");

  const handleRun = async () => {
    const res = await runAgentTask("fusionx", { prompt });
    setResult(res.data.result);
  };

  return (
    <div className="p-4 border rounded shadow-md">
      <h2 className="text-xl font-bold mb-2">FusionX CAD Task</h2>
      <textarea
        className="w-full p-2 border mb-2"
        placeholder="Describe your CAD optimization goal..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button className="bg-blue-600 text-white px-4 py-2" onClick={handleRun}>
        Run Agent
      </button>
      <pre className="mt-4 bg-gray-100 p-3">{result}</pre>
    </div>
  );
}
