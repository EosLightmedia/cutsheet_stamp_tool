import React, { useEffect, useState } from "react"
import MainController from "./Components/MainController"
import LoadingImage from "./Assets/loading-spinner.gif"
import "./App.css"

function App() {
  const [authCode, setAuthCode] = useState("")

  useEffect(() => {
    const interval = setInterval(() => {
      const cookieName = "auth_code"
      const value = `; ${document.cookie}`
      const parts = value.split(`; ${cookieName}=`)
      if (parts.length === 2) {
        const code = parts.pop().split(";").shift()
        if (code !== authCode) {
          setAuthCode(code)
          clearInterval(interval) // Stop checking once the code is found
        }
      }
    }, 1000) // Check every 1000 milliseconds (1 second)

    return () => clearInterval(interval) // Clean up the interval on unmount
  }, [authCode])

  useEffect(() => {
    if (authCode) {
      console.log("Auth Code:", authCode)
    }
  }, [authCode])

  return (
    <div className="center-container">
      {authCode ? (
        <MainController authCode={authCode} />
      ) : (
        <div className="loading-container">
          <img
            className="loading-spinner"
            src={LoadingImage}
            alt="Loading..."
          />
          <p>Verifying Box Credentials...</p>
        </div>
      )}
    </div>
  )
}

export default App
