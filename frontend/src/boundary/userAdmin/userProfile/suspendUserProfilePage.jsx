import { useState } from "react";
import ConfirmModal from "../../../components/userAdmin/ConfirmModal";
import { suspendUserProfile as suspendUserProfileApi } from "../../../api/userProfileApi";

function suspendUserProfilePage({ profile, onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalError, setModalError] = useState("");

  async function suspendUserProfile(profileID) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await suspendUserProfileApi(profileID);
      onSuccess();
      onClose();
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function onClick() {
    suspendUserProfile(profile.id);
  }

  return (
    <ConfirmModal
      title="Suspend"
      message={`Are you sure you want to suspend the profile ${profile.name_of_role}?`}
      confirmText="SUSPEND"
      onClose={onClose}
      onConfirm={onClick}
      error={modalError}
      isSubmitting={isSubmitting}
    />
  );
}

export default suspendUserProfilePage;
