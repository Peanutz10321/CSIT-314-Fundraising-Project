import { useState } from "react";
import UserAccountFormModal from "../../../components/userAdmin/UserAccountFormModal";
import { createUserAccount } from "../../../api/userAccountApi";

function createUserAccountPage({ onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalError, setModalError] = useState("");

  async function onClick(payload) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await createUserAccount(payload);
      onSuccess();
      onClose();
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <UserAccountFormModal
      mode="create"
      onClose={onClose}
      onSubmit={onClick}
      error={modalError}
      isSubmitting={isSubmitting}
    />
  );
}

export default createUserAccountPage;
