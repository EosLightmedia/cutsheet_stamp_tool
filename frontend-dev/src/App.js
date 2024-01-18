import React, { useEffect, useState } from "react"
import MainController from "./Components/MainController"
import LoadingImage from "./Assets/loading-spinner.gif"
import "./App.css"

function App() {
  const [authCode, setAuthCode] = useState("")
  const [refreshToken, setRefreshToken] = useState("")

  useEffect(() => {
    if (process.env.NODE_ENV === "development") {
      // Set arbitrary values in development environment
      setAuthCode("dev-auth-code")
      setRefreshToken("dev-refresh-token")
      // console.log(
      //   "Development mode: Using arbitrary Auth Code and Refresh Token."
      // )
    } else {
      // Function to check and set cookie values
      const checkAndSetCookie = (cookieName, setState) => {
        const value = `; ${document.cookie}`
        const parts = value.split(`; ${cookieName}=`)
        if (parts.length === 2) {
          const code = parts.pop().split(";").shift()
          setState(code)
        }
      }

      // Polling intervals for authCode and refreshToken
      const intervalAuth = setInterval(() => {
        checkAndSetCookie("access", setAuthCode)
      }, 1000)

      const intervalRefresh = setInterval(() => {
        checkAndSetCookie("refresh", setRefreshToken)
      }, 1000)

      // Clean up the intervals on unmount
      return () => {
        clearInterval(intervalAuth)
        clearInterval(intervalRefresh)
      }
    }
  }, [])

  // useEffect(() => {
  //   if (authCode) {
  //     console.log("Auth Code:", authCode)
  //   }
  // }, [authCode])

  // useEffect(() => {
  //   if (refreshToken) {
  //     console.log("Refresh Token:", refreshToken)
  //   }
  // }, [refreshToken])

  return (
    <div className="center-container">
      {authCode && refreshToken ? (
        <MainController authCode={authCode} refresh={refreshToken} />
      ) : (
        <div className="center-container-app">
          <div className="loading-container-app">
            <img
              className="loading-spinner"
              src={LoadingImage}
              alt="Loading..."
            />
            <p>Verifying Box Credentials...</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
