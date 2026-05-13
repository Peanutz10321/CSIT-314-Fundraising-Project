function StatusBadge({ status, variant = "fundraiser" }) {
  const normalizedStatus = status || "UNKNOWN";

  if (variant === "donee") {
    let modifier = "suspended";
    if (normalizedStatus === "ACTIVE" || normalizedStatus === "ONGOING") modifier = "ongoing";
    else if (normalizedStatus === "COMPLETED") modifier = "completed";
    return <span className={`activity-status-badge ${modifier}`}>{normalizedStatus}</span>;
  }

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