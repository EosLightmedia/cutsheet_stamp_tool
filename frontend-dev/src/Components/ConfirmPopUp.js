import React from "react"
import PDFChecker from "./PDFChecker"

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

  return (
    <div className="confirm-pop-up">
      <div className="confirm-popup-main-div">
        <div className="confirm-popup-content">
          <h2>Just to confirm...</h2>
          <p className="main-prompt">
            You want to stamp the PDFs in this Box folder:
          </p>
          <p className="folder-path-text">{folderPath}</p>
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
            <div className="pdf-listed-files">
              <p>
                <strong>PDF File</strong>
              </p>
              <p>
                <strong>Extracted Type Name</strong>
              </p>
            </div>
            {foundPDFs.map((pdf, index) => (
              <PDFChecker key={index} name={pdf.name} type={pdf.type} />
            ))}
          </div>
          <div className="confirm-buttons">
            <button onClick={() => closePopup()}>CANCEL</button>
            <button onClick={handleSubmit}>YES, STAMP AWAY</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ConfirmPopUp
