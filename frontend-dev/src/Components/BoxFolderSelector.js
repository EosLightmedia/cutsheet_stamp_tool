import React, { useState } from "react"
import axios from "axios"
import mockData from "../Data/mockData.json"

function URLFolderSelector({ URLFolder, setURLFolder, setFoundPDFs }) {
  const defaultHelperText =
    "Paste Box link here (e.g. https://eoslightmedia.app.box.com/folder/240776517305)"
  const [helperText, setHelperText] = useState(defaultHelperText)

  const fetchFolderData = async (folderNumber) => {
    setHelperText("Fetching folder data...") // Indicate loading before starting the fetch

    // Check if the environment is development
    if (process.env.NODE_ENV === "development") {
      // Simulate a delay to mimic network request
      setTimeout(() => {
        const pdfs = mockData.items.filter((item) => item.type === "pdf")
        setFoundPDFs(pdfs)
        setHelperText(`Path: ${mockData.path}`)
      }, 1000) // Simulate a fetch delay
    } else {
      // This block will run in production
      try {
        const response = await axios.get(`/api/folder/${folderNumber}`)
        const { items, path } = response.data
        const pdfs = items.filter((item) => item.type === "pdf")
        setFoundPDFs(pdfs)
        setHelperText(`Path: ${path}`)
      } catch (error) {
        setHelperText("Error fetching folder data.")
        console.error("Error fetching folder data:", error)
      }
    }
  }

  const validateFolderLink = (inputUrl) => {
    setURLFolder(inputUrl)
    setHelperText("Fetching folder data...") // Set this early to indicate loading

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
      <p className="helper-text">{helperText}</p>
    </div>
  )
}

export default URLFolderSelector
