import { useState } from "react";
import Modal from "../common/Modal";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

function UserAccountFormModal({
  mode,
  account,
  onClose,
  onSubmit,
  error,
  isSubmitting = false,
}) {
  const isEdit = mode === "edit";

  const [name, setName] = useState(account?.name || account?.username || "");
  const [dob, setDob] = useState(parseDate(account?.dob));
  const [email, setEmail] = useState(account?.email || "");
  const [phoneNo, setPhoneNo] = useState(account?.phone_no || "");
  const [address, setAddress] = useState(account?.address || "");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [formError, setFormError] = useState("");
  const [profile, setProfile] = useState(account?.name_of_role || "");

  function parseDate(dateString) {
    if (!dateString) return null;

    const date = new Date(dateString);
    return Number.isNaN(date.getTime()) ? null : date;
  }

  function formatDateForBackend(date) {
    if (!date) return "";

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${day}-${month}-${year}`;
  }

  function handleSubmit(e) {
    e.preventDefault();
    setFormError("");

    if (isEdit) {
      if (password || confirmPassword) {
        if (!password || !confirmPassword) {
          setFormError("Please fill in both new password and confirm password.");
          return;
        }

        if (password !== confirmPassword) {
          setFormError("Passwords do not match.");
          return;
        }
      }
    }

    const payload = {
      name,
      dob: formatDateForBackend(dob),
      phone_no: phoneNo,
      address,
      user_profile: profile,
      status: account?.status || "ACTIVE",
    };

    if (!isEdit) {
      payload.email = email;
    }

    if (password.trim()) {
      payload.password = password;
    }

    onSubmit(payload);
  }

  return (
    <Modal
      title={isEdit ? "Edit Account" : "New Account"}
      onClose={onClose}
      width="980px"
    >
      <form onSubmit={handleSubmit} className="account-form">
        <div className="account-form-grid">
          <div className="form-field">
            <label>FULL NAME</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="form-field">
            <label>BIRTHDATE</label>
            <DatePicker
              selected={dob}
              onChange={(date) => setDob(date)}
              dateFormat="dd MMMM yyyy"
              placeholderText="Select birthdate"
              showYearDropdown
              showMonthDropdown
              dropdownMode="select"
              maxDate={new Date()}
              className="date-picker-input"
            />
          </div>

          {!isEdit && (
            <div className="form-field">
              <label>EMAIL</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          )}

          <div className="form-field">
            <label>{isEdit ? "NEW PASSWORD" : "PASSWORD"}</label>
            <input
              type="password"
              value={password}
              placeholder={isEdit ? "Leave blank to keep current password" : ""}
              onChange={(e) => setPassword(e.target.value)}
              required={!isEdit}
            />
          </div>

          {isEdit && (
          <div className="form-field">
            <label>CONFIRM PASSWORD</label>
            <input
              type="password"
              value={confirmPassword}
              placeholder={isEdit ? "Confirm new password" : "Confirm password"}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required={!isEdit}
            />
            {(formError || error) && (
              <p className="modal-error-message">{formError || error}</p>
            )}
          </div>
          )}

          <div className="form-field">
            <label>PHONE</label>
            <input
              value={phoneNo}
              onChange={(e) => setPhoneNo(e.target.value)}
            />
          </div>

          <div className="form-field">
            <label>ADDRESS</label>
            <input
              value={address}
              onChange={(e) => setAddress(e.target.value)}
            />
          </div>
        </div>

        <div className="form-field full-width-field">
          <label>ASSIGNED PROFILE</label>
          <select
            value={profile}
            onChange={(e) => setProfile(e.target.value)}
            required
          >
            <option value="">Select profile</option>
            <option value="USER_ADMIN">User Admin</option>
            <option value="FUNDRAISER">Fundraiser</option>
            <option value="DONEE">Donee</option>
            <option value="PLATFORM_MANAGER">Platform Manager</option>
          </select>
        </div>

        <div className="modal-divider" />

        {error && <p className="modal-error-message">{error}</p>}

        <div className="modal-footer-actions">
          <button type="button" className="secondary-btn" onClick={onClose}>
            CANCEL
          </button>

          <button
            type="submit"
            className="primary-action-btn"
            disabled={isSubmitting}
          >
            {isEdit ? "SAVE CHANGES" : "CREATE ACCOUNT"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default UserAccountFormModal;