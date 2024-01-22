import React from "react"

const PageNumberSelector = ({
  showPageNumbers,
  isPackagePDFs,
  setShowPageNumbers,
}) => {
  const getHelperText = () => {
    if (showPageNumbers) {
      if (isPackagePDFs) {
        return "All PDFs will be packaged into a single document with page numbers."
      } else {
        return "Each individual PDF will be stamped with page numbers."
      }
    } else {
      return "No page numbers will be stamped."
    }
  }

  return (
    <div className="text-input-container">
      <label className="selector-label-input-package">Number Pages?</label>
      <div>
        <div className="button-group-package">
          <button
            onClick={() => setShowPageNumbers(true)}
            className={showPageNumbers ? "selected" : ""}
          >
            Yes
          </button>
          <button
            onClick={() => setShowPageNumbers(false)}
            className={!showPageNumbers ? "selected" : ""}
          >
            No
          </button>
        </div>
        <div className="helper-text-package-div">
          <p className="helper-text-package">{getHelperText()}</p>
        </div>
      </div>
    </div>
  )
}

export default PageNumberSelector
