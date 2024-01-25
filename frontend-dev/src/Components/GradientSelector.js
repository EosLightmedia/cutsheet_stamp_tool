import React from "react"

const GradientSelector = ({ gradient, setGradient }) => {
  const getHelperText = () => {
    if (gradient) {
      return "Stamp will have a gradient."
    } else {
      return "No gradient will be shown."
    }
  }

  return (
    <div className="text-input-container">
      <label className="selector-label-input-package">Show Gradient?</label>
      <div>
        <div className="button-group-package">
          <button
            onClick={() => setGradient(true)}
            className={gradient ? "selected" : ""}
          >
            Yes
          </button>
          <button
            onClick={() => setGradient(false)}
            className={!gradient ? "selected" : ""}
          >
            No
          </button>
        </div>
        <div className="helper-text-package-div">
          <p className="helper-text-package">{getHelperText()}</p>
        </div>
      </div>
    </div>
  )
}

export default GradientSelector
