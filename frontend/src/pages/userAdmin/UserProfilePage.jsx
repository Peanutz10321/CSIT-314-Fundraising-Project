import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import StatusBadge from "../../components/common/StatusBadge";
import UserProfileFormModal from "../../components/userAdmin/UserProfileFormModal";
import UserProfileViewModal from "../../components/userAdmin/UserProfileViewModal";
import ConfirmModal from "../../components/userAdmin/ConfirmModal";
import {
  getUserProfiles,
  createUserProfile,
  updateUserProfile,
  suspendUserProfile,
} from "../../api/userProfileApi";

function UserProfilePage({ onLogout , setCurrentPage}) {
  const [profiles, setProfiles] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [error, setError] = useState("");

  const [selectedProfile, setSelectedProfile] = useState(null);
  const [modalType, setModalType] = useState(null); 
  const [modalError, setModalError] = useState("");

  const [isSubmitting, setIsSubmitting] = useState(false);

  async function loadProfiles(searchKeyword = "") {
    try {
      setError("");
      const result = await getUserProfiles(searchKeyword);
      setProfiles(result.data || result || []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadProfiles();
  }, []);

  function closeModal() {
    setModalType(null);
    setSelectedProfile(null);
    setModalError("");
  }

  function openCreateModal() {
    setSelectedProfile(null);
    setModalError("");
    setModalType("create");
  }

  function openEditModal(profile) {
    setSelectedProfile(profile);
    setModalError("");
    setModalType("edit");
  }

  async function handleCreate(payload) {
    try {
      setIsSubmitting(true);
      setModalError("");

      await createUserProfile(payload);
      closeModal();
      loadProfiles(keyword);
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
      await updateUserProfile(selectedProfile.id, payload);
      closeModal();
      loadProfiles(keyword);
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
      await suspendUserProfile(selectedProfile.id);
      closeModal();
      loadProfiles(keyword);
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleSearchChange(e) {
    const value = e.target.value;
    setKeyword(value);
    loadProfiles(value);
  }

  return (
    <DashboardLayout
      activePage="profiles"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="USER_ADMIN"
    >
      <div className="page-header">
        <div>
          <h1>User Profiles</h1>
        </div>

        <button
          className="primary-btn small-btn"
          onClick={openCreateModal}
        >
          +New Profile
        </button>
      </div>

      <div className="divider" />

      <input
        className="search-input"
        placeholder="search profiles..."
        value={keyword}
        onChange={handleSearchChange}
      />

      {error && <p className="error-message">{error}</p>}

      <table className="data-table">
        <thead>
          <tr>
            <th>PROFILE</th>
            <th>DESCRIPTION</th>
            <th>STATUS</th>
            <th>ACTIONS</th>
          </tr>
        </thead>

        <tbody>
          {profiles.length === 0 ? (
            <tr>
              <td colSpan="4" className="empty-table-message">
                No matching records found.
              </td>
            </tr>
          ) : (
            profiles.map((profile) => (
              <tr key={profile.id}>
                <td>{profile.name_of_role}</td>
                <td>{profile.description || "-"}</td>
                <td>
                  <StatusBadge status={profile.status} />
                </td>
                <td>
                  <div className="actions">
                    <button onClick={() => openViewModal(profile)}>View</button>
                    <button onClick={() => openEditModal(profile)}>EDIT</button>
                    <button
                      className="danger-btn"
                      onClick={() => openSuspendModal(profile)}
                      disabled={profile.status !== "ACTIVE"}
                    >
                      {profile.status === "ACTIVE" ? "SUSPEND" : "SUSPENDED"}
                    </button>
                  </div>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      {modalType === "create" && (
        <UserProfileFormModal
          mode="create"
          onClose={closeModal}
          onSubmit={handleCreate}
          error={modalError}
          isSubmitting={isSubmitting}
        />
      )}

      {modalType === "edit" && selectedProfile && (
        <UserProfileFormModal
          mode="edit"
          profile={selectedProfile}
          onClose={closeModal}
          onSubmit={handleEdit}
          error={modalError}
          isSubmitting={isSubmitting}
        />
      )}

      {modalType === "view" && selectedProfile && (
        <UserProfileViewModal
          profile={selectedProfile}
          onClose={closeModal}
        />
      )}

      {modalType === "suspend" && selectedProfile && (
        <ConfirmModal
          title="Suspend"
          message={`Are you sure you want to suspend the profile ${selectedProfile.name_of_role}?`}
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

export default UserProfilePage;