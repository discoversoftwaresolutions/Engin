// src/testImports.js
import React from "react";

// Import all your components/services here:
import SimulAI from "./simulai";
import ProtoPrint from "./protoprint";
import FusionX from "./fusionx";
import FlowCore from "./flowcore";
import CodeMotion from "./codemotion";
import CircuitIQ from "./circuitiq";

// Uncomment only one import below at a time to test
// const TestComponent = () => <SimulAI />;
// const TestComponent = () => <ProtoPrint />;
// const TestComponent = () => <FusionX />;
// const TestComponent = () => <FlowCore />;
// const TestComponent = () => <CodeMotion />;
// const TestComponent = () => <CircuitIQ />;

// Or if you want to test a service function:
// import { computeOrbit } from "./services/orbital";
// const TestComponent = () => <div>{computeOrbit ? "Orbit function loaded" : "No function"}</div>;

const TestComponent = () => <div>Select an import to test in src/testImports.js</div>;

export default TestComponent;
