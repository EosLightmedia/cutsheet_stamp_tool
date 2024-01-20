import React, { useState, useEffect } from "react"
import EosLogo from "../Assets/eos-logo.png"
import AbernathyLogo from "../Assets/abernathy-logo.png"
import PurpleGradient from "../Assets/purple-gradient.png"
import OrangeGradient from "../Assets/orange-gradient.png"
import LoadingSpinner from "../Assets/loading-spinner.gif"
import "../Styles/StampPreview.css"

function StampPreview(props) {
  const {
    jobName,
    jobCode,
    preparedFor,
    preparedBy,
    date,
    isRevision,
    note,
    gradientStyle,
    revisionNumber,
    disclaimer,
    showPageNumbers,
    typeArray,
  } = props

  const [currentType, setCurrentType] = useState("")
  const [key, setKey] = useState(0)
  const [isLoading, setIsLoading] = useState(false)

  const processTypeNames = (types) => {
    return types.map((type) => {
      let processedName = type.includes("_")
        ? type.split("_")[0]
        : type.replace(".pdf", "")
      return processedName
    })
  }

  useEffect(() => {
    if (typeArray && typeArray.length > 0) {
      setIsLoading(true) // Start loading when typeArray is received

      const processedTypes = processTypeNames(typeArray)

      let index = 0
      const interval = setInterval(() => {
        setCurrentType(processedTypes[index])
        setKey((prevKey) => prevKey + 1)
        if (index === 0) {
          setIsLoading(false) // End loading after the first type is set
        }
        index = (index + 1) % processedTypes.length
      }, 5000)

      return () => clearInterval(interval)
    } else {
      setIsLoading(false) // Set loading to false if typeArray is empty or not provided
    }
  }, [typeArray])

  const formatRevisionNumber = (number) => {
    return String(number).padStart(2, "0")
  }

  const disclaimerTextOptions = {
    0: "For bid purposes only",
    1: "For internal review only",
    2: "This is a generic disclaimer as a placeholder",
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
        backgroundPosition: "bottom right",
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

    return {}
  }

  const previewStyle = getGradientStyle(gradientStyle, preparedBy)

  return (
    <div className="content-div">
      <div className="stamp-preview-div" style={previewStyle}>
        <div className="type-div">
          <p className="preview-title">Type</p>
          {isLoading ? (
            <p className="preview-type-big-text-loading">
              <img src={LoadingSpinner} alt="" className="preview-loader-gif" />{" "}
              <em>Loading Found Type Names</em>
            </p>
          ) : typeArray && typeArray.length > 0 ? (
            <p
              className="preview-type-big-text"
              key={key}
              style={{ color: currentType.length > 15 ? "red" : "inherit" }}
            >
              {currentType}
            </p>
          ) : (
            <p className="preview-type-big-text-placeholder">
              <em>Type Placeholder</em>
            </p>
          )}
        </div>
        <div className="details-div">
          <p className="preview-title">Job Name</p>
          {jobName ? (
            <p className="preview-details-text">{jobName}</p>
          ) : (
            <p className="preview-details-text-placeholder">
              <em>Job Name</em>
            </p>
          )}
          <p className="preview-title">JOB CODE</p>

          {jobCode ? (
            <p className="preview-details-text">{jobCode}</p>
          ) : (
            <p className="preview-details-text-placeholder">
              <em>Job Code</em>
            </p>
          )}
          <p className="preview-title">Prepared For</p>
          {preparedFor ? (
            <p className="preview-details-text">{preparedFor}</p>
          ) : (
            <p className="preview-details-text-placeholder">
              <em>Client Name</em>
            </p>
          )}
          {note && (
            <>
              <p className="preview-title">NOTE</p>
              <p className="preview-details-text">{note}</p>
            </>
          )}
          {displayLogo && (
            <img
              className="preview-logo"
              src={displayLogo}
              alt="Company Logo"
            />
          )}
        </div>
        <div className="preview-footer-div">
          <div className="top-footer-div">
            <div className="date-div">
              {isRevision ? <p>Revision Date:</p> : <p>Issued Date:</p>}
              <span className="footer-date"> {date}</span>
              {isRevision && (
                <p className="rev-info">
                  | Rev:
                  <span className="footer-rev-p">
                    {" "}
                    {formatRevisionNumber(revisionNumber)}
                  </span>
                </p>
              )}
            </div>
            <div className="page-number-div">
              {showPageNumbers && (
                <p className="page-number">
                  Page <strong>1</strong> of <strong>5</strong>
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
      <div className="disclaimer-div-content">
        {disclaimer.map(
          (isSelected, index) =>
            isSelected && (
              <p className="disclaimer-text" key={index}>
                {disclaimerTextOptions[index]}
              </p>
            )
        )}
      </div>
    </div>
  )
}

export default StampPreview
