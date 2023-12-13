import React from "react";
import EosLogo from "../Assets/eos-logo.png";
import AbernathyLogo from "../Assets/abernathy-logo.png";
import PurpleGradient from "../Assets/purple-gradient.png";
import OrangeGradient from "../Assets/orange-gradient.png";

function StampPreview(props) {
  const {
    jobName,
    jobCode,
    preparedFor,
    preparedBy,
    date,
    isRevision,
    jobPhase,
    gradientStyle,
    dateFormat,
    revisionNumber,
  } = props;

  const formatDisplayDate = (date, format) => {
    if (!date || !date.year || !date.month || !date.day) {
      return "No Date Selected";
    }
    const paddedMonth = String(date.month).padStart(2, "0");
    const paddedDay = String(date.day).padStart(2, "0");
    switch (format) {
      case "YYYY/MM/DD":
        return `${date.year}/${paddedMonth}/${paddedDay}`;
      case "MM/DD/YYYY":
        return `${paddedMonth}/${paddedDay}/${date.year}`;
      case "DD/MM/YYYY":
        return `${paddedDay}/${paddedMonth}/${date.year}`;
      default:
        return `${date.year}-${paddedMonth}-${paddedDay}`; // Default format
    }
  };

  const displayDate = formatDisplayDate(date, dateFormat);

  const displayLogo =
    preparedBy === "Eos Lightmedia"
      ? EosLogo
      : preparedBy === "Abernathy Lighting Design"
      ? AbernathyLogo
      : null;

  const getGradientStyle = (gradient) => {
    switch (gradient) {
      case "Purple/Blue":
        return {
          backgroundImage: `url(${PurpleGradient})`,
          backgroundPosition: "bottom left",
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
        };
      case "Yellow/Green":
        return {
          backgroundImage: `url(${OrangeGradient})`,
          backgroundPosition: "bottom left",
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
        };
      default:
        return {};
    }
  };

  const previewStyle = getGradientStyle(gradientStyle);

  return (
    <div className="content-div">
      <div className="stamp-preview-div" style={previewStyle}>
        <div className="first-column">
          <p class="type-title">
            Type
            <br />
            <span className="type-value">EG01</span>
          </p>
        </div>
        <div class="second-column">
          <div className="info-grid">
            <p>
              Project Name <span className="value">{jobName}</span>
            </p>
            <p>
              Job Code <span className="value">{jobCode}</span>
            </p>
            <p>
              Prepared For <span className="value">{preparedFor}</span>
            </p>

            <p>
              Project Phase <span className="value">{jobPhase}</span>
            </p>
          </div>
        </div>
        {displayLogo && (
          <img className="preview-logo" src={displayLogo} alt="Company Logo" />
        )}
      </div>
      <div className="preview-footer">
        <div className="footer-content">
          <p>
            {isRevision ? "Revision Date" : "Issued Date"}:{" "}
            <span className="footer-value">{displayDate}</span>
            {isRevision && (
              <>
                {"  |  "}
                Revision <span className="footer-value">{revisionNumber}</span>
              </>
            )}
          </p>
          <p>
            Page <strong>XX</strong> of <strong>XX</strong>
          </p>
        </div>
      </div>
    </div>
  );
}

export default StampPreview;
