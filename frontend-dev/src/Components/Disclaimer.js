import React from "react"

const Disclaimer = ({ disclaimer, setDisclaimer }) => {
  const handleOptionChange = (index) => {
    if (index === -1) {
      setDisclaimer(disclaimer.map(() => false))
    } else {
      const updatedDisclaimer = disclaimer.map((item, idx) =>
        idx === index ? !item : item
      )
      setDisclaimer(updatedDisclaimer)
    }
  }

  const isNoDisclaimerSelected = disclaimer.every((item) => !item)

  return (
    <div className="disclaimer-container">
      <label className="input-label">Disclaimer</label>
      <div className="disclaimer-options">
        <label>
          <input
            type="checkbox"
            value="No Disclaimer"
            checked={isNoDisclaimerSelected}
            onChange={() => handleOptionChange(-1)}
          />
          No Disclaimer
        </label>
        <label>
          <input
            type="checkbox"
            value="Disclaimer 1"
            checked={disclaimer[0]}
            onChange={() => handleOptionChange(0)}
          />
          For coordination only
        </label>
        <label>
          <input
            type="checkbox"
            value="Disclaimer 2"
            checked={disclaimer[1]}
            onChange={() => handleOptionChange(1)}
          />
          Issued for tender
        </label>
        <label>
          <input
            type="checkbox"
            value="Disclaimer 3"
            checked={disclaimer[2]}
            onChange={() => handleOptionChange(2)}
          />
          Disclaimer Option 3
        </label>
      </div>
    </div>
  )
}

export default Disclaimer
