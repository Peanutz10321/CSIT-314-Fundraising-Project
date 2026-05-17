import { useState } from "react";
import ConfirmModal from "../../../components/userAdmin/ConfirmModal";
import { suspendUserAccount as suspendUserAccountApi } from "../../../api/userAccountApi";

function suspendUserAccountPage({ account, onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [modalError, setModalError] = useState("");

  async function suspendUserAccount(accountID) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await suspendUserAccountApi(accountID);
      onSuccess();
      onClose();
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function onClickSuspend() {
    suspendUserAccount(account.id);
  }

  return (
    <ConfirmModal
      title="Suspend"
      message={`Are you sure you want to suspend the account ${account.name || account.email}?`}
      confirmText="SUSPEND"
      onClose={onClose}
      onConfirm={onClickSuspend}
      error={modalError}
      isSubmitting={isSubmitting}
    />
  );
}

export default suspendUserAccountPage;
