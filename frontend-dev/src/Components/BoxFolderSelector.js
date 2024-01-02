import React, { useState } from "react"

function URLFolderSelector({ URLFolder, setURLFolder }) {
  const defaultHelperText =
    "Paste Box link here (e.g. https://eoslightmedia.app.box.com/folder/240776517305)"
  const [helperText, setHelperText] = useState(defaultHelperText)

  const validateFolderLink = (inputUrl) => {
    setURLFolder(inputUrl)

    if (inputUrl === "") {
      setHelperText(defaultHelperText)
      return
    }
    const isValidFormat =
      /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/.test(
        inputUrl
      )
    if (isValidFormat) {
      setHelperText("Link looks good! Nice work!")
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
