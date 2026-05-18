import { useEffect, useState } from "react";
import DoneeActivityCard from "../../../components/donee/DoneeActivityCard";
import { doneeSearchFundraisingActivity } from "../../../api/doneeApi";

function searchFundraisingActivityPage({ onView, onSave, refreshKey, favoriteIds }) {
  const [activities, setActivities] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [error, setError] = useState("");

  async function displaySearchResults(searchKeyword = "") {
    try {
      setError("");
      const result = await doneeSearchFundraisingActivity(searchKeyword);
      setActivities(result.data || result || []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    displaySearchResults();
  }, []);

  useEffect(() => {
    if (refreshKey > 0) displaySearchResults(keyword);
  }, [refreshKey]);

  function onClick(e) {
    const value = e.target.value;
    setKeyword(value);
    displaySearchResults(value);
  }

  return (
    <>
      <div className="page-header donee-page-header">
        <div><h1>Browse Activities</h1></div>
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
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="activity-card-list">
        {activities.length === 0 ? (
          <div className="empty-card-state">No matching activities found.</div>
        ) : (
          activities.map((activity) => (
            <DoneeActivityCard
              key={activity.id}
              activity={activity}
              mode="browse"
              onView={onView}
              onSave={onSave}
              isSaved={(favoriteIds || []).includes(String(activity.id))}
            />
          ))
        )}
      </div>
    </>
  );
}

export default searchFundraisingActivityPage;
