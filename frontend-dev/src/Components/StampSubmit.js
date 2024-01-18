import React from "react"
import StampIcon from "../Assets/stamp-icon.png"

function StampSubmit({ isActive, openPopup }) {
  return (
    <div className="stamp-div">
      <button
        className="submit-button"
        onClick={() => openPopup()}
        disabled={!isActive}
      >
        <img src={StampIcon} className="stamp-icon" alt="Stamp Icon" />
        Confirm Stamp Details
      </button>
      <p className="helper-text-submit">
        {isActive
          ? "Good job! Almost ready for stamping..."
          : "All fields must be filled in first."}
      </p>
    </div>
  )
}

export default StampSubmit
