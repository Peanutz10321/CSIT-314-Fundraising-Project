function StatusBadge({ status }) {
  const normalizedStatus = status || "UNKNOWN";

  let className = "status";

  if (normalizedStatus === "ACTIVE" || normalizedStatus === "ONGOING") {
    className += " active-status";
  } else if (normalizedStatus === "COMPLETED") {
    className += " completed-status";
  } else {
    className += " suspended-status";
  }

  return <span className={className}>{normalizedStatus}</span>;
}

export default StatusBadge;