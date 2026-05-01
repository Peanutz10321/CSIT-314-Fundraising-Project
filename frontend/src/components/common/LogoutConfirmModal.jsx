import Modal from "./Modal";

function LogoutConfirmModal({ onClose, onConfirm }) {
  return (
    <Modal title="Log out" onClose={onClose} width="760px">
      <div className="confirm-modal-content">
        <p>Are you sure you want to log out?</p>

        <div className="modal-footer-actions">
          <button type="button" className="secondary-btn" onClick={onClose}>
            CANCEL
          </button>

          <button type="button" className="primary-action-btn" onClick={onConfirm}>
            LOG OUT
          </button>
        </div>
      </div>
    </Modal>
  );
}

export default LogoutConfirmModal;