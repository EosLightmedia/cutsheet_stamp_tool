import React, { useEffect, useState } from "react"
import StampForm from "./StampForm"
import StampPreview from "./StampPreview"
import StampSubmit from "./StampSubmit"
import ProcessingPage from "./ProcessingPage"
import ConfirmPopUp from "./ConfirmPopUp"
import Banner from "./Banner"
import Footer from "./Footer"
import axios from "axios"

function MainController({ authCode, refresh }) {
  const [preparedBy, setPreparedBy] = useState("Eos Lightmedia")
  const [jobName, setJobName] = useState("")
  const [jobCode, setJobCode] = useState("")
  const [URLFolder, setURLFolder] = useState("")
  const [preparedFor, setPreparedFor] = useState("")
  const [date, setDate] = useState("")
  const [isRevision, setIsRevision] = useState(false)
  const [jobPhase, setJobPhase] = useState("")
  const [note, setNote] = useState("")
  const [gradientStyle, setGradientStyle] = useState(true)
  const [revisionNumber, setRevisionNumber] = useState(0)
  const [showPageNumbers, setShowPageNumbers] = useState(true)
  const [isPackagePDFs, setIsPackagePDFs] = useState(true)
  const [disclaimer, setDisclaimer] = useState([false, false, false])
  const [createdFolderNumber, setCreatedFolderNumber] = useState()
  const [foundPDFs, setFoundPDFs] = useState([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [bannerIsVisible, setBannerIsVisible] = useState(false)
  const [confirmPopUpIsVisible, setConfirmPopUpIsVisible] = useState(false)
  const [folderPath, setFolderPath] = useState("")
  const [canSubmit, setCanSubmit] = useState(false)

  const openPopup = () => {
    document.body.classList.add("no-scroll")
    setConfirmPopUpIsVisible(true)
  }

  const closePopup = () => {
    document.body.classList.remove("no-scroll")
    setConfirmPopUpIsVisible(false)
  }

  useEffect(() => {
    const urlRegex =
      /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/
    const isValidLink = urlRegex.test(URLFolder)
    const areRequiredFieldsFilled =
      jobName && jobCode && preparedFor && jobPhase && isValidLink
    setCanSubmit(areRequiredFieldsFilled)
  }, [jobName, jobCode, preparedFor, jobPhase, URLFolder])

  const handleSubmit = () => {
    closePopup()
    setIsProcessing(true)
    function extractFolderNumber(url) {
      const regex = /https:\/\/eoslightmedia\.app\.box\.com\/folder\/(\d+)/
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

    const formData = {
      folderID: folderNumber,
      projectName: jobName,
      projectNumber: jobCode,
      preparedBy: preparedByNumber,
      preparedFor: preparedFor,
      date: date,
      note: note,
      isRevision: isRevision,
      showPageNumbers: showPageNumbers,
      revisionNumber: revisionNumber,
      isGradient: gradientStyle,
      disclaimer: disclaimer,
      packageSet: isPackagePDFs,
    }

    console.log("Form Data:", formData)

    axios
      .post(`/api/stamp/?access=${authCode}&refresh=${refresh}`, formData)
      .then((response) => {
        console.log("Newly Created Folder:", response.data)
        setCreatedFolderNumber(response.data)
        setIsProcessing(false)
        setBannerIsVisible(true)
      })
      .catch((error) => {
        console.error("There was an error submitting the form:", error)
        setIsProcessing(false)
        setBannerIsVisible(true)
      })
  }

  return (
    <>
      {confirmPopUpIsVisible && (
        <ConfirmPopUp
          jobName={jobName}
          jobCode={jobCode}
          preparedBy={preparedBy}
          preparedFor={preparedFor}
          date={date}
          isRevision={isRevision}
          note={note}
          revisionNumber={revisionNumber}
          handleSubmit={handleSubmit}
          closePopup={closePopup}
          isPackagePDFs={isPackagePDFs}
          foundPDFs={foundPDFs}
          folderPath={folderPath}
        />
      )}
      {isProcessing && <ProcessingPage setIsProcessing={setIsProcessing} />}
      {bannerIsVisible && (
        <Banner
          createdFolderNumber={createdFolderNumber}
          setBannerIsVisible={setBannerIsVisible}
        />
      )}
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
          foundPDFs={foundPDFs}
          setFoundPDFs={setFoundPDFs}
          setFolderPath={setFolderPath}
          authCode={authCode}
          refresh={refresh}
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
        <StampSubmit isActive={true} openPopup={openPopup} />

        <Footer />
      </div>
    </>
  )
}

export default MainController
