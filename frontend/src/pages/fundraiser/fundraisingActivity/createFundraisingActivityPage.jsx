import { useState } from "react";
import FundraisingActivityFormModal from "../../../components/fundraiser/FundraisingActivityFormModal";
import { createFundraisingActivity } from "../../../api/fundraisingActivityApi";

function createFundraisingActivityPage({ onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalError, setModalError] = useState("");

  async function onClick(payload) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await createFundraisingActivity(payload);
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
      mode="create"
      onClose={onClose}
      onSubmit={onClick}
      error={modalError}
      isSubmitting={isSubmitting}
    />
  );
}

export default createFundraisingActivityPage;
