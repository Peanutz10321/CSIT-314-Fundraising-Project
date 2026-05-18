import { useState } from "react";
import CategoryFormModal from "../../../components/platformManagement/CategoryFormModal";
import { updateCategory } from "../../../api/categoryApi";

function updateCategoryPage({ category, onClose, onSuccess }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function onClick(payload) {
    try {
      setIsSubmitting(true);
      setError("");
      await updateCategory(category.id, payload);
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
      mode="edit"
      category={category}
      onClose={onClose}
      onSubmit={onClick}
      error={error}
      isSubmitting={isSubmitting}
    />
  );
}

export default updateCategoryPage;
