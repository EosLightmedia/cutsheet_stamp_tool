import React, { useEffect, useState } from "react"
import StampForm from "./StampForm"
import StampPreview from "./StampPreview"
import StampSubmit from "./StampSubmit"
import Footer from "./Footer"
import axios from "axios"

function MainController() {
  const [preparedBy, setPreparedBy] = useState("Eos Lightmedia")
  const [jobName, setJobName] = useState("")
  const [jobCode, setJobCode] = useState("")
  const [URLFolder, setURLFolder] = useState("")
  const [preparedFor, setPreparedFor] = useState("")
  const [date, setDate] = useState("")
  const [isRevision, setIsRevision] = useState(false)
  const [jobPhase, setJobPhase] = useState("")
  const [note, setNote] = useState("")
  const [gradientStyle, setGradientStyle] = useState("No Gradient")
  const [revisionNumber, setRevisionNumber] = useState(0)
  const [showPageNumbers, setShowPageNumbers] = useState(false)
  const [isPackagePDFs, setIsPackagePDFs] = useState(false)
  const [disclaimer, setDisclaimer] = useState(0)
  const [canSubmit, setCanSubmit] = useState(false)

  useEffect(() => {
    const urlRegex =
      /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/
    const isValidLink = urlRegex.test(URLFolder)
    const areRequiredFieldsFilled =
      jobName && jobCode && preparedFor && jobPhase && isValidLink

    setCanSubmit(areRequiredFieldsFilled)
  }, [jobName, jobCode, preparedFor, jobPhase, URLFolder])

  const handleSubmit = () => {
    function extractFolderNumber(url) {
      const regex = /https:\/\/box\.com\/folder\/(\d+)/
      const match = url.match(regex)
      return match ? match[1] : null
    }

    const folderNumber = extractFolderNumber(URLFolder)

    let preparedByNumber
    if (preparedBy === "Eos Lightmedia") {
      preparedByNumber = 0
    } else if (preparedBy === "Abernathy Lighting Design") {
      preparedByNumber = 1
    }

    let gradientNumber
    switch (gradientStyle) {
      case "No Gradient":
        gradientNumber = 0
        break
      case "Purple/Blue":
        gradientNumber = 1
        break
      case "Orange":
        gradientNumber = 2
        break
      default:
        gradientNumber = 0
    }

    const formData = {
      folderID: folderNumber,
      projectName: jobName,
      projectNumber: jobCode,
      preparedBy: preparedByNumber,
      preparedFor: preparedFor,
      date: date,
      note: note,
      isRevision: isRevision,
      revisionNumber: revisionNumber,
      gradient: gradientNumber,
      disclaimer: disclaimer,
      packageSet: isPackagePDFs,
    }

    axios
      .post("/api/stamp", formData)
      .then((response) => {
        console.log("Data submitted successfully:", response.data)
      })
      .catch((error) => {
        console.error("There was an error submitting the form:", error)
      })

    console.log(formData)
  }

  return (
    <>
      <div className="all-app-content">
        <StampForm
          jobName={jobName}
          setJobName={setJobName}
          jobCode={jobCode}
          setJobCode={setJobCode}
          note={note}
          setNote={setNote}
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
          revisionNumber={revisionNumber}
          setRevisionNumber={setRevisionNumber}
          isPackagePDFs={isPackagePDFs}
          setIsPackagePDFs={setIsPackagePDFs}
          showPageNumbers={showPageNumbers}
          setShowPageNumbers={setShowPageNumbers}
          disclaimer={disclaimer}
          setDisclaimer={setDisclaimer}
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
          jobPhase={note}
          gradientStyle={gradientStyle}
          revisionNumber={revisionNumber}
          disclaimer={disclaimer}
          showPageNumbers={showPageNumbers}
        />
        <StampSubmit onClick={handleSubmit} isActive={true} />
        <Footer />
      </div>
    </>
  )
}

export default MainController
