import React from "react";
import EosLogo from "../Assets/eos-logo-horizontal.png";
import AldLogo from "../Assets/ald-logo-horizontal.png";

function PreparedBySelector({ value, setValue }) {
  const handleSelect = (selectedValue) => {
    setValue(selectedValue);
  };

  return (
    <div className="selector-container">
      <div className="button-group button-group-company">
        <button
          onClick={() => handleSelect("Eos Lightmedia")}
          className={
            value === "Eos Lightmedia"
              ? "selected company-button"
              : "company-button"
          }
        >
          <img src={EosLogo} alt="Eos Lightmedia" className="company-logo" />
        </button>
        <button
          onClick={() => handleSelect("Abernathy Lighting Design")}
          className={
            value === "Abernathy Lighting Design"
              ? "selected company-button"
              : "company-button"
          }
        >
          <img
            src={AldLogo}
            alt="Abernathy Lighting Design"
            className="company-logo"
          />
        </button>
      </div>
    </div>
  );
}

export default PreparedBySelector;
