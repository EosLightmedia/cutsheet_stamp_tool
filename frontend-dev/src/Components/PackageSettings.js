import React from "react"

const PackageSettings = ({ isPackagePDFs, setIsPackagePDFs }) => {
  return (
    <div className="text-input-container">
      <label className="selector-label-input-package">Package PDFs?</label>
      <div>
        <div className="button-group-package">
          <button
            onClick={() => setIsPackagePDFs(false)}
            className={!isPackagePDFs ? "selected" : ""}
          >
            No
          </button>
          <button
            onClick={() => setIsPackagePDFs(true)}
            className={isPackagePDFs ? "selected" : ""}
          >
            Yes
          </button>
        </div>
        <div className="helper-text-package-div">
          {isPackagePDFs ? (
            <p className="helper-text-package">
              All PDFs will be packaged into a single document.
            </p>
          ) : (
            <p className="helper-text-package">
              PDFs will be stamped individually.
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

export default PackageSettings
