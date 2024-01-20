import React from "react"

const PDFChecker = ({ name, hasIssues }) => {
  const hasUnderscore = name.includes("_")
  const extractedType = hasUnderscore
    ? name.split("_")[0]
    : name.replace(".pdf", "")
  const isLongName = extractedType.length > 15
  const warningIcon = !hasUnderscore || isLongName ? "⚠️ " : ""

  const textStyle = hasIssues ? { color: "red", fontWeight: "bold" } : {}

  return (
    <div className="pdf-listed-files">
      <p style={textStyle}>{name}</p>
      <p style={textStyle}>
        {warningIcon}
        {extractedType}
      </p>
    </div>
  )
}

export default PDFChecker
