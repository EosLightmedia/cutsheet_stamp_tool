import React from "react";

function ConfirmPopUp({
  jobName,
  jobCode,
  boxFolder,
  preparedFor,
  preparedBy,
  date,
  isRevision,
  jobPhase,
  gradientStyle,
  revisionNumber,
  hidePopUp,
  handleSubmit,
}) {
  const formatDate = (date) => {
    return `${date.year}-${date.month.toString().padStart(2, "0")}-${date.day
      .toString()
      .padStart(2, "0")}`;
  };

  return (
    <div className="confirm-pop-up">
      <div className="confirm-pop-up-content">
        <h2>All looks good?</h2>
        <div className="confirm-details">
          <p>
            Job Name: <span className="value">{jobName}</span>
          </p>
          <p>
            Job Code: <span className="value">{jobCode}</span>
          </p>
          <p>
            Box Folder: <span className="value">{boxFolder}</span>
          </p>
          <p>
            Prepared For: <span className="value">{preparedFor}</span>
          </p>
          <p>
            Prepared By: <span className="value">{preparedBy}</span>
          </p>
          <p>
            Date: <span className="value">{formatDate(date)}</span>
          </p>
          <p>
            Is Revision:{" "}
            <span className="value">{isRevision ? "Yes" : "No"}</span>
          </p>
          <p>
            Job Phase: <span className="value">{jobPhase}</span>
          </p>
          <p>
            Gradient Style: <span className="value">{gradientStyle}</span>
          </p>

          <p>
            Revision Number: <span className="value">{revisionNumber}</span>
          </p>
        </div>
        <div className="confirm-buttons">
          <button onClick={hidePopUp}>CANCEL</button>
          <button onClick={handleSubmit}>YES, STAMP AWAY</button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmPopUp;
