import { useEffect, useMemo, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import FundraisingActivityViewModal from "../../components/fundraiser/FundraisingActivityViewModal";
import {
  getCompletedFundraisingActivities,
} from "../../api/fundraisingActivityApi";

function CompletedFundraisingActivityPage({ onLogout, setCurrentPage }) {
  const [activities, setActivities] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [error, setError] = useState("");
  const [selectedActivity, setSelectedActivity] = useState(null);

  async function loadCompletedActivities(searchKeyword = "") {
    try {
      setError("");
      const result = await getCompletedFundraisingActivities(searchKeyword);
      setActivities(result.data || result || []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadCompletedActivities();
  }, []);

  function handleSearchChange(e) {
    const value = e.target.value;
    setKeyword(value);
    loadCompletedActivities(value);
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
      activePage="completedActivities"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="FUNDRAISER"
    >
      <div className="fundraising-page-content">
        <div className="page-header">
          <div>
            <h1>Completed Activities</h1>
          </div>
        </div>

        <div className="divider" />

        <div className="fundraising-toolbar">
          <div className="fundraising-search-wrapper">
            <span className="search-icon">🔍</span>
            <input
              className="fundraising-search-input"
              placeholder="search completed activities..."
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
            <div className="empty-card-state">
              No matching records found.
            </div>
          ) : (
            filteredActivities.map((activity) => {
              const current = Number(activity.current_amount || 0);
              const goal = Number(activity.goal_amount || 0);
              const progress = getProgress(activity);

              return (
                <div className="activity-card" key={activity.id}>
                  <div className="activity-card-main">
                    <div className="activity-card-top">
                      <div className="activity-badges">
                        <span className="activity-category-badge">
                          {activity.category || "CATEGORY"}
                        </span>

                        <span className="activity-status-badge completed">
                          COMPLETED
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
                      <span>Ended {activity.deadline || "-"}</span>
                      <span>{activity.view_count || 0} views</span>
                      <span>{activity.shortlist_count || 0} shortlisted</span>
                    </div>

                    <div className="activity-actions">
                      <button onClick={() => setSelectedActivity(activity)}>
                        View
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
                        <span>COMPLETED</span>
                      </div>
                    </div>

                    <p className="activity-location">
                      {activity.location || "-"}
                    </p>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {selectedActivity && (
          <FundraisingActivityViewModal
            activity={selectedActivity}
            onClose={() => setSelectedActivity(null)}
          />
        )}
      </div>
    </DashboardLayout>
  );
}

export default CompletedFundraisingActivityPage;