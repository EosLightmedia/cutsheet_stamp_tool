import React from "react";

function GradientSelector({ gradient, setGradient }) {
  const gradients = ["No Gradient", "Purple/Blue", "Yellow/Green"];

  return (
    <div className="gradient-selector-container">
      <label className="input-label">Gradient Style:</label>
      <div className="button-group">
        {gradients.map((g) => (
          <button
            key={g}
            onClick={() => setGradient(g)}
            className={gradient === g ? "selected" : ""}
          >
            {g}
          </button>
        ))}
      </div>
    </div>
  );
}

export default GradientSelector;
