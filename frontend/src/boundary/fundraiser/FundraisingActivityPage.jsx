import { useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import SearchFundraisingActivityPage from "./fundraisingActivity/searchFundraisingActivityPage";
import CreateFundraisingActivityPage from "./fundraisingActivity/createFundraisingActivityPage";
import ViewFundraisingActivityPage from "./fundraisingActivity/viewFundraisingActivityPage";
import UpdateFundraisingActivityPage from "./fundraisingActivity/updateFundraisingActivityPage";
import SuspendFundraisingActivityPage from "./fundraisingActivity/suspendFundraisingActivityPage";

function FundraisingActivityPage({ onLogout, setCurrentPage }) {
  const [modalType, setModalType] = useState(null);
  const [selectedActivity, setSelectedActivity] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  function closeModal() {
    setModalType(null);
    setSelectedActivity(null);
  }

  function handleSuccess() {
    setRefreshKey((k) => k + 1);
  }

  return (
    <DashboardLayout
      activePage="fundraisingActivities"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="FUNDRAISER"
    >
      <SearchFundraisingActivityPage
        onCreate={() => setModalType("create")}
        onView={(a) => { setSelectedActivity(a); setModalType("view"); }}
        onEdit={(a) => { setSelectedActivity(a); setModalType("edit"); }}
        onSuspend={(a) => { setSelectedActivity(a); setModalType("suspend"); }}
        refreshKey={refreshKey}
      />

      {modalType === "create" && (
        <CreateFundraisingActivityPage onClose={closeModal} onSuccess={handleSuccess} />
      )}

      {modalType === "view" && selectedActivity && (
        <ViewFundraisingActivityPage activityId={selectedActivity.id} onClose={closeModal} />
      )}

      {modalType === "edit" && selectedActivity && (
        <UpdateFundraisingActivityPage activity={selectedActivity} onClose={closeModal} onSuccess={handleSuccess} />
      )}

      {modalType === "suspend" && selectedActivity && (
        <SuspendFundraisingActivityPage activity={selectedActivity} onClose={closeModal} onSuccess={handleSuccess} />
      )}
    </DashboardLayout>
  );
}

export default FundraisingActivityPage;
