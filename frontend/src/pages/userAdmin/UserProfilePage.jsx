import { useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import SearchUserProfilePage from "./userProfile/searchUserProfilePage";
import CreateUserProfilePage from "./userProfile/createUserProfilePage";
import ViewUserProfilePage from "./userProfile/viewUserProfilePage";
import UpdateUserProfilePage from "./userProfile/updateUserProfilePage";
import SuspendUserProfilePage from "./userProfile/suspendUserProfilePage";

function UserProfilePage({ onLogout, setCurrentPage }) {
  const [modalType, setModalType] = useState(null);
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  function closeModal() {
    setModalType(null);
    setSelectedProfile(null);
  }

  function handleSuccess() {
    setRefreshKey((k) => k + 1);
  }

  return (
    <DashboardLayout
      activePage="profiles"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="USER_ADMIN"
    >
      <SearchUserProfilePage
        onCreate={() => setModalType("create")}
        onView={(p) => { setSelectedProfile(p); setModalType("view"); }}
        onEdit={(p) => { setSelectedProfile(p); setModalType("edit"); }}
        onSuspend={(p) => { setSelectedProfile(p); setModalType("suspend"); }}
        refreshKey={refreshKey}
      />

      {modalType === "create" && (
        <CreateUserProfilePage onClose={closeModal} onSuccess={handleSuccess} />
      )}

      {modalType === "view" && selectedProfile && (
        <ViewUserProfilePage profileId={selectedProfile.id} onClose={closeModal} />
      )}

      {modalType === "edit" && selectedProfile && (
        <UpdateUserProfilePage profile={selectedProfile} onClose={closeModal} onSuccess={handleSuccess} />
      )}

      {modalType === "suspend" && selectedProfile && (
        <SuspendUserProfilePage profile={selectedProfile} onClose={closeModal} onSuccess={handleSuccess} />
      )}
    </DashboardLayout>
  );
}

export default UserProfilePage;