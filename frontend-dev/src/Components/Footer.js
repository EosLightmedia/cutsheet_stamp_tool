import React from "react"
import EosLogo from "../Assets/eos-logo.png"

function Footer() {
  return (
    <div className="footer-div">
      <div className="footer-content">
        <img src={EosLogo} alt="Eos Logo" className="footer-logo" />
        <p>I am footer</p>
      </div>
    </div>
  )
}

export default Footer
