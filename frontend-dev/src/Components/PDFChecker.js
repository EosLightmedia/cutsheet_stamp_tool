import React from "react"

const PDFChecker = ({ name }) => {
  const hasUnderscore = name.includes("_")
  const extractedType = hasUnderscore ? name.split("_")[0] : name
  const warningIcon = !hasUnderscore ? "⚠️" : ""

  return (
    <div className="pdf-listed-files">
      <p>{name}</p>
      <p>
        {extractedType} {warningIcon}
      </p>
    </div>
  )
}

export default PDFChecker
