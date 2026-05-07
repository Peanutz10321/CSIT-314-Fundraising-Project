function getProgress(activity) {
  const current = Number(activity.current_amount || 0);
  const goal = Number(activity.goal_amount || 0);
  if (goal <= 0) return 0;
  return Math.min((current / goal) * 100, 100);
}

function formatCurrency(currency, amount) {
  if (currency === "SGD") return `$${Number(amount || 0)}`;
  if (currency === "USD") return `$${Number(amount || 0)}`;
  return `${currency || "$"}${Number(amount || 0)}`;
}

function DoneeActivityCard({ activity, mode = "browse", onView, onSave, isSaved }) {
  const current = Number(activity.current_amount || 0);
  const goal = Number(activity.goal_amount || 0);
  const progress = getProgress(activity);
  const remaining = Math.max(100 - Math.round(progress), 0);
  const completed = String(activity.status || "").toUpperCase() === "COMPLETED";
  const viewCount = Number(activity.view_count ?? activity.views ?? activity.viewCount ?? 0);
  const shortlistCount = Number(activity.shortlist_count ?? activity.shortlists ?? activity.shortlistCount ?? 0);

  return (
    <div className="activity-card donee-activity-card">
      <div className="activity-card-main">
        <div className="activity-card-top">
          <div className="activity-badges">
            <span className="activity-category-badge">
              {activity.category || "CATEGORY"}
            </span>

            <span
              className={`activity-status-badge ${
                completed ? "completed" : "active"
              }`}
            >
              {completed ? "COMPLETED" : activity.status || "ONGOING"}
            </span>
          </div>

          <div className="activity-beneficiary">
            {activity.fundraiserName || activity.beneficiaryName || "-"}
          </div>
        </div>

        <h3 className="activity-title">{activity.title}</h3>
        <p className="activity-description-text">{activity.description || "-"}</p>

        <div className="activity-meta-row">
          <span>Ends {activity.deadline || "-"}</span>
          <span>{viewCount} views</span>
          <span>{shortlistCount} shortlisted</span>
        </div>

        <div className="activity-actions donee-card-actions">
          <button
            type="button"
            className="donee-view-btn"
            onClick={(event) => {
              event.stopPropagation();
              onView(activity);
            }}
          >
            View
          </button>

          {mode !== "completed" && (
            <button
              type="button"
              className={isSaved ? "donee-save-btn saved-btn" : "donee-save-btn"}
              onClick={(event) => {
                event.stopPropagation();
                if (!isSaved) onSave(activity);
              }}
              disabled={isSaved}
            >
              {isSaved ? "SAVED" : "SAVE"}
            </button>
          )}
        </div>
      </div>

      <div className="activity-card-side">
        <p className="raised-label">{mode === "completed" ? "YOU RAISED" : "RAISED"}</p>
        <h3 className="raised-amount">{formatCurrency(activity.currency, current)}</h3>
        <p className="raised-goal-text">
          of {formatCurrency(activity.currency, goal)} goal
        </p>

        <div className="activity-progress-wrap">
          <div className="activity-progress-track">
            <div
              className="activity-progress-fill"
              style={{ width: `${progress}%` }}
            />
          </div>

          <div className="activity-progress-labels">
            <span>{Math.round(progress)}%</span>
            <span>{completed ? "GOAL MET" : `${remaining}% TO GO`}</span>
          </div>
        </div>

        <p className="activity-location">{activity.location || "-"}</p>
      </div>
    </div>
  );
}

export default DoneeActivityCard;
