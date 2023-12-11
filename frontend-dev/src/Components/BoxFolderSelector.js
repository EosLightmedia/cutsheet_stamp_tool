import React, { useState } from "react";

function URLFolderSelector({ URLFolder, setURLFolder }) {
  const defaultHelperText =
    "Copy and paste the link (e.g., https://example.com/resource)";
  const [helperText, setHelperText] = useState(defaultHelperText);

  const validateFolderLink = (inputUrl) => {
    setURLFolder(inputUrl);

    if (inputUrl === "") {
      setHelperText(defaultHelperText);
      return;
    }
    const isValidFormat =
      /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/.test(
        inputUrl
      );
    if (isValidFormat) {
      setHelperText("Link looks good! Nice work!");
    } else {
      setHelperText("Hmmm, something about that link doesn’t look right...");
    }
  };

  const handleChange = (event) => {
    const inputUrl = event.target.value;
    validateFolderLink(inputUrl);
  };

  return (
    <div className="box-folder-selector-container">
      <label htmlFor="box-folder-url" className="input-label">
        URL:
      </label>
      <input
        type="text"
        id="box-folder-url"
        className="text-input"
        value={URLFolder}
        onChange={handleChange}
        placeholder="https://example.com/resource"
      />
      <p className="helper-text">{helperText}</p>
    </div>
  );
}

export default URLFolderSelector;
