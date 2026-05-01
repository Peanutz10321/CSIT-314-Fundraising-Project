import { useEffect, useMemo, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import ConfirmModal from "../../components/userAdmin/ConfirmModal";
import FundraisingActivityFormModal from "../../components/fundraiser/FundraisingActivityFormModal";
import FundraisingActivityViewModal from "../../components/fundraiser/FundraisingActivityViewModal";
import {
  getFundraisingActivities,
  createFundraisingActivity,
  updateFundraisingActivity,
  suspendFundraisingActivity,
} from "../../api/fundraisingActivityApi";

function FundraisingActivityPage({ onLogout, setCurrentPage }) {
  const [activities, setActivities] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [error, setError] = useState("");
  const [modalError, setModalError] = useState("");
  const [modalType, setModalType] = useState(null);
  const [selectedActivity, setSelectedActivity] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function loadActivities(searchKeyword = "") {
    try {
      setError("");
      const result = await getFundraisingActivities(searchKeyword);
      setActivities(result.data || result || []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadActivities();
  }, []);

  function closeModal() {
    setModalType(null);
    setSelectedActivity(null);
    setModalError("");
  }

  function openCreateModal() {
    setSelectedActivity(null);
    setModalError("");
    setModalType("create");
  }

  function openViewModal(activity) {
    setSelectedActivity(activity);
    setModalError("");
    setModalType("view");
  }

  function openEditModal(activity) {
    setSelectedActivity(activity);
    setModalError("");
    setModalType("edit");
  }

  function openSuspendModal(activity) {
    setSelectedActivity(activity);
    setModalError("");
    setModalType("suspend");
  }

  async function handleCreate(payload) {
    try {
      setIsSubmitting(true);
      setModalError("");
      await createFundraisingActivity(payload);
      closeModal();
      loadActivities(keyword);
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
      await updateFundraisingActivity(selectedActivity.id, payload);
      closeModal();
      loadActivities(keyword);
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
      await suspendFundraisingActivity(selectedActivity.id);
      closeModal();
      loadActivities(keyword);
    } catch (err) {
      setModalError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleSearchChange(e) {
    const value = e.target.value;
    setKeyword(value);
    loadActivities(value);
  }

  const filteredActivities = useMemo(() => {
    if (!selectedCategory) return activities;
    return activities.filter(
      (activity) =>
        (activity.category || "").toLowerCase() === selectedCategory.toLowerCase()
    );
  }, [activities, selectedCategory]);

  function getProgress(activity) {
    const current = Number(activity.current_amount || 0);
    const goal = Number(activity.goal_amount || 0);
    if (goal <= 0) return 0;
    return Math.min((current / goal) * 100, 100);
  }

  return (
    <DashboardLayout
      activePage="fundraisingActivities"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="FUNDRAISER"
    >
      <div className="page-header">
        <div>
          <h1>Fundraising Activities</h1>
        </div>

        <button className="primary-btn small-btn" onClick={openCreateModal}>
          +New Activity
        </button>
      </div>

      <div className="divider" />

      <div className="fundraising-toolbar">
        <div className="fundraising-search-wrapper">
          <span className="search-icon">🔍</span>
          <input
            className="fundraising-search-input"
            placeholder="search activities..."
            value={keyword}
            onChange={handleSearchChange}
          />
        </div>

        <select
          className="fundraising-category-filter"
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          <option value="">All categories</option>
          <option value="Community">Community</option>
          <option value="Education">Education</option>
          <option value="Medical">Medical</option>
          <option value="Healthcare">Healthcare</option>
          <option value="Emergency">Emergency</option>
        </select>
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="activity-card-list">
        {filteredActivities.length === 0 ? (
          <div className="empty-card-state">No matching records found.</div>
        ) : (
          filteredActivities.map((activity) => {
            const current = Number(activity.current_amount || 0);
            const goal = Number(activity.goal_amount || 0);
            const progress = getProgress(activity);
            const remaining = Math.max(100 - Math.round(progress), 0);

            return (
              <div className="activity-card" key={activity.id}>
                <div className="activity-card-main">
                  <div className="activity-card-top">
                    <div className="activity-badges">
                      <span className="activity-category-badge">
                        {activity.category || "CATEGORY"}
                      </span>

                      <span
                        className={`activity-status-badge ${
                          activity.status === "ACTIVE"
                            ? "active"
                            : "suspended"
                        }`}
                      >
                        {activity.status}
                      </span>
                    </div>

                    <div className="activity-beneficiary">
                      {activity.beneficiaryName || "-"}
                    </div>
                  </div>

                  <h3 className="activity-title">{activity.title}</h3>

                  <p className="activity-description-text">
                    {activity.description || "-"}
                  </p>

                  <div className="activity-meta-row">
                    <span>Ends {activity.deadline || "-"}</span>
                    <span>{activity.view_count || 0} views</span>
                    <span>{activity.shortlist_count || 0} shortlisted</span>
                  </div>

                  <div className="activity-actions">
                    <button onClick={() => openViewModal(activity)}>View</button>
                    <button onClick={() => openEditModal(activity)}>EDIT</button>
                    <button
                      className="danger-btn"
                      onClick={() => openSuspendModal(activity)}
                      disabled={activity.status !== "ACTIVE"}
                    >
                      {activity.status === "ACTIVE" ? "SUSPEND" : "SUSPENDED"}
                    </button>
                  </div>
                </div>

                <div className="activity-card-side">
                  <p className="raised-label">RAISED</p>
                  <h3 className="raised-amount">
                    {activity.currency || "$"}
                    {current}
                  </h3>
                  <p className="raised-goal-text">
                    of {activity.currency || "$"}
                    {goal} goal
                  </p>

                  <div className="activity-progress-wrap">
                    <div className="activity-progress-track">
                      <div
                        className="activity-progress-fill"
                        style={{ width: `${progress}%` }}
                      />
                    </div>

                    <div className="activity-progress-labels">
                      <span>{Math.round(progress)}%</span>
                      <span>{remaining}% TO GO</span>
                    </div>
                  </div>

                  <p className="activity-location">{activity.location || "-"}</p>
                </div>
              </div>
            );
          })
        )}
      </div>

      {modalType === "create" && (
        <FundraisingActivityFormModal
          mode="create"
          onClose={closeModal}
          onSubmit={handleCreate}
          error={modalError}
          isSubmitting={isSubmitting}
        />
      )}

      {modalType === "edit" && selectedActivity && (
        <FundraisingActivityFormModal
          mode="edit"
          activity={selectedActivity}
          onClose={closeModal}
          onSubmit={handleEdit}
          error={modalError}
          isSubmitting={isSubmitting}
        />
      )}

      {modalType === "view" && selectedActivity && (
        <FundraisingActivityViewModal
          activity={selectedActivity}
          onClose={closeModal}
        />
      )}

      {modalType === "suspend" && selectedActivity && (
        <ConfirmModal
          title="Suspend"
          message={`Are you sure you want to suspend the activity ${selectedActivity.title}?`}
          confirmText={
            selectedActivity.status === "ACTIVE" ? "SUSPEND" : "REACTIVATE"
          }
          onClose={closeModal}
          onConfirm={handleSuspend}
          error={modalError}
          isSubmitting={isSubmitting}
        />
      )}
    </DashboardLayout>
  );
}

export default FundraisingActivityPage;