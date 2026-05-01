import Modal from "../common/Modal";
import StatusBadge from "../common/StatusBadge";

function UserProfileViewModal({ profile, onClose }) {
  if (!profile) return null;

  return (
    <Modal title={profile.name_of_role} onClose={onClose} width="640px">
      <div className="profile-view-table">
        <div className="profile-view-row">
          <div className="profile-view-label">NAME</div>
          <div className="profile-view-value">{profile.name_of_role}</div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">DESCRIPTION</div>
          <div className="profile-view-value">{profile.description || "-"}</div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">STATUS</div>
          <div className="profile-view-value">
            <StatusBadge status={profile.status} />
          </div>
        </div>
      </div>
    </Modal>
  );
}

export default UserProfileViewModal;