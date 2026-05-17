import { useState } from "react";
import ConfirmModal from "../../../components/userAdmin/ConfirmModal";
import { saveFundraisingActivity as saveFundraisingActivityApi } from "../../../api/doneeApi";

function saveFundraisingActivityPage({ activityId, onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalError, setModalError] = useState("");

  async function saveFundraisingActivity(activityID) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await saveFundraisingActivityApi(activityID);
      onSuccess();
      onClose();
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function onClick() {
    saveFundraisingActivity(activityId);
  }

  return (
    <ConfirmModal
      title="Save Activity"
      message="Do you want to save this activity to your favorites?"
      confirmText="SAVE"
      onClose={onClose}
      onConfirm={onClick}
      error={modalError}
      isSubmitting={isSubmitting}
    />
  );
}

export default saveFundraisingActivityPage;
