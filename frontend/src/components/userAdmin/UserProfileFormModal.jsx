import { useState } from "react";
import Modal from "../common/Modal";

function UserProfileFormModal({
  mode,
  profile,
  onClose,
  onSubmit,
  error,
  isSubmitting = false,
}) {
  const [nameOfRole, setNameOfRole] = useState(profile?.name_of_role || "");
  const [description, setDescription] = useState(profile?.description || "");

  function handleSubmit(e) {
    e.preventDefault();

    onSubmit({
      name_of_role: nameOfRole,
      description,
      status: profile?.status || "ACTIVE",
    });
  }

  const isEdit = mode === "edit";

  return (
    <Modal
      title={isEdit ? "Edit Profile" : "New User Profile"}
      onClose={onClose}
      width="640px"
    >
      <form onSubmit={handleSubmit} className="profile-form">
        <label>PROFILE NAME</label>
        <input
          type="text"
          value={nameOfRole}
          onChange={(e) => setNameOfRole(e.target.value)}
          required
        />

        <label>DESCRIPTION</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows="5"
        />

        <div className="modal-divider" />

        {error && <p className="modal-error-message">{error}</p>}

        <div className="modal-footer-actions">
          <button type="button" className="secondary-btn" onClick={onClose}>
            CANCEL
          </button>

          <button type="submit" className="primary-action-btn" disabled={isSubmitting}>
            {isEdit ? "SAVE CHANGES" : "CREATE PROFILE"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default UserProfileFormModal;