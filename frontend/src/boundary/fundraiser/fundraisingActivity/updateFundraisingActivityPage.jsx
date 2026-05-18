import { useState } from "react";
import FundraisingActivityFormModal from "../../../components/fundraiser/FundraisingActivityFormModal";
import { updateFundraisingActivity } from "../../../api/fundraisingActivityApi";

function updateFundraisingActivityPage({ activity, onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalError, setModalError] = useState("");

  async function onClick(payload) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await updateFundraisingActivity(activity.id, payload);
      onSuccess();
      onClose();
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <FundraisingActivityFormModal
      mode="edit"
      activity={activity}
      onClose={onClose}
      onSubmit={onClick}
      error={modalError}
      isSubmitting={isSubmitting}
    />
  );
}

export default updateFundraisingActivityPage;
