import React, { useState, useEffect } from "react"

function DateSelector({ setSelectedDate }) {
  const [internalDate, setInternalDate] = useState("")

  // Convert date to "YYYY-MM-DD" format for the input
  const formatDateForInput = (date) => {
    if (!date) return ""
    const [year, month, day] = [
      date.getFullYear(),
      date.getMonth() + 1,
      date.getDate(),
    ]
    return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(
      2,
      "0"
    )}`
  }

  // Convert date to "DEC / 15 / 2023" format in UTC
  const formatDateForDisplay = (date) => {
    if (!date) return ""
    const monthNames = [
      "JAN",
      "FEB",
      "MAR",
      "APR",
      "MAY",
      "JUN",
      "JUL",
      "AUG",
      "SEP",
      "OCT",
      "NOV",
      "DEC",
    ]
    const year = date.getUTCFullYear()
    const month = monthNames[date.getUTCMonth()]
    const day = date.getUTCDate().toString().padStart(2, "0")
    return `${month} / ${day} / ${year}`
  }

  // Handle changes to the date input
  const handleChange = (event) => {
    const dateValue = event.target.value
    setInternalDate(dateValue)

    // Adjust the date creation to treat the input as a UTC date
    const [year, month, day] = dateValue
      .split("-")
      .map((num) => parseInt(num, 10))
    const newDate = new Date(Date.UTC(year, month - 1, day)) // Months are 0-indexed in JavaScript Date

    setSelectedDate(formatDateForDisplay(newDate))
  }

  // Initialize with today's date
  useEffect(() => {
    const today = new Date()
    setInternalDate(formatDateForInput(today))
    setSelectedDate(formatDateForDisplay(today))
  }, []) // Empty dependency array to run only once on mount

  return (
    <div className="date-selector-container">
      <label htmlFor="date-selector" className="input-label">
        Select a Date:
      </label>
      <input
        type="date"
        id="date-selector"
        className="date-input"
        value={internalDate}
        onChange={handleChange}
      />
    </div>
  )
}

export default DateSelector
