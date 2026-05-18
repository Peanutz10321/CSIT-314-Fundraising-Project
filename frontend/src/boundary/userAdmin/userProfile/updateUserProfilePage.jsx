import { useState } from "react";
import UserProfileFormModal from "../../../components/userAdmin/UserProfileFormModal";
import { updateUserProfile } from "../../../api/userProfileApi";

function updateUserProfilePage({ profile, onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalError, setModalError] = useState("");

  function goToProfileUpdate(profileID) {
    return profile;
  }

  async function onClick(payload) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await updateUserProfile(profile.id, payload);
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
      mode="edit"
      profile={goToProfileUpdate(profile.id)}
      onClose={onClose}
      onSubmit={onClick}
      error={modalError}
      isSubmitting={isSubmitting}
    />
  );
}

export default updateUserProfilePage;
