import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import StatusBadge from "../../components/common/StatusBadge";
import CategoryFormModal from "../../components/platformManagement/CategoryFormModal";
import CategoryViewModal from "../../components/platformManagement/CategoryViewModal";
import ConfirmModal from "../../components/userAdmin/ConfirmModal";
import {
  getCategories,
  createCategory,
  updateCategory,
  suspendCategory,
} from "../../api/categoryApi";

function CategoriesPage({ onLogout, setCurrentPage }) {
  const [categories, setCategories] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [error, setError] = useState("");
  const [modalType, setModalType] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [modalError, setModalError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function loadCategories(searchKeyword = "") {
    try {
      setError("");
      const result = await getCategories(searchKeyword);
      setCategories(result.data || result || []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadCategories();
  }, []);

  function closeModal() {
    setModalType(null);
    setSelectedCategory(null);
    setModalError("");
  }

  async function handleCreate(payload) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await createCategory(payload);
      closeModal();
      loadCategories(keyword);
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleEdit(payload) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await updateCategory(selectedCategory.id, payload);
      closeModal();
      loadCategories(keyword);
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleSuspend() {
    try {
      setIsSubmitting(true);
      setModalError("");
      await suspendCategory(selectedCategory.id);
      closeModal();
      loadCategories(keyword);
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleSearchChange(e) {
    const value = e.target.value;
    setKeyword(value);
    loadCategories(value);
  }

  return (
    <DashboardLayout
      activePage="categories"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="PLATFORM_MANAGER"
    >
      <div className="page-header">
        <h1>Activity Categories</h1>
        <button
          className="primary-btn small-btn"
          onClick={() => { setSelectedCategory(null); setModalError(""); setModalType("create"); }}
        >
          +New Category
        </button>
      </div>

      <div className="divider" />

      <div className="fundraising-search-wrapper" style={{ marginBottom: "24px", maxWidth: "1200px" }}>
        <span className="search-icon">🔍</span>
        <input
          className="fundraising-search-input"
          placeholder="search categories..."
          value={keyword}
          onChange={handleSearchChange}
        />
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="category-card-grid">
        {categories.length === 0 ? (
          <div className="empty-card-state">No matching categories found.</div>
        ) : (
          categories.map((cat) => (
            <div className="category-card" key={cat.id}>
              <div className="category-card-header">
                <span className="category-card-name">{cat.name}</span>
                <StatusBadge status={cat.status} />
              </div>

              <p className="category-card-desc">{cat.description || "-"}</p>

              <div className="category-card-footer">
                <span className="category-activity-count">{cat.activity_count ?? 0} activities</span>
                <div className="actions">
                  <button onClick={() => { setSelectedCategory(cat); setModalError(""); setModalType("view"); }}>
                    View
                  </button>
                  <button onClick={() => { setSelectedCategory(cat); setModalError(""); setModalType("edit"); }}>
                    EDIT
                  </button>
                  <button
                    className="danger-btn"
                    onClick={() => { setSelectedCategory(cat); setModalError(""); setModalType("suspend"); }}
                    disabled={cat.status !== "ACTIVE"}
                  >
                    {cat.status === "ACTIVE" ? "SUSPEND" : "SUSPENDED"}
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {modalType === "create" && (
        <CategoryFormModal
          mode="create"
          onClose={closeModal}
          onSubmit={handleCreate}
          error={modalError}
          isSubmitting={isSubmitting}
        />
      )}

      {modalType === "edit" && selectedCategory && (
        <CategoryFormModal
          mode="edit"
          category={selectedCategory}
          onClose={closeModal}
          onSubmit={handleEdit}
          error={modalError}
          isSubmitting={isSubmitting}
        />
      )}

      {modalType === "view" && selectedCategory && (
        <CategoryViewModal category={selectedCategory} onClose={closeModal} />
      )}

      {modalType === "suspend" && selectedCategory && (
        <ConfirmModal
          title="Suspend"
          message={`Are you sure you want to suspend the category ${selectedCategory.name}?`}
          confirmText="SUSPEND"
          onClose={closeModal}
          onConfirm={handleSuspend}
          error={modalError}
          isSubmitting={isSubmitting}
        />
      )}
    </DashboardLayout>
  );
}

export default CategoriesPage;
