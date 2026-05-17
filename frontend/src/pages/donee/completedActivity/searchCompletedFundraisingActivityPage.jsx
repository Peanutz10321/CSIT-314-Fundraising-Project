import { useEffect, useState } from "react";
import DoneeActivityCard from "../../../components/donee/DoneeActivityCard";
import { searchCompletedActivity } from "../../../api/doneeApi";

function searchCompletedFundraisingActivityPage({ keyword, onView }) {
  const [activities, setActivities] = useState([]);
  const [error, setError] = useState("");

  async function onClick(query) {
    try {
      setError("");
      const result = await searchCompletedActivity(query);
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
            mode="completed"
            onView={onView}
            onSave={() => {}}
            isSaved={false}
          />
        ))
      )}
    </div>
  );
}

export default searchCompletedFundraisingActivityPage;
