import React, { useState, useEffect } from "react"

function ProcessingPage({ setIsProcessing }) {
  const [secondsRemaining, setSecondsRemaining] = useState(30)

  useEffect(() => {
    let intervalId

    if (secondsRemaining > 0) {
      intervalId = setInterval(() => {
        setSecondsRemaining((prevSeconds) => prevSeconds - 1)
      }, 1000)
    } else {
      // When countdown reaches 0, stop processing
      setIsProcessing(false)
    }

    // Clear the interval when the component is unmounted or when the countdown is finished
    return () => clearInterval(intervalId)
  }, [secondsRemaining, setIsProcessing]) // Include setIsProcessing in the dependency array

  return (
    <div className="processing-page-div">
      <div className="processing-page-content">
        <h3>Hang Tight</h3>
        <h4>Your cut sheets are being processed...</h4>
        <p className="countdown-timer">{secondsRemaining}</p>
      </div>
    </div>
  )
}

export default ProcessingPage
