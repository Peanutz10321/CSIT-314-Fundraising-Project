import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import SearchFundraisingActivityPage from "./browseActivity/searchFundraisingActivityPage";
import ViewFundraisingActivityPage from "./browseActivity/viewFundraisingActivityPage";
import SaveFundraisingActivityPage from "./browseActivity/saveFundraisingActivityPage";
import { viewFavoriteList } from "../../api/doneeApi";

function DoneeBrowseActivitiesPage({ onLogout, setCurrentPage }) {
  const [modalType, setModalType] = useState(null);
  const [selectedActivity, setSelectedActivity] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [favoriteIds, setFavoriteIds] = useState([]);

  useEffect(() => {
    viewFavoriteList()
      .then((res) => setFavoriteIds((res.data || []).map((a) => String(a.id)).filter(Boolean)))
      .catch(() => {});
  }, []);

  function closeModal() {
    setModalType(null);
    setSelectedActivity(null);
  }

  function handleViewClose() {
    closeModal();
    setRefreshKey((k) => k + 1);
  }

  function handleSaveSuccess() {
    setFavoriteIds((prev) =>
      selectedActivity ? [...prev, String(selectedActivity.id)] : prev
    );
    setRefreshKey((k) => k + 1);
  }

  return (
    <DashboardLayout
      activePage="doneeBrowse"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="DONEE"
    >
      <SearchFundraisingActivityPage
        onView={(a) => { setSelectedActivity(a); setModalType("view"); }}
        onSave={(a) => { setSelectedActivity(a); setModalType("save"); }}
        refreshKey={refreshKey}
        favoriteIds={favoriteIds}
      />

      {modalType === "view" && selectedActivity && (
        <ViewFundraisingActivityPage activityId={selectedActivity.id} onClose={handleViewClose} />
      )}

      {modalType === "save" && selectedActivity && (
        <SaveFundraisingActivityPage
          activityId={selectedActivity.id}
          onClose={closeModal}
          onSuccess={handleSaveSuccess}
        />
      )}
    </DashboardLayout>
  );
}

export default DoneeBrowseActivitiesPage;
