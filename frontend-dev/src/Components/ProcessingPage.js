import React from "react"
import LoadingSpinner from "../Assets/loading-spinner.gif"

function ProcessingPage() {
  return (
    <div className="processing-page-div">
      <div className="processing-page-content">
        <img
          src={LoadingSpinner}
          className="loading-spinner"
          alt="Loading Spinner"
        />
        <p className="large-pop-up-text">
          Your cut sheets are being stamped
          <span className="ellipsis">
            <span>.</span>
            <span>.</span>
            <span>.</span>
          </span>
        </p>
        <p className="small-pop-up-text">
          This window will close automatically when the process is complete.
        </p>
      </div>
    </div>
  )
}

export default ProcessingPage
