import React from "react"
import PreparedBySelector from "./PreparedBySelector"
import TextInput from "./TextInput"
import Dropdown from "./Dropdown"
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
    date,
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
  } = props

  const disclaimerOptions = [
    { label: "No Disclaimer", value: 0 },
    { label: "Disclaimer 1", value: 1 },
    { label: "Disclaimer 2", value: 2 },
    { label: "Disclaimer 3", value: 3 },
  ]

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
        />
        <TextInput
          label="Job Code"
          value={jobCode}
          placeHolder={"Project Code"}
          onChange={(e) => setJobCode(e.target.value)}
        />
        <TextInput
          label="Prepared For"
          value={preparedFor}
          placeHolder={"Client"}
          onChange={(e) => setPreparedFor(e.target.value)}
        />
        <TextInput
          label="Job Phase"
          value={note}
          placeHolder={"Job Phase"}
          onChange={(e) => setNote(e.target.value)}
        />
        <Dropdown
          label="Disclaimer"
          value={disclaimer}
          placeHolder={"Job Phase"}
          onChange={(e) => setDisclaimer(e.target.value)}
          options={disclaimerOptions}
        />
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
        <URLFolderSelector URLFolder={URLFolder} setURLFolder={setURLFolder} />
      </div>
    </div>
  )
}

export default StampForm
