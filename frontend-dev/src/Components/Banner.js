import React, { useState, useEffect } from "react"

const Banner = ({ createdFolderNumber, setBannerIsVisible }) => {
  const [bannerMessage, setBannerMessage] = useState("")
  const initialStyle = {
    transition: "opacity 1s ease", // Transition for the fade-out effect
    opacity: 1, // Start with full opacity
    backgroundColor: "#4CAF50", // Default background color
    color: "#fff", // Default text color
  }
  const [bannerStyle, setBannerStyle] = useState(initialStyle)

  useEffect(() => {
    let fadeOutTimer
    let hideTimer

    if (createdFolderNumber) {
      setBannerMessage(
        <>
          Success! Click{" "}
          <a
            href={`https://eoslightmedia.app.box.com/folder/${createdFolderNumber}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            here
          </a>{" "}
          to find your newly stamped cut sheets on Box.
        </>
      )
      setBannerStyle({ ...bannerStyle, backgroundColor: "#4CAF50" })
    } else {
      setBannerMessage(
        "Uh oh... something went wrong. Please check your folder link and try again."
      )
      setBannerStyle({ ...bannerStyle, backgroundColor: "#F44336" })
    }

    // Start fading out the banner after 10 seconds
    fadeOutTimer = setTimeout(() => {
      setBannerStyle({ ...bannerStyle, opacity: 0 })
    }, 30000)

    // Completely hide the banner after the fade-out animation completes
    hideTimer = setTimeout(() => {
      setBannerIsVisible(false)
    }, 31000) // 1 second longer than the fade-out duration

    // Clean up timers
    return () => {
      clearTimeout(fadeOutTimer)
      clearTimeout(hideTimer)
    }
  }, [createdFolderNumber, setBannerIsVisible])

  return (
    <div className="banner-main-div" style={bannerStyle}>
      <div className="banner-inner-div">
        <p>{bannerMessage}</p>
      </div>
    </div>
  )
}

export default Banner
