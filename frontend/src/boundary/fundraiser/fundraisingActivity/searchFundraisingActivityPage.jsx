import { useEffect, useMemo, useState } from "react";
import { searchFundraisingActivities } from "../../../api/fundraisingActivityApi";
import { getActiveCategories } from "../../../api/categoryApi";

function getCurrentUserId() {
  return localStorage.getItem("userId");
}

function activityBelongsToCurrentFundraiser(activity) {
  const currentUserId = getCurrentUserId();
  if (!currentUserId) return true;
  const possibleOwnerIds = [
    activity.fundraiser_id, activity.fundraiserId,
    activity.user_account_id, activity.userAccountId,
    activity.created_by, activity.owner_id,
  ].filter((v) => v !== undefined && v !== null);
  if (possibleOwnerIds.length === 0) return true;
  return possibleOwnerIds.some((id) => String(id) === String(currentUserId));
}

function getProgress(activity) {
  const current = Number(activity.current_amount || 0);
  const goal = Number(activity.goal_amount || 0);
  if (goal <= 0) return 0;
  return Math.min((current / goal) * 100, 100);
}

function searchFundraisingActivityPage({ onCreate, onView, onEdit, onSuspend, refreshKey }) {
  const [activities, setActivities] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [availableCategories, setAvailableCategories] = useState([]);
  const [error, setError] = useState("");

  async function displaySearchResults(searchKeyword = "") {
    try {
      setError("");
      const result = await searchFundraisingActivities(searchKeyword);
      setActivities((result.data || result || []).filter(activityBelongsToCurrentFundraiser));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    displaySearchResults();
    getActiveCategories()
      .then((res) => setAvailableCategories((res.data || []).filter((c) => c.status === "ACTIVE")))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (refreshKey > 0) displaySearchResults(keyword);
  }, [refreshKey]);

  function enterSearchCriteria(criteria) {
    setKeyword(criteria);
    displaySearchResults(criteria);
  }

  function onClick(e) {
    enterSearchCriteria(e.target.value);
  }

  const filteredActivities = useMemo(() => {
    if (!selectedCategory) return activities;
    return activities.filter(
      (a) => (a.category || "").toLowerCase() === selectedCategory.toLowerCase()
    );
  }, [activities, selectedCategory]);

  return (
    <>
      <div className="page-header">
        <div><h1>Fundraising Activities</h1></div>
        <button className="primary-btn small-btn" onClick={onCreate}>+New Activity</button>
      </div>

      <div className="divider" />

      <div className="fundraising-toolbar">
        <div className="fundraising-search-wrapper">
          <span className="search-icon">🔍</span>
          <input
            className="fundraising-search-input"
            placeholder="search activities..."
            value={keyword}
            onChange={onClick}
          />
        </div>
        <select
          className="fundraising-category-filter"
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          <option value="">All categories</option>
          {availableCategories.map((c) => (
            <option key={c.id} value={c.name}>{c.name}</option>
          ))}
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
                      <span className="activity-category-badge">{activity.category || "CATEGORY"}</span>
                      <span className={`activity-status-badge ${activity.status === "ACTIVE" ? "active" : "suspended"}`}>
                        {activity.status}
                      </span>
                    </div>
                    <div className="activity-beneficiary">{activity.beneficiaryName || "-"}</div>
                  </div>
                  <h3 className="activity-title">{activity.title}</h3>
                  <p className="activity-description-text">{activity.description || "-"}</p>
                  <div className="activity-meta-row">
                    <span>Ends {activity.deadline || "-"}</span>
                    <span>{activity.view_count || 0} views</span>
                    <span>{activity.shortlist_count || 0} shortlisted</span>
                  </div>
                  <div className="activity-actions">
                    <button onClick={() => onView(activity)}>View</button>
                    <button onClick={() => onEdit(activity)}>EDIT</button>
                    <button
                      className="danger-btn"
                      onClick={() => onSuspend(activity)}
                      disabled={activity.status !== "ACTIVE"}
                    >
                      {activity.status === "ACTIVE" ? "SUSPEND" : "SUSPENDED"}
                    </button>
                  </div>
                </div>
                <div className="activity-card-side">
                  <p className="raised-label">RAISED</p>
                  <h3 className="raised-amount">{activity.currency || "$"}{current}</h3>
                  <p className="raised-goal-text">of {activity.currency || "$"}{goal} goal</p>
                  <div className="activity-progress-wrap">
                    <div className="activity-progress-track">
                      <div className="activity-progress-fill" style={{ width: `${progress}%` }} />
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
    </>
  );
}

export default searchFundraisingActivityPage;
