import { useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import SearchUserAccountPage from "./userAccount/searchUserAccountPage";
import CreateUserAccountPage from "./userAccount/createUserAccountPage";
import ViewUserAccountPage from "./userAccount/viewUserAccountPage";
import UpdateUserAccountPage from "./userAccount/updateUserAccountPage";
import SuspendUserAccountPage from "./userAccount/suspendUserAccountPage";

function UserAccountPage({ onLogout, setCurrentPage }) {
  const [modalType, setModalType] = useState(null);
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  function closeModal() {
    setModalType(null);
    setSelectedAccount(null);
  }

  function handleSuccess() {
    setRefreshKey((k) => k + 1);
  }

  return (
    <DashboardLayout
      activePage="accounts"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="USER_ADMIN"
    >
      <SearchUserAccountPage
        onCreate={() => setModalType("create")}
        onView={(a) => { setSelectedAccount(a); setModalType("view"); }}
        onEdit={(a) => { setSelectedAccount(a); setModalType("edit"); }}
        onSuspend={(a) => { setSelectedAccount(a); setModalType("suspend"); }}
        refreshKey={refreshKey}
      />

      {modalType === "create" && (
        <CreateUserAccountPage onClose={closeModal} onSuccess={handleSuccess} />
      )}

      {modalType === "view" && selectedAccount && (
        <ViewUserAccountPage accountId={selectedAccount.id} onClose={closeModal} />
      )}

      {modalType === "edit" && selectedAccount && (
        <UpdateUserAccountPage account={selectedAccount} onClose={closeModal} onSuccess={handleSuccess} />
      )}

      {modalType === "suspend" && selectedAccount && (
        <SuspendUserAccountPage account={selectedAccount} onClose={closeModal} onSuccess={handleSuccess} />
      )}
    </DashboardLayout>
  );
}

export default UserAccountPage;
