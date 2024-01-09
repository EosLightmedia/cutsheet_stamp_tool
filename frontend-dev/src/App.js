import React, { useEffect, useState } from "react"
import MainController from "./Components/MainController"
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

  // Separate useEffect to log authCode when it changes
  useEffect(() => {
    if (authCode) {
      console.log("Auth Code:", authCode)
    }
  }, [authCode]) // This useEffect runs whenever authCode changes

  return (
    <div className="center-container">
      <MainController authCode={authCode} />
    </div>
  )
}

export default App
