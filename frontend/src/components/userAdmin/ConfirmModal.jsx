import Modal from "../common/Modal";

function ConfirmModal({
  title,
  message,
  confirmText,
  onClose,
  onConfirm,
  error,
  isSubmitting = false,
}) {
  return (
    <Modal title={title} onClose={onClose} width="760px">
      <div className="confirm-modal-content">
        <p>{message}</p>

        {error && <p className="modal-error-message">{error}</p>}

        <div className="modal-footer-actions">
          <button type="button" className="secondary-btn" onClick={onClose}>
            CANCEL
          </button>

          <button
            type="button"
            className="primary-action-btn"
            onClick={onConfirm}
            disabled={isSubmitting}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </Modal>
  );
}

export default ConfirmModal;