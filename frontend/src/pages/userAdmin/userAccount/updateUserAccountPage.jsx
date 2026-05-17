import { useState } from "react";
import UserAccountFormModal from "../../../components/userAdmin/UserAccountFormModal";
import { updateUserAccount } from "../../../api/userAccountApi";

function updateUserAccountPage({ account, onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalError, setModalError] = useState("");

  async function onClick(payload) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await updateUserAccount(account.id, payload);
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
      mode="edit"
      account={account}
      onClose={onClose}
      onSubmit={onClick}
      error={modalError}
      isSubmitting={isSubmitting}
    />
  );
}

export default updateUserAccountPage;
