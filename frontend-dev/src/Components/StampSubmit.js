import React from "react";
import StampIcon from "../Assets/stamp-icon.png";

function StampSubmit({ onClick, isActive }) {
  return (
    <div className="stamp-div">
      <button className="submit-button" onClick={onClick} disabled={!isActive}>
        <img src={StampIcon} className="stamp-icon" alt="Stamp Icon" />
        Stamp Cut Sheets
      </button>
      <p className="helper-text-submit">
        {isActive
          ? "Good job! Looks ready for stamping..."
          : "All fields must be filled in first."}
      </p>
    </div>
  );
}

export default StampSubmit;
