import { useState } from "react";
import ConfirmModal from "../../../components/userAdmin/ConfirmModal";
import { suspendCategory } from "../../../api/categoryApi";

function suspendCategoryPage({ category, onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function suspendCategoryAction(categoryID) {
    try {
      setIsSubmitting(true);
      setError("");
      await suspendCategory(categoryID);
      onSuccess();
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function onClick() {
    suspendCategoryAction(category.id);
  }

  return (
    <ConfirmModal
      title="Suspend"
      message={`Are you sure you want to suspend the category ${category.name}?`}
      confirmText="SUSPEND"
      onClose={onClose}
      onConfirm={onClick}
      error={error}
      isSubmitting={isSubmitting}
    />
  );
}

export default suspendCategoryPage;
