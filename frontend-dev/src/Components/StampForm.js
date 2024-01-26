import React from "react"
import PreparedBySelector from "./PreparedBySelector"
import TextInput from "./TextInput"
import Disclaimer from "./Disclaimer"
import DateSelector from "./DateSelector"
import RevisionSelector from "./RevisionSelector"
import GradientSelector from "./GradientSelector"
import RevisionNumberSelector from "./RevisionNumberSelector"
import URLFolderSelector from "./BoxFolderSelector"
import PackageSettings from "./PackageSettings"
import PageNumberSelector from "./PageNumberSelector"
import StampLogo from "../Assets/stamp-logo.png"

function StampForm(props) {
  const {
    jobName,
    setJobName,
    jobCode,
    setJobCode,
    URLFolder,
    setURLFolder,
    preparedFor,
    setPreparedFor,
    preparedBy,
    setPreparedBy,
    setDate,
    isRevision,
    setIsRevision,
    gradientStyle,
    setGradientStyle,
    note,
    setNote,
    revisionNumber,
    setRevisionNumber,
    isPackagePDFs,
    setIsPackagePDFs,
    disclaimer,
    setDisclaimer,
    showPageNumbers,
    setShowPageNumbers,
    foundPDFs,
    setFoundPDFs,
    setFolderPath,
    setTypeArray,
  } = props

  return (
    <div className="content-div form-container">
      <img src={StampLogo} alt="Stamp Logo" className="centered-logo" />
      <h1>Eos Cut Sheet Stamper</h1>
      <div className="form-content">
        <PreparedBySelector value={preparedBy} setValue={setPreparedBy} />
        <h2 className="form-section-title">Job Details</h2>
        <TextInput
          label="Job Name"
          value={jobName}
          placeHolder={"Project Name"}
          onChange={(e) => setJobName(e.target.value)}
          optionalOrRequired={true}
          optionalOrRequiredText="Required Field"
          id={"job-name-input"}
          name={"job-name-input"}
        />
        <TextInput
          label="Job Code"
          value={jobCode}
          placeHolder={"Project Code"}
          onChange={(e) => setJobCode(e.target.value)}
          optionalOrRequired={true}
          optionalOrRequiredText="Required Field"
          id={"job-code-input"}
          name={"job-code-input"}
        />
        <TextInput
          label="Prepared For"
          value={preparedFor}
          placeHolder={"Client"}
          onChange={(e) => setPreparedFor(e.target.value)}
          optionalOrRequired={true}
          optionalOrRequiredText="Required Field"
          id={"prepared-for-input"}
          name={"prepared-for-input"}
        />
        <TextInput
          label="Note"
          value={note}
          placeHolder={"Add a custom note"}
          onChange={(e) => setNote(e.target.value)}
          optionalOrRequired={false}
          optionalOrRequiredText="Optional Field"
          id={"note-input"}
          name={"note-input"}
        />
        <Disclaimer disclaimer={disclaimer} setDisclaimer={setDisclaimer} />
        <h2 className="form-section-title">Date</h2>
        <DateSelector setSelectedDate={setDate} />
        <div className="revision-section">
          <h2 className="form-section-title">Revision</h2>
          <div className="revision-controls">
            <RevisionSelector
              isRevision={isRevision}
              setIsRevision={setIsRevision}
            />
            {isRevision && (
              <RevisionNumberSelector
                revisionNumber={revisionNumber}
                setRevisionNumber={setRevisionNumber}
              />
            )}
          </div>
        </div>
        <h2 className="form-section-title">Package Settings</h2>
        <PackageSettings
          isPackagePDFs={isPackagePDFs}
          setIsPackagePDFs={setIsPackagePDFs}
        />
        <PageNumberSelector
          showPageNumbers={showPageNumbers}
          isPackagePDFs={isPackagePDFs}
          setShowPageNumbers={setShowPageNumbers}
        />
        <GradientSelector
          gradient={gradientStyle}
          setGradient={setGradientStyle}
        />
        <h2 className="form-section-title">Box Details</h2>
        <URLFolderSelector
          URLFolder={URLFolder}
          setURLFolder={setURLFolder}
          foundPDFs={foundPDFs}
          setFoundPDFs={setFoundPDFs}
          setFolderPath={setFolderPath}
          setTypeArray={setTypeArray}
        />
      </div>
    </div>
  )
}

export default StampForm
