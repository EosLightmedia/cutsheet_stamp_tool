import React from "react"
import StampIcon from "../Assets/stamp-icon.png"

function StampSubmit({ openPopup, jobName, jobCode, preparedFor, URLFolder }) {
  // Determine if all required fields are filled out
  const isActive = jobName && jobCode && preparedFor && URLFolder

  const getMissingFieldsMessage = () => {
    const missingFields = []
    if (!jobName) missingFields.push("Job Name")
    if (!jobCode) missingFields.push("Job Code")
    if (!preparedFor) missingFields.push("Prepared For")
    if (!URLFolder) missingFields.push("Box Folder Link")

    return missingFields.length ? (
      <span>
        Please complete: <strong>{missingFields.join(", ")}</strong>
      </span>
    ) : (
      "Good job! Almost ready for stamping..."
    )
  }

  return (
    <div className="stamp-div">
      <button
        className="submit-button"
        onClick={openPopup}
        disabled={!isActive}
      >
        <img src={StampIcon} className="stamp-icon" alt="Stamp Icon" />
        Confirm Stamp Details
      </button>
      <p className="helper-text-submit">{getMissingFieldsMessage()}</p>
    </div>
  )
}

export default StampSubmit
