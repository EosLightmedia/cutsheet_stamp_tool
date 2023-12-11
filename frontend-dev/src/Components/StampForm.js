import React from "react";
import PreparedBySelector from "./PreparedBySelector";
import TextInput from "./TextInput";
import Dropdown from "./Dropdown";
import DateSelector from "./DateSelector";
import RevisionSelector from "./RevisionSelector";
import DateFormatSelector from "./DateFormatSelector";
import GradientSelector from "./GradientSelector";
import RevisionNumberSelector from "./RevisionNumberSelector";
import URLFolderSelector from "./BoxFolderSelector";
import StampLogo from "../Assets/stamp-logo.png";

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
    jobPhase,
    setJobPhase,
    gradientStyle,
    setGradientStyle,
    dateFormat,
    setDateFormat,
    revisionNumber,
    setRevisionNumber,
  } = props;

  const jobPhaseOptions = [
    { label: "Select One", value: "" },
    { label: "For Bid", value: "For Bid" },
    { label: "For Review", value: "For Review" },
    { label: "Coordination", value: "Coordination" },
  ];

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
        <Dropdown
          label="Job Phase"
          value={jobPhase}
          onChange={(e) => setJobPhase(e.target.value)}
          options={jobPhaseOptions}
        />
        <h2 className="form-section-title">Date</h2>
        <DateSelector selectedDate={date} setSelectedDate={setDate} />
        <DateFormatSelector
          dateFormat={dateFormat}
          setDateFormat={setDateFormat}
        />
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
        <h2 className="form-section-title">Style Settings</h2>
        <GradientSelector
          gradient={gradientStyle}
          setGradient={setGradientStyle}
        />
        <h2 className="form-section-title">Box Details</h2>
        <URLFolderSelector URLFolder={URLFolder} setURLFolder={setURLFolder} />
      </div>
    </div>
  );
}

export default StampForm;
