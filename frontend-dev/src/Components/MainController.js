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
  const [boxFolder, setBoxFolder] = useState("");
  const [boxFolderNumber, setBoxFolderNumber] = useState("");
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
    const extractFolderNumber = () => {
      const trimmedUrl = boxFolder.trim();
      const match = trimmedUrl.match(/https:\/\/box\.com\/folder\/(\d+)/);
      if (match) {
        setBoxFolderNumber(String(match[1]));
      } else {
        setBoxFolderNumber(undefined);
      }
    };
    if (boxFolder) {
      extractFolderNumber();
    } else {
      setBoxFolderNumber(undefined);
    }
  }, [boxFolder]);

  useEffect(() => {
    const isValidBoxLink = boxFolder.match(/https:\/\/box\.com\/folder\/(\d+)/);
    const areRequiredFieldsFilled =
      jobName && jobCode && preparedFor && jobPhase && isValidBoxLink;

    setCanSubmit(areRequiredFieldsFilled);
  }, [jobName, jobCode, preparedFor, jobPhase, boxFolder]);

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
      folderID: boxFolderNumber,
      projectName: jobName,
      projectNumber: jobCode,
      preparedBy: preparedByNumber,
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
          boxFolder={boxFolder}
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
          boxFolder={boxFolder}
          setBoxFolder={setBoxFolder}
          boxFolderNumber={boxFolderNumber}
          setBoxFolderNumber={setBoxFolderNumber}
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
          boxFolder={boxFolder}
          boxFolderNumber={boxFolderNumber}
          preparedFor={preparedFor}
          preparedBy={preparedBy}
          date={date}
          isRevision={isRevision}
          jobPhase={jobPhase}
          gradientStyle={gradientStyle}
          dateFormat={dateFormat}
          revisionNumber={revisionNumber}
        />
        <StampSubmit onClick={handleSubmit} isActive={canSubmit} />
        <Footer />
      </div>
    </>
  );
}

export default MainController;
