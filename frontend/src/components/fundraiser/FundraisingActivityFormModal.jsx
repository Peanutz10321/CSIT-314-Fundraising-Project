import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import Modal from "../common/Modal";

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

  return `${year}-${month}-${day}`;
}

function FundraisingActivityFormModal({
  mode,
  activity,
  onClose,
  onSubmit,
  error,
  isSubmitting = false,
}) {
const isEdit = mode === "edit";

const [fundraiserName, setFundraiserName] = useState(activity?.fundraiserName || "");
const [beneficiaryName, setBeneficiaryName] = useState(activity?.beneficiaryName || "");
const [title, setTitle] = useState(activity?.title || "");
const [description, setDescription] = useState(activity?.description || "");
const [currency, setCurrency] = useState(activity?.currency || "SGD");
const [goalAmount, setGoalAmount] = useState(activity?.goal_amount || "");
const [category, setCategory] = useState(activity?.category || "");
const [location, setLocation] = useState(activity?.location || "");
const [deadline, setDeadline] = useState(parseDate(activity?.deadline));

  function handleSubmit(e) {
    e.preventDefault();

    const payload = {
        fundraiserName,
        beneficiaryName,
        title,
        description,
        currency,
        goal_amount: Number(goalAmount),
        category,
        location,
        deadline: formatDateForBackend(deadline),
    };

    onSubmit(payload);
  }

  return (
    <Modal
      title={isEdit ? "Edit Activity" : "New Fundraising Activity"}
      onClose={onClose}
      width="760px"
    >
      <form onSubmit={handleSubmit} className="fundraising-form">
        <div className="form-field full-width-field">
        <label>FUNDRAISER NAME</label>
        <input
            value={fundraiserName}
            onChange={(e) => setFundraiserName(e.target.value)}
        />
        </div>

        <div className="form-field full-width-field">
        <label>BENEFICIARY NAME</label>
        <input
            value={beneficiaryName}
            onChange={(e) => setBeneficiaryName(e.target.value)}
        />
        </div>

        <div className="form-field full-width-field">
          <label>TITLE</label>
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div className="form-field full-width-field">
          <label>DESCRIPTION</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows="3"
          />
        </div>

        <div className="fundraising-form-grid">
          <div className="form-field">
            <label>LOCATION</label>
            <input
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </div>

          <div className="form-field">
            <label>GOAL AMOUNT</label>
            <input
              type="number"
              min="0"
              value={goalAmount}
              onChange={(e) => setGoalAmount(e.target.value)}
              required
            />
          </div>

          <div className="form-field">
            <label>CATEGORY</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              required
            >
              <option value="">Select category</option>
              <option value="COMMUNITY">Community</option>
              <option value="EDUCATION">Education</option>
              <option value="HEALTHCARE">Healthcare</option>
              <option value="EMERGENCY">Emergency</option>
            </select>
          </div>

          <div className="form-field">
            <label>END DATE</label>
            <DatePicker
            selected={deadline}
            onChange={(date) => setDeadline(date)}
            dateFormat="dd MMMM yyyy"
            placeholderText="Select deadline"
            minDate={new Date()}
            showYearDropdown
            showMonthDropdown
            dropdownMode="select"
            className="date-picker-input"
            />
          </div>
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
            {isEdit ? "SAVE CHANGES" : "CREATE ACTIVITY"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default FundraisingActivityFormModal;