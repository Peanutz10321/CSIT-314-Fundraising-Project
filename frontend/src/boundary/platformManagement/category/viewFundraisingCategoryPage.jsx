import { useEffect, useState } from "react";
import CategoryViewModal from "../../../components/platformManagement/CategoryViewModal";
import { getCategory } from "../../../api/categoryApi";

function viewFundraisingCategoryPage({ categoryId, onClose }) {
  const [category, setCategory] = useState(null);
  const [error, setError] = useState("");

  function displayCategory(data) {
    setCategory(data);
  }

  function displayNoData() {
    setError("Category not found.");
  }

  async function onClick(categoryID) {
    try {
      const result = await getCategory(categoryID);
      if (result) {
        displayCategory(result);
      } else {
        displayNoData();
      }
    } catch (err) {
      displayNoData();
    }
  }

  useEffect(() => {
    onClick(categoryId);
  }, [categoryId]);

  if (error) return <p className="error-message">{error}</p>;
  if (!category) return null;

  return <CategoryViewModal category={category} onClose={onClose} />;
}

export default viewFundraisingCategoryPage;
