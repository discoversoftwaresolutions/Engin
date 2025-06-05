import React from "react";
import ReactDOM from "react-dom";
import TestComponent from "./testImports";

ReactDOM.render(
  <React.StrictMode>
    <TestComponent />
  </React.StrictMode>,
  document.getElementById("root")
);
