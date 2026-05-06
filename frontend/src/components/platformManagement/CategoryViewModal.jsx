import Modal from "../common/Modal";
import StatusBadge from "../common/StatusBadge";

function CategoryViewModal({ category, onClose }) {
  if (!category) return null;

  const dateStr = category.date_created
    ? new Date(category.date_created).toISOString().split("T")[0]
    : "-";

  return (
    <Modal title={category.name} onClose={onClose} width="640px">
      <div className="profile-view-table">
        <div className="profile-view-row">
          <div className="profile-view-label">NAME</div>
          <div className="profile-view-value">{category.name}</div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">DESCRIPTION</div>
          <div className="profile-view-value">{category.description || "-"}</div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">STATUS</div>
          <div className="profile-view-value">
            <StatusBadge status={category.status} />
          </div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">ACTIVITIES</div>
          <div className="profile-view-value">{category.activity_count ?? 0}</div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">DATE CREATED</div>
          <div className="profile-view-value">{dateStr}</div>
        </div>
      </div>
    </Modal>
  );
}

export default CategoryViewModal;
