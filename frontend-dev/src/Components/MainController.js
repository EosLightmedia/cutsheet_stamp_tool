import React, { useEffect, useState } from "react";
import StampForm from "./StampForm";
import StampPreview from "./StampPreview";
import StampSubmit from "./StampSubmit";
import Footer from "./Footer";
import ConfirmPopUp from "./ConfirmPopUp";
import axios from "axios";

function MainController() {
  const [preparedBy, setPreparedBy] = useState("Eos Lightmedia");
  const [jobName, setJobName] = useState("");
  const [jobCode, setJobCode] = useState("");
  const [URLFolder, setURLFolder] = useState("");
  const [preparedFor, setPreparedFor] = useState("");
  const initialDate = {
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1,
    day: new Date().getDate(),
  };
  const [date, setDate] = useState(initialDate);
  const [isRevision, setIsRevision] = useState(false);
  const [dateFormat, setDateFormat] = useState("YYYY/MM/DD");
  const [jobPhase, setJobPhase] = useState("");
  const [gradientStyle, setGradientStyle] = useState("No Gradient");
  const [revisionNumber, setRevisionNumber] = useState(0);
  const [canSubmit, setCanSubmit] = useState(false);
  const [showConfirmPopUp, setShowConfirmPopUp] = useState(false);

  useEffect(() => {
    const urlRegex =
      /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/;
    const isValidLink = urlRegex.test(URLFolder);
    const areRequiredFieldsFilled =
      jobName && jobCode && preparedFor && jobPhase && isValidLink;

    setCanSubmit(areRequiredFieldsFilled);
  }, [jobName, jobCode, preparedFor, jobPhase, URLFolder]);

  const formatDateObj = (dateObj) => {
    if (!dateObj || !dateObj.year || !dateObj.month || !dateObj.day) {
      return { year: "", month: "", day: "" };
    }
    return {
      year: dateObj.year,
      month: dateObj.month,
      day: dateObj.day,
    };
  };

  const handleSubmit = () => {
    const formattedDate = formatDateObj(date);

    let preparedByNumber;
    if (preparedBy === "Eos Lightmedia") {
      preparedByNumber = 0;
    } else if (preparedBy === "Abernathy Lighting Design") {
      preparedByNumber = 1;
    }

    let dateFormatNumber;
    switch (dateFormat) {
      case "YYYY/MM/DD":
        dateFormatNumber = 0;
        break;
      case "MM/DD/YYYY":
        dateFormatNumber = 1;
        break;
      case "DD/MM/YYYY":
        dateFormatNumber = 2;
        break;
      default:
        dateFormatNumber = -1;
    }

    let jobPhaseNumber;
    switch (jobPhase) {
      case "For Bid":
        jobPhaseNumber = 0;
        break;
      case "For Review":
        jobPhaseNumber = 1;
        break;
      case "Coordination":
        jobPhaseNumber = 2;
        break;
      default:
        jobPhaseNumber = -1;
    }

    let gradientNumber;
    switch (gradientStyle) {
      case "No Gradient":
        gradientNumber = 0;
        break;
      case "Purple/Blue":
        gradientNumber = 1;
        break;
      case "Orange":
        gradientNumber = 2;
        break;
      default:
        gradientNumber = 0;
    }

    const formData = {
      URL: URLFolder,
      projectName: jobName,
      projectNumber: jobCode,
      preparedBy: preparedByNumber,
      preparedFor: preparedFor,
      date: formattedDate,
      dateFormat: dateFormatNumber,
      isRevision: isRevision,
      revisionNumber: revisionNumber,
      jobPhase: jobPhaseNumber,
      gradient: gradientNumber,
    };

    axios
      .post("/post-stamp", formData)
      .then((response) => {
        console.log("Data submitted successfully:", response.data);
      })
      .catch((error) => {
        console.error("There was an error submitting the form:", error);
      });

    console.log(formData);
  };

  const showPopUp = () => {
    setShowConfirmPopUp(true);
  };

  const hidePopUp = () => {
    setShowConfirmPopUp(false);
  };

  return (
    <>
      {showConfirmPopUp && (
        <ConfirmPopUp
          jobName={jobName}
          jobCode={jobCode}
          URLFolder={URLFolder}
          preparedFor={preparedFor}
          preparedBy={preparedBy}
          date={date}
          isRevision={isRevision}
          jobPhase={jobPhase}
          gradientStyle={gradientStyle}
          dateFormat={dateFormat}
          revisionNumber={revisionNumber}
          hidePopUp={hidePopUp}
          handleSubmit={handleSubmit}
        />
      )}
      <div className="all-app-content">
        <StampForm
          jobName={jobName}
          setJobName={setJobName}
          jobCode={jobCode}
          setJobCode={setJobCode}
          URLFolder={URLFolder}
          setURLFolder={setURLFolder}
          preparedFor={preparedFor}
          setPreparedFor={setPreparedFor}
          preparedBy={preparedBy}
          setPreparedBy={setPreparedBy}
          date={date}
          setDate={setDate}
          isRevision={isRevision}
          setIsRevision={setIsRevision}
          jobPhase={jobPhase}
          setJobPhase={setJobPhase}
          gradientStyle={gradientStyle}
          setGradientStyle={setGradientStyle}
          dateFormat={dateFormat}
          setDateFormat={setDateFormat}
          revisionNumber={revisionNumber}
          setRevisionNumber={setRevisionNumber}
        />
        <StampPreview
          jobName={jobName}
          jobCode={jobCode}
          URLFolder={URLFolder}
          setURLFolder={setURLFolder}
          preparedFor={preparedFor}
          preparedBy={preparedBy}
          date={date}
          isRevision={isRevision}
          jobPhase={jobPhase}
          gradientStyle={gradientStyle}
          dateFormat={dateFormat}
          revisionNumber={revisionNumber}
        />
        <StampSubmit onClick={handleSubmit} isActive={true} />
        <Footer />
      </div>
    </>
  );
}

export default MainController;
