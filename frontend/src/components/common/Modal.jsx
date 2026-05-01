function Modal({ title, onClose, children, width = "640px" }) {
  return (
    <div className="modal-overlay">
      <div className="modal-container" style={{ width }}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="modal-close-btn" onClick={onClose}>
            X
          </button>
        </div>

        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
}

export default Modal;