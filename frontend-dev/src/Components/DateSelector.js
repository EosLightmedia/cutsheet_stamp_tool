import React from "react";

function DateSelector({ selectedDate, setSelectedDate }) {
  const convertDateToObj = (dateStr) => {
    const dateObj = new Date(dateStr);
    if (isNaN(dateObj.getTime())) {
      return { year: "", month: "", day: "" };
    }

    return {
      year: dateObj.getFullYear(),
      month: dateObj.getMonth() + 1, // getMonth() returns 0-11
      day: dateObj.getDate(),
    };
  };

  const handleChange = (event) => {
    const dateObj = convertDateToObj(event.target.value);
    setSelectedDate(dateObj);
  };

  return (
    <div className="date-selector-container">
      <label htmlFor="date-selector" className="input-label">
        Select a Date:
      </label>
      <input
        type="date"
        id="date-selector"
        className="date-input"
        value={
          selectedDate
            ? `${selectedDate.year}-${selectedDate.month
                .toString()
                .padStart(2, "0")}-${selectedDate.day
                .toString()
                .padStart(2, "0")}`
            : ""
        }
        onChange={handleChange}
      />
    </div>
  );
}

export default DateSelector;
