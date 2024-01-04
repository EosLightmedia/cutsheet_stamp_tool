import React from "react"
import EosLogo from "../Assets/eos-logo.png"
import AbernathyLogo from "../Assets/abernathy-logo.png"
import PurpleGradient from "../Assets/purple-gradient.png"
import OrangeGradient from "../Assets/orange-gradient.png"
import "../Styles/StampPreview.css"

function StampPreview(props) {
  const {
    jobName,
    jobCode,
    preparedFor,
    preparedBy,
    date,
    isRevision,
    jobPhase,
    gradientStyle,
    revisionNumber,
    disclaimer,
    showPageNumbers,
  } = props

  const formatRevisionNumber = (number) => {
    return String(number).padStart(2, "0")
  }

  const displayLogo =
    preparedBy === "Eos Lightmedia"
      ? EosLogo
      : preparedBy === "Abernathy Lighting Design"
      ? AbernathyLogo
      : null

  const getGradientStyle = (gradient) => {
    switch (gradient) {
      case "Purple/Blue":
        return {
          backgroundImage: `url(${PurpleGradient})`,
          backgroundPosition: "bottom left",
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
        }
      case "Yellow/Green":
        return {
          backgroundImage: `url(${OrangeGradient})`,
          backgroundPosition: "bottom left",
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
        }
      default:
        return {}
    }
  }

  const previewStyle = getGradientStyle(gradientStyle)

  const getDisclaimerText = (disclaimerValue) => {
    switch (disclaimerValue) {
      case "1":
        return "This document is for bid purposes only."
      case "2":
        return "This document is for review and not for construction."
      case "3":
        return "This is a generic disclaimer."
      default:
        return ""
    }
  }

  const disclaimerText = getDisclaimerText(disclaimer)

  return (
    <div className="content-div">
      <div className="stamp-preview-div" style={previewStyle}>
        <div className="first-column">
          <p className="type-title">
            Type
            <br />
            <span className="type-value">EG01</span>
          </p>
        </div>
        <div className="second-column">
          <div className="info-grid">
            <p>
              <span className="label">Project Name</span>
              <span className="value">{jobName}</span>
            </p>
            <p>
              <span className="label">Job Code</span>
              <span className="value">{jobCode}</span>
            </p>
            <p>
              <span className="label">Prepared For</span>
              <span className="value">{preparedFor}</span>
            </p>
            <p>
              <span className="label">Project Phase</span>
              <span className="value">{jobPhase}</span>
            </p>
          </div>
        </div>
        {displayLogo && (
          <img className="preview-logo" src={displayLogo} alt="Company Logo" />
        )}
        <div className="disclaimer-div">
          <div className="disclaimer-div-content">
            <p>
              <em>{disclaimerText}</em>{" "}
            </p>
          </div>
        </div>
      </div>

      <div className="preview-footer">
        <div className="footer-content">
          <p>
            {isRevision ? "Revision Date" : "Issued Date"}:{" "}
            <span className="footer-value">{date}</span>
            {isRevision && (
              <>
                {"  |  "}
                Rev:{" "}
                <span className="footer-value">
                  {formatRevisionNumber(revisionNumber)}
                </span>
              </>
            )}
          </p>
          {showPageNumbers && (
            <p>
              Page <strong>XX</strong> of <strong>XX</strong>
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

export default StampPreview
