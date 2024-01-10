import React, { useState } from "react"
import axios from "axios"
import mockData from "../Data/mockData.json"
import LoadingSpinner from "../Assets/loading-spinner.gif"

function URLFolderSelector({
  URLFolder,
  setURLFolder,
  setFoundPDFs,
  setFolderPath,
  authCode,
}) {
  const defaultHelperText =
    "Paste Box link here (e.g. https://eoslightmedia.app.box.com/folder/240776517305)"
  const [helperText, setHelperText] = useState(defaultHelperText)
  const loadingMessage = "Fetching folder data..."

  const fetchFolderData = async (folderNumber) => {
    setHelperText(loadingMessage) // Indicate loading before starting the fetch

    // Check if the environment is development
    if (process.env.NODE_ENV === "development") {
      setTimeout(() => {
        const pdfs = mockData.items.filter((item) => item.type === "pdf")
        setFoundPDFs(pdfs)
        setFolderPath(mockData.path)
        setHelperText(
          <div className="helper-text-block">
            <>✅ Box folder found!</>
            <br />
            <>📁 {mockData.path}</>
            <br />
            <>📄 Total PDFs: </> <>{pdfs.length}</>
          </div>
        )
      }, 1000)
    } else {
      try {
        const response = await axios.get(
          `/api/folder/?folder_id=${folderNumber}&auth_code=${authCode}`
        )
        const { items, path } = response.data
        const pdfs = items.filter((item) => item.type === "pdf")
        setFoundPDFs(pdfs)
        setFolderPath(path)
        setHelperText(
          <div className="helper-text-block">
            <>✅ Box folder found!</>
            <br />
            <>📁 {path}</>
            <br />
            <>📄 Total PDFs: </> <>{pdfs.length}</>
          </div>
        )
      } catch (error) {
        setHelperText("❌ Error fetching folder data.")
        console.error("❌ Error fetching folder data:", error)
      }
    }
  }

  console.log("Auth Code BoxFolderSelector:", authCode)

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
      <p className="box-helper-text">
        {helperText === loadingMessage && (
          <img
            src={LoadingSpinner}
            className="loading-spinner-small"
            alt="Loading"
            style={{ width: "15px", marginRight: "5px", marginTop: "-1px" }}
          />
        )}

        {helperText}
      </p>
    </div>
  )
}

export default URLFolderSelector
