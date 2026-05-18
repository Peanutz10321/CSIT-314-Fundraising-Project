import { useState } from "react";
import CategoryFormModal from "../../../components/platformManagement/CategoryFormModal";
import { createFundraisingCategory } from "../../../api/categoryApi";

function createCategoryPage({ onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function onClick(payload) {
    try {
      setIsSubmitting(true);
      setError("");
      await createFundraisingCategory(payload);
      onSuccess();
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <CategoryFormModal
      mode="create"
      onClose={onClose}
      onSubmit={onClick}
      error={error}
      isSubmitting={isSubmitting}
    />
  );
}

export default createCategoryPage;
