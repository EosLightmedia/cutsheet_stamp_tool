import React, { useState } from "react";

function BoxFolderSelector({ boxFolder, setBoxFolder }) {
  const defaultHelperText =
    "Copy and paste the Box folder link (e.g., https://box.com/folder/12345)";
  const [helperText, setHelperText] = useState(defaultHelperText);

  const validateBoxFolderLink = (inputUrl) => {
    setBoxFolder(inputUrl);

    if (inputUrl === "") {
      setHelperText(defaultHelperText);
      return;
    }
    const isValidFormat = /^https:\/\/box\.com\/folder\/\d+$/.test(inputUrl);
    if (isValidFormat) {
      setHelperText("Box link looks good! Nice work!");
    } else {
      setHelperText("Hmmm, something about that link doesn’t look right...");
    }
  };

  const handleChange = (event) => {
    const inputUrl = event.target.value;
    validateBoxFolderLink(inputUrl);
  };

  return (
    <div className="box-folder-selector-container">
      <label htmlFor="box-folder-url" className="input-label">
        Box Folder URL:
      </label>
      <input
        type="text"
        id="box-folder-url"
        className="text-input"
        value={boxFolder}
        onChange={handleChange}
        placeholder="https://box.com/folder/12345"
      />
      <p className="helper-text">{helperText}</p>
    </div>
  );
}

export default BoxFolderSelector;
