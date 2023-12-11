import React from "react";

function RevisionSelector({ isRevision, setIsRevision }) {
  return (
    <div className="revision-selector-container">
      <label className="input-label">Is this a revision?</label>
      <div className="button-group">
        <button
          onClick={() => setIsRevision(false)}
          className={!isRevision ? "selected" : ""}
        >
          No
        </button>
        <button
          onClick={() => setIsRevision(true)}
          className={isRevision ? "selected" : ""}
        >
          Yes
        </button>
      </div>
    </div>
  );
}

export default RevisionSelector;
