import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import StatusBadge from "../../components/common/StatusBadge";
import ConfirmModal from "../../components/userAdmin/ConfirmModal";
import UserAccountFormModal from "../../components/userAdmin/UserAccountFormModal";
import UserAccountViewModal from "../../components/userAdmin/UserAccountViewModal";
import {
  getUserAccounts,
  createUserAccount,
  updateUserAccount,
  suspendUserAccount,
} from "../../api/userAccountApi";

function UserAccountPage({ onLogout, setCurrentPage }) {
  const [accounts, setAccounts] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [error, setError] = useState("");
  const [modalError, setModalError] = useState("");
  const [modalType, setModalType] = useState(null);
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function loadAccounts(searchKeyword = "") {
    try {
      setError("");
      const result = await getUserAccounts(searchKeyword);
      setAccounts(result.data || result || []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadAccounts();
  }, []);

  function closeModal() {
    setModalType(null);
    setSelectedAccount(null);
    setModalError("");
  }

  function openCreateModal() {
    setSelectedAccount(null);
    setModalError("");
    setModalType("create");
  }

  function openViewModal(account) {
    setSelectedAccount(account);
    setModalError("");
    setModalType("view");
  }

  function openEditModal(account) {
    setSelectedAccount(account);
    setModalError("");
    setModalType("edit");
  }

  function openSuspendModal(account) {
    setSelectedAccount(account);
    setModalError("");
    setModalType("suspend");
  }

  async function handleCreate(payload) {
    try {
      setIsSubmitting(true);
      setModalError("");

      await createUserAccount(payload);

      closeModal();
      loadAccounts(keyword);
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

      await updateUserAccount(selectedAccount.id, payload);

      closeModal();
      loadAccounts(keyword);
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

      await suspendUserAccount(selectedAccount.id);

      closeModal();
      loadAccounts(keyword);
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleSearchChange(e) {
    const value = e.target.value;
    setKeyword(value);
    loadAccounts(value);
  }

  return (
    <DashboardLayout
      activePage="accounts"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="USER_ADMIN"
    >
      <div className="page-header">
        <div>
          <h1>User Accounts</h1>
        </div>

        <button className="primary-btn small-btn" onClick={openCreateModal}>
          +New Account
        </button>
      </div>

      <div className="divider" />

      <input
        className="search-input"
        placeholder="search accounts..."
        value={keyword}
        onChange={handleSearchChange}
      />

      {error && <p className="error-message">{error}</p>}

      <table className="data-table">
        <thead>
          <tr>
            <th>NAME</th>
            <th>EMAIL</th>
            <th>PROFILE</th>
            <th>STATUS</th>
            <th>ACTIONS</th>
          </tr>
        </thead>

        <tbody>
          {accounts.length === 0 ? (
            <tr>
              <td colSpan="5" className="empty-table-message">
                No matching records found.
              </td>
            </tr>
          ) : (
            accounts.map((account) => (
              <tr key={account.id}>
                <td>{account.name}</td>
                <td>{account.email}</td>
                <td>{account.name_of_role || "-"}</td>
                <td>
                  <StatusBadge status={account.status} />
                </td>
                <td>
                  <div className="actions">
                    <button onClick={() => openViewModal(account)}>View</button>
                    <button onClick={() => openEditModal(account)}>EDIT</button>
                    <button
                      className="danger-btn"
                      onClick={() => openSuspendModal(account)}
                      disabled={account.status !== "ACTIVE"}
                    >
                      {account.status === "ACTIVE" ? "SUSPEND" : "SUSPENDED"}
                    </button>
                  </div>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      {modalType === "create" && (
        <UserAccountFormModal
          mode="create"
          onClose={closeModal}
          onSubmit={handleCreate}
          error={modalError}
          isSubmitting={isSubmitting}
        />
      )}

      {modalType === "edit" && selectedAccount && (
        <UserAccountFormModal
          mode="edit"
          account={selectedAccount}
          onClose={closeModal}
          onSubmit={handleEdit}
          error={modalError}
          isSubmitting={isSubmitting}
        />
      )}

      {modalType === "view" && selectedAccount && (
        <UserAccountViewModal account={selectedAccount} onClose={closeModal} />
      )}

      {modalType === "suspend" && selectedAccount && (
        <ConfirmModal
          title="Suspend"
          message={`Are you sure you want to suspend the account ${
            selectedAccount.name || selectedAccount.username || selectedAccount.email
          }?`}
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

export default UserAccountPage;