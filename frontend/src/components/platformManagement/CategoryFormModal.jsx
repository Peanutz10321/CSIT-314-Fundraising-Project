import { useState } from "react";
import Modal from "../common/Modal";

function CategoryFormModal({ mode, category, onClose, onSubmit, error, isSubmitting = false }) {
  const [name, setName] = useState(category?.name || "");
  const [description, setDescription] = useState(category?.description || "");

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit({ name, description });
  }

  const isEdit = mode === "edit";

  return (
    <Modal title={isEdit ? "Edit Category" : "New Category"} onClose={onClose} width="640px">
      <form onSubmit={handleSubmit} className="profile-form">
        <label>CATEGORY NAME</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
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
            {isEdit ? "SAVE CHANGES" : "CREATE CATEGORY"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default CategoryFormModal;
