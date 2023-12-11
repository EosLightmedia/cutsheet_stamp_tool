import React from "react";

function DateFormatSelector({ dateFormat, setDateFormat }) {
  const formats = ["YYYY/MM/DD", "MM/DD/YYYY", "DD/MM/YYYY"];

  return (
    <div className="date-format-selector-container">
      <label className="input-label">Date Format:</label>
      <div className="button-group">
        {formats.map((format) => (
          <button
            key={format}
            onClick={() => setDateFormat(format)}
            className={dateFormat === format ? "selected" : ""}
          >
            {format}
          </button>
        ))}
      </div>
    </div>
  );
}

export default DateFormatSelector;
