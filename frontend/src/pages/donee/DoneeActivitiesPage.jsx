import { useEffect, useMemo, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import DoneeActivityCard from "../../components/donee/DoneeActivityCard";
import FundraisingActivityViewModal from "../../components/fundraiser/FundraisingActivityViewModal";
import {
  getBrowseActivities,
  getCompletedActivities,
  getFavoriteActivities,
  saveActivity,
  viewActivity,
  viewCompletedActivity,
} from "../../api/doneeApi";
import { getActiveCategories } from "../../api/categoryApi";

function getActivityStatus(activity) {
  return String(activity.status || "").toUpperCase();
}

function isOngoingActivity(activity) {
  const status = getActivityStatus(activity);
  return status === "ACTIVE" || status === "ONGOING";
}

function isCompletedActivity(activity) {
  return getActivityStatus(activity) === "COMPLETED";
}

function filterActivitiesByMode(list, mode) {
  const activities = Array.isArray(list) ? list : [];

  if (mode === "completed") {
    return activities.filter(isCompletedActivity);
  }

  return activities.filter(isOngoingActivity);
}

function getPageTitle(mode) {
  if (mode === "favorites") return "My Favorites Activities";
  if (mode === "completed") return "Completed Activities";
  return "Browse Activities";
}

function DoneeActivitiesPage({ mode = "browse", onLogout, setCurrentPage }) {
  const [activities, setActivities] = useState([]);
  const [favoriteIds, setFavoriteIds] = useState([]);
  const [categories, setCategories] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [error, setError] = useState("");
  const [selectedActivity, setSelectedActivity] = useState(null); 

  const activePage =
    mode === "favorites"
      ? "doneeFavorites"
      : mode === "completed"
      ? "doneeCompleted"
      : "doneeBrowse";

  async function loadActivities(searchKeyword = keyword) {
    try {
      setError("");
      setActivities([]);

      let result;
      if (mode === "favorites") {
        result = await getFavoriteActivities(searchKeyword);
      } else if (mode === "completed") {
        result = await getCompletedActivities(searchKeyword);
      } else {
        result = await getBrowseActivities(searchKeyword);
      }

      setActivities(filterActivitiesByMode(result.data || result || [], mode));
    } catch (err) {
      setError(err.message);
    }
  }

  function getActivityId(activity) {
    return String(
      activity.activity_id ??
      activity.fundraising_activity_id ??
      activity.fundraisingActivityId ??
      activity.id
    );
  }

  async function loadFavorites() {

    try {
      const result = await getFavoriteActivities();
      setFavoriteIds((result.data || []).map(getActivityId).filter(Boolean));
    } catch {
      setFavoriteIds([]);
    }
  }

  useEffect(() => {
    loadActivities("");
    loadFavorites();
    getActiveCategories()
      .then((res) => setCategories((res.data || []).filter((c) => c.status === "ACTIVE")))
      .catch(() => {});
  }, [mode]);

  function handleSearchChange(e) {
    const value = e.target.value;
    setKeyword(value);
    loadActivities(value);
  }

  function closeViewModal() {
    setSelectedActivity(null);
  }

  function getViewCount(activity) {
    return Number(activity?.view_count ?? activity?.views ?? activity?.viewCount ?? 0);
  }

  async function handleView(activity) {
    try {
      setError("");

      const result =
        mode === "completed"
          ? await viewCompletedActivity(activity.id)
          : await viewActivity(activity.id);

      const activityDetails = result?.data || result || {};
      const previousViewCount = getViewCount(activity);
      const returnedViewCount = getViewCount(activityDetails);

      const nextViewCount =
        mode === "completed"
          ? Math.max(previousViewCount, returnedViewCount)
          : Math.max(previousViewCount + 1, returnedViewCount);

      const updatedActivity = {
        ...activity,
        ...activityDetails,
        view_count: nextViewCount,
        views: nextViewCount,
      };

      setSelectedActivity(updatedActivity);

      setActivities((previousActivities) =>
        previousActivities.map((item) =>
          String(item.id) === String(activity.id) ? updatedActivity : item
        )
      );
    } catch (err) {
      setError(err.message);
      setSelectedActivity(activity);
    }
  }

  async function handleSave(activity) {
    try {

      const activityId = String(activity.id);

      setFavoriteIds((previousIds) =>
        previousIds.includes(activityId) ? previousIds : [...previousIds, activityId]
      );

      setActivities((previousActivities) =>
        previousActivities.map((item) =>
          String(item.id) === activityId
            ? {
                ...item,
                shortlist_count: Number(item.shortlist_count || 0) + 1,
              }
            : item
        )
      );

      await saveActivity(activity.id);

      if (mode === "favorites") {
        await loadActivities(keyword);
      }
    } catch (err) {
      setError(err.message);

      // If backend says it was already saved, keep the button as SAVED.
      if (String(err.message || "").toLowerCase().includes("already saved")) {
        setFavoriteIds((previousIds) =>
          previousIds.includes(String(activity.id))
            ? previousIds
            : [...previousIds, String(activity.id)]
        );
      }
    }
  }

  const filteredActivities = useMemo(() => {
    if (!selectedCategory) return activities;
    return activities.filter(
      (activity) =>
        (activity.category || "").toLowerCase() === selectedCategory.toLowerCase()
    );
  }, [activities, selectedCategory]);

  return (
    <DashboardLayout
      activePage={activePage}
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="DONEE"
    >
      <div className="page-header donee-page-header">
        <div>
          <h1>{getPageTitle(mode)}</h1>
        </div>
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

        {mode === "browse" && (
          <select
            className="fundraising-category-filter"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            <option value="">All categories</option>
            {categories.map((category) => (
              <option key={category.id} value={category.name}>
                {category.name}
              </option>
            ))}
          </select>
        )}
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="activity-card-list">
        {filteredActivities.length === 0 ? (
          <div className="empty-card-state">No matching activities found.</div>
        ) : (
          filteredActivities.map((activity) => (
            <DoneeActivityCard
              key={activity.id}
              activity={activity}
              mode={mode}
              onView={handleView}
              onSave={handleSave}
              isSaved={favoriteIds.includes(String(activity.id))}
            />
          ))
        )}
      </div>

      {selectedActivity && (
        <FundraisingActivityViewModal
          activity={selectedActivity}
          onClose={closeViewModal}
          role="DONEE"
        />
      )}
    </DashboardLayout>
  );
}

export default DoneeActivitiesPage;
