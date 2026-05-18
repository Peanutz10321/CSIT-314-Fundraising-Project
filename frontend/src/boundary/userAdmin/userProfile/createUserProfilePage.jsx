import { useState } from "react";
import UserProfileFormModal from "../../../components/userAdmin/UserProfileFormModal";
import { createUserProfile } from "../../../api/userProfileApi";

function createUserProfilePage({ onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalError, setModalError] = useState("");

  async function onClick(payload) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await createUserProfile(payload);
      onSuccess();
      onClose();
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <UserProfileFormModal
      mode="create"
      onClose={onClose}
      onSubmit={onClick}
      error={modalError}
      isSubmitting={isSubmitting}
    />
  );
}

export default createUserProfilePage;
