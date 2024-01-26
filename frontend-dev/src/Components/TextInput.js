import React from "react"
import Good from "../Assets/good.png"

function TextInput({
  label,
  value,
  placeHolder,
  onChange,
  optionalOrRequired,
  optionalOrRequiredText,
  id,
  name,
}) {
  return (
    <div className="text-input-container">
      {label && <label className="selector-label">{label}</label>}
      <input
        type="text"
        placeholder={placeHolder}
        value={value}
        onChange={onChange}
        id={id}
        name={name}
      />
      <p className="optional-or-required-p">
        <em>{optionalOrRequiredText}</em>
        {optionalOrRequired && value && (
          <img
            src={Good}
            className="tiny-icon"
            alt="Good"
            style={{ marginLeft: "5px" }}
          />
        )}
      </p>
    </div>
  )
}

export default TextInput
