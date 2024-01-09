import React, { useEffect, useState } from "react"
import MainController from "./Components/MainController"
import "./App.css"

function App() {
  const [authCode, setAuthCode] = useState("")

  useEffect(() => {
    const cookieName = "auth_code" // Replace with your cookie's name
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${cookieName}=`)
    if (parts.length === 2) {
      setAuthCode(parts.pop().split(";").shift())
    }
    console.log("Auth Code:", authCode)
  }, [])

  return (
    <div className="center-container">
      <MainController authCode={authCode} />
    </div>
  )
}

export default App
