function StatusBadge({ status }) {
  const normalizedStatus = status || "UNKNOWN";

  return (
    <span
      className={
        normalizedStatus === "ACTIVE"
          ? "status active-status"
          : "status suspended-status"
      }
    >
      {normalizedStatus}
    </span>
  );
}

export default StatusBadge;