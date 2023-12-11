import React from "react";

function TextInput({ label, value, placeHolder, onChange }) {
  return (
    <div className="text-input-container">
      {label && <label className="selector-label">{label}</label>}
      <input
        type="text"
        placeholder={placeHolder}
        value={value}
        onChange={onChange}
      />
    </div>
  );
}

export default TextInput;
