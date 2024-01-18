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

  console.log(gradientStyle)

  const formatRevisionNumber = (number) => {
    return String(number).padStart(2, "0")
  }

  const disclaimerTextOptions = {
    0: "For bid purposes only.",
    1: "For review and not for construction.",
    2: "For even more testing.",
  }

  const displayLogo =
    preparedBy === "Eos Lightmedia"
      ? EosLogo
      : preparedBy === "Abernathy Lighting Design"
      ? AbernathyLogo
      : null

  const getGradientStyle = (gradientStyle, preparedBy) => {
    if (!gradientStyle) {
      return {} // Return an empty object if gradientStyle is false
    }

    if (preparedBy === "Eos Lightmedia") {
      return {
        backgroundImage: `url(${PurpleGradient})`,
        backgroundPosition: "bottom left",
        backgroundRepeat: "no-repeat",
        backgroundSize: "cover",
      }
    } else if (preparedBy === "Abernathy Lighting Design") {
      return {
        backgroundImage: `url(${OrangeGradient})`,
        backgroundPosition: "bottom left",
        backgroundRepeat: "no-repeat",
        backgroundSize: "cover",
      }
    }

    return {} // Return an empty object as default
  }

  const previewStyle = getGradientStyle(gradientStyle)

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
              <span className="label">Note</span>
              <span className="value">{jobPhase}</span>
            </p>
          </div>
        </div>
        {displayLogo && (
          <img className="preview-logo" src={displayLogo} alt="Company Logo" />
        )}
        <div className="disclaimer-div">
          <div className="disclaimer-div-content">
            {disclaimer.map(
              (isSelected, index) =>
                isSelected && (
                  <p key={index}>
                    <em>{disclaimerTextOptions[index]}</em>
                  </p>
                )
            )}
          </div>
        </div>
      </div>

      <div className="preview-footer">
        <div className="stamp-footer-content">
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
