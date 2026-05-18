import { useState } from "react";
import ConfirmModal from "../../../components/userAdmin/ConfirmModal";
import { suspendFundraisingActivity as suspendFundraisingActivityApi } from "../../../api/fundraisingActivityApi";

function suspendFundraisingActivityPage({ activity, onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalError, setModalError] = useState("");

  async function suspendFundraisingActivity(activityID) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await suspendFundraisingActivityApi(activityID);
      onSuccess();
      onClose();
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function onClick() {
    suspendFundraisingActivity(activity.id);
  }

  return (
    <ConfirmModal
      title="Suspend"
      message={`Are you sure you want to suspend the activity ${activity.title}?`}
      confirmText={activity.status === "ACTIVE" ? "SUSPEND" : "REACTIVATE"}
      onClose={onClose}
      onConfirm={onClick}
      error={modalError}
      isSubmitting={isSubmitting}
    />
  );
}

export default suspendFundraisingActivityPage;
