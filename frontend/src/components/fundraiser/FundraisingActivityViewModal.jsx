import Modal from "../common/Modal";
import StatusBadge from "../common/StatusBadge";

function FundraisingActivityViewModal({ activity, onClose }) {
  if (!activity) return null;

  const currentAmount = Number(activity.current_amount || 0);
  const goalAmount = Number(activity.goal_amount || 0);
  const viewCount = activity.view_count || 0;
  const shortlistCount = activity.shortlist_count || 0;
  
  const progress =
    goalAmount > 0 ? Math.min((currentAmount / goalAmount) * 100, 100) : 0;

  return (
    <Modal title={activity.title} onClose={onClose} width="680px">
      <div className="activity-view">
        <div className="activity-view-top">
          <span className="category-badge">
            {activity.category || "CATEGORY"}
          </span>

          <StatusBadge status={activity.status} />

          <strong className="beneficiary-name">
            {activity.beneficiaryName || "-"}
          </strong>
        </div>

        <p className="activity-description">{activity.description || "-"}</p>

        <div className="activity-stats-grid">
          <div>
            <span>RAISED</span>
            <strong>${currentAmount}</strong>
            <p>
              {goalAmount > 0 ? Math.round((currentAmount / goalAmount) * 100) : 0}
              % of goal
            </p>
          </div>

          <div>
            <span>VIEWS</span>
            <strong>{viewCount}</strong>
            <p>page views</p>
          </div>

          <div>
            <span>SHORTLISTS</span>
            <strong>{shortlistCount}</strong>
            <p>donees saved</p>
          </div>
        </div>

        <div className="activity-progress-bar">
          <div style={{ width: `${progress}%` }} />
        </div>

        <p className="activity-goal-line">
          Goal ${goalAmount} · Deadline {activity.deadline || "-"}
        </p>

        <div className="modal-divider" />

        <div className="activity-meta-grid">
          <div>
            <span>DATE CREATED</span>
            <strong>{activity.date_created
            ? new Date(activity.date_created).toLocaleDateString()
            : "-"}</strong>
          </div>

          <div>
            <span>ACTIVITY ID</span>
            <strong>{activity.activity_id || activity.id}</strong>
          </div>

          <div>
            <span>ORGANIZER</span>
            <strong>{activity.fundraiserName || "-"}</strong>
          </div>

          <div>
            <span>LOCATION</span>
            <strong>{activity.location || "-"}</strong>
          </div>
        </div>
      </div>
    </Modal>
  );
}

export default FundraisingActivityViewModal;