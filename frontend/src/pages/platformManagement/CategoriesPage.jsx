import { useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import SearchFundraisingCategoryPage from "./category/searchFundraisingCategoryPage";
import CreateCategoryPage from "./category/createCategoryPage";
import ViewFundraisingCategoryPage from "./category/viewFundraisingCategoryPage";
import UpdateCategoryPage from "./category/updateCategoryPage";
import SuspendCategoryPage from "./category/suspendCategoryPage";

function CategoriesPage({ onLogout, setCurrentPage }) {
  const [modalType, setModalType] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  function closeModal() {
    setModalType(null);
    setSelectedCategory(null);
  }

  function handleSuccess() {
    setRefreshKey((k) => k + 1);
  }

  return (
    <DashboardLayout
      activePage="categories"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="PLATFORM_MANAGER"
    >
      <SearchFundraisingCategoryPage
        onCreate={() => setModalType("create")}
        onView={(c) => { setSelectedCategory(c); setModalType("view"); }}
        onEdit={(c) => { setSelectedCategory(c); setModalType("edit"); }}
        onSuspend={(c) => { setSelectedCategory(c); setModalType("suspend"); }}
        refreshKey={refreshKey}
      />

      {modalType === "create" && (
        <CreateCategoryPage onClose={closeModal} onSuccess={handleSuccess} />
      )}

      {modalType === "view" && selectedCategory && (
        <ViewFundraisingCategoryPage categoryId={selectedCategory.id} onClose={closeModal} />
      )}

      {modalType === "edit" && selectedCategory && (
        <UpdateCategoryPage category={selectedCategory} onClose={closeModal} onSuccess={handleSuccess} />
      )}

      {modalType === "suspend" && selectedCategory && (
        <SuspendCategoryPage category={selectedCategory} onClose={closeModal} onSuccess={handleSuccess} />
      )}
    </DashboardLayout>
  );
}

export default CategoriesPage;
