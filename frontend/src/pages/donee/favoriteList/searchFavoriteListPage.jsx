import { useEffect, useState } from "react";
import DoneeActivityCard from "../../../components/donee/DoneeActivityCard";
import { searchFavoriteList } from "../../../api/doneeApi";

function searchFavoriteListPage({ keyword, onView }) {
  const [activities, setActivities] = useState([]);
  const [error, setError] = useState("");

  async function onClick(searchKeyword) {
    try {
      setError("");
      const result = await searchFavoriteList(searchKeyword);
      setActivities(result.data || result || []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    onClick(keyword);
  }, [keyword]);

  if (error) return <p className="error-message">{error}</p>;

  return (
    <div className="activity-card-list">
      {activities.length === 0 ? (
        <div className="empty-card-state">No matching activities found.</div>
      ) : (
        activities.map((activity) => (
          <DoneeActivityCard
            key={activity.id}
            activity={activity}
            mode="favorites"
            onView={onView}
            onSave={() => {}}
            isSaved={true}
          />
        ))
      )}
    </div>
  );
}

export default searchFavoriteListPage;
