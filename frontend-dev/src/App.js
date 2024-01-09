import React, { useEffect, useState } from "react"
import MainController from "./Components/MainController"
import LoadingImage from "./Assets/loading-spinner.gif"
import "./App.css"

function App() {
  const [authCode, setAuthCode] = useState("")

  useEffect(() => {
    const cookieName = "auth_code"
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${cookieName}=`)
    if (parts.length === 2) {
      const code = parts.pop().split(";").shift()
      setAuthCode(code)
    }
  }, [])

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
