import React from "react";

function RevisionNumberSelector({ revisionNumber, setRevisionNumber }) {
  const handleChange = (event) => {
    const number = parseInt(event.target.value, 10);
    if (!isNaN(number)) {
      setRevisionNumber(number);
    } else {
      setRevisionNumber(1);
    }
  };

  return (
    <div className="revision-number-container">
      <label htmlFor="revision-number" className="input-label">
        Revision Number:
      </label>
      <input
        type="number"
        id="revision-number"
        className="text-input"
        value={revisionNumber}
        onChange={handleChange}
        min="1"
      />
    </div>
  );
}

export default RevisionNumberSelector;
