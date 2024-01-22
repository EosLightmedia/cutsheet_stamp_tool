import React, { useState } from "react"
import axios from "axios"
import mockData from "../Data/mockData.json"
import LoadingSpinner from "../Assets/loading-spinner.gif"

function BoxFolderSelector({
  URLFolder,
  setURLFolder,
  setFoundPDFs,
  setFolderPath,
  setTypeArray,
  authCode,
  refresh,
}) {
  const defaultHelperText =
    "Paste Box link here (e.g. https://eoslightmedia.app.box.com/folder/240776517305)"
  const [helperText, setHelperText] = useState(defaultHelperText)
  const loadingMessage = "Fetching folder data..."

  const fetchFolderData = async (folderNumber) => {
    setHelperText(loadingMessage)

    // Common function to process the response and set helper text
    const processResponse = (items, path) => {
      const pdfs = items.filter((item) => item.type === "pdf")
      const pdfNames = pdfs.map((pdf) => pdf.name)
      setTypeArray(pdfNames)
      setFoundPDFs(pdfs)
      setFolderPath(path)

      // Find PDFs that don't have an underscore and are longer than 15 characters
      const problematicPDFs = pdfs.filter(
        (pdf) => !pdf.name.includes("_") && pdf.name.length - 4 > 15
      )

      // Construct the helper text with potential issues
      const issueText =
        problematicPDFs.length > 0 ? (
          <>
            <br />
            <p className="issue-alert">⚠️ Possible file naming issues found:</p>
            <ul className="issue-list">
              {problematicPDFs.map((pdf) => (
                <li key={pdf.name}>{pdf.name}</li>
              ))}
            </ul>
            <p className="info-helper-text">
              <strong>
                {" "}
                ℹ️ "Type" is determined by the text before the first underscore
                "_" in the file name and should not exceed 15 characters.
              </strong>
            </p>
          </>
        ) : null

      setHelperText(
        <div className="helper-text-block">
          <p className="success-helper-p">
            ✅ Box folder found containing <strong>{pdfs.length}</strong> PDFs!
          </p>
          <p>
            📁 <strong>{path}</strong>{" "}
          </p>
          {issueText}
        </div>
      )
    }

    if (process.env.NODE_ENV === "development") {
      setTimeout(() => {
        processResponse(mockData.items, mockData.path)
      }, 1000)
    } else {
      try {
        const response = await axios.get(
          `/api/folder/?folder_id=${folderNumber}&access=${authCode}&refresh=${refresh}`
        )
        processResponse(response.data.items, response.data.path)
      } catch (error) {
        setHelperText(
          "❌ Error fetching folder data. You might not have permission or the folder doesn't exist."
        )
        console.error("❌ Error fetching folder data:", error)
      }
    }
  }

  const validateFolderLink = (inputUrl) => {
    setURLFolder(inputUrl)
    setHelperText("❌ Fetching folder data...")

    if (inputUrl === "") {
      setHelperText(defaultHelperText)
      return
    }

    const regex = /^(https?:\/\/)?eoslightmedia.app.box.com\/folder\/(\d+)$/
    const match = inputUrl.match(regex)

    if (match && match[2]) {
      fetchFolderData(match[2])
    } else {
      setHelperText("Hmmm, something about that link doesn’t look right...")
    }
  }

  const handleChange = (event) => {
    const inputUrl = event.target.value
    validateFolderLink(inputUrl)
  }

  return (
    <div className="box-folder-selector-container">
      <label htmlFor="box-folder-url" className="input-label">
        Box Folder Link:
      </label>
      <input
        type="text"
        id="box-folder-url"
        className="text-input"
        value={URLFolder}
        onChange={handleChange}
        placeholder="https://eoslightmedia.app.box.com/folder/240776517305"
      />
      <div className="box-helper-text">
        {helperText === loadingMessage && (
          <img
            src={LoadingSpinner}
            className="loading-spinner-small"
            alt="Loading"
            style={{ width: "15px", marginRight: "5px", marginTop: "-1px" }}
          />
        )}
        {helperText}
      </div>
    </div>
  )
}

export default BoxFolderSelector
