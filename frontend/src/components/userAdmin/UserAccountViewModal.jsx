import Modal from "../common/Modal";
import StatusBadge from "../common/StatusBadge";

function UserAccountViewModal({ account, onClose }) {
  if (!account) return null;

  return (
    <Modal
      title={account.name_of_role || account.profile || "User Account"}
      onClose={onClose}
      width="760px"
    >
      <div className="profile-view-table">
        <div className="profile-view-row">
          <div className="profile-view-label">NAME</div>
          <div className="profile-view-value">
            {account.name || "-"}
          </div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">BIRTHDATE</div>
          <div className="profile-view-value">{account.dob || "-"}</div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">PHONE</div>
          <div className="profile-view-value">{account.phone_no || "-"}</div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">EMAIL</div>
          <div className="profile-view-value">
            <u>{account.email || "-"}</u>
          </div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">ADDRESS</div>
          <div className="profile-view-value">{account.address || "-"}</div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">PROFILE</div>
          <div className="profile-view-value">
            {account.name_of_role || "-"}
          </div>
        </div>

        <div className="profile-view-row">
          <div className="profile-view-label">STATUS</div>
          <div className="profile-view-value">
            <StatusBadge status={account.status} />
          </div>
        </div>
      </div>
    </Modal>
  );
}

export default UserAccountViewModal;