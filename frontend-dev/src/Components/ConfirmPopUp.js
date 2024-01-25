import React from "react"
import PDFChecker from "./PDFChecker"
import StampIcon from "../Assets/stamp-icon.png"

function ConfirmPopUp({
  jobName,
  jobCode,
  preparedFor,
  preparedBy,
  date,
  isRevision,
  note,
  revisionNumber,
  isPackagePDFs,
  foundPDFs,
  folderPath,
  handleSubmit,
  closePopup,
}) {
  let company
  // let disclaimer = [true, true, true]

  if (preparedBy === 0) {
    company = "Eos Lightmedia"
  } else {
    company = "Abernathy Lighting Design"
  }

  const problematicPDFs = foundPDFs.filter((pdf) => {
    const nameWithoutExtension = pdf.name.replace(".pdf", "")
    return (
      !nameWithoutExtension.includes("_") ||
      nameWithoutExtension.split("_")[0].length > 15
    )
  })

  const normalPDFs = foundPDFs.filter((pdf) => !problematicPDFs.includes(pdf))

  const sortedPDFs = [...problematicPDFs, ...normalPDFs] // First problematic, then normal PDFs

  return (
    <div className="confirm-pop-up">
      <button
        className="close-button-big"
        onClick={() => closePopup()}
      ></button>
      <div className="confirm-popup-main-div">
        <div className="confirm-popup-content">
          <h2>Confirm Details Before Stamping</h2>

          <div className="confirm-details">
            <p>
              <span className="confirm-title">Job Name:</span> <br />
              <span className="value">{jobName}</span>
            </p>
            <p>
              <span className="confirm-title">Job Code:</span> <br />{" "}
              <span className="value">{jobCode}</span>
            </p>

            <p>
              <span className="confirm-title">Prepared For:</span> <br />{" "}
              <span className="value">{preparedFor}</span>
            </p>
            <p>
              <span className="confirm-title">Date:</span> <br />{" "}
              <span className="value">{date}</span>
            </p>

            <p>
              <span className="confirm-title">Prepared By:</span> <br />{" "}
              <span className="value">{company}</span>
            </p>
            <p>
              <span className="confirm-title">Note:</span> <br />{" "}
              <span className="value">{note}</span>
            </p>

            <p>
              <span className="confirm-title">Revision?</span> <br />{" "}
              {isRevision ? (
                <>
                  <span className="value">Revision #{revisionNumber}</span>
                </>
              ) : (
                <>
                  <span className="value">This is not a revision</span>
                </>
              )}
            </p>
            <p>
              <span className="confirm-title">Package PDFs?</span> <br />{" "}
              {isPackagePDFs ? (
                <>
                  <span className="value">PDFs will be packaged</span>
                </>
              ) : (
                <>
                  <span className="value">Will be stamped individually</span>
                </>
              )}
            </p>
          </div>
          <div className="listed-files-div">
            <div className="pdf-listed-files-title">
              <p className="confirm-title">PDF Files</p>
              <p className="confirm-title">Extracted Type Name</p>
            </div>

            {sortedPDFs.map((pdf, index) => (
              <PDFChecker
                key={index}
                name={pdf.name}
                hasIssues={problematicPDFs.includes(pdf)} // Pass true if PDF is problematic
              />
            ))}
          </div>
          <div className="confirm-buttons">
            <button onClick={() => closePopup()}>CANCEL</button>
            <button onClick={handleSubmit}>
              {" "}
              <img src={StampIcon} className="stamp-icon" alt="Stamp Icon" />
              YES, STAMP AWAY
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ConfirmPopUp
