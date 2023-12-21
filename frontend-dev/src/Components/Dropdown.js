import React from "react"

function Dropdown({ label, value, onChange, options }) {
  return (
    <div className="dropdown-container">
      {label && <label className="input-label">{label}</label>}
      <select className="dropdown-select" value={value} onChange={onChange}>
        {options.map((option, index) => (
          <option
            key={index}
            value={option.value}
            disabled={option.value === ""}
          >
            {option.label}
          </option>
        ))}
      </select>
    </div>
  )
}

export default Dropdown
