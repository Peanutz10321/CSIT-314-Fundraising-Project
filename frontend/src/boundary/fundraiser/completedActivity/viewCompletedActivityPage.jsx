import { useEffect, useState } from "react";
import FundraisingActivityViewModal from "../../../components/fundraiser/FundraisingActivityViewModal";
import { viewFundraisingActivity } from "../../../api/fundraisingActivityApi";

function viewCompletedActivityPage({ activityId, onClose }) {
  const [activity, setActivity] = useState(null);
  const [error, setError] = useState("");

  function displayCompletedActivities(data) {
    setActivity(data);
  }

  function displayNoData() {
    setError("Activity not found.");
  }

  async function onClick(activityID) {
    try {
      const result = await viewFundraisingActivity(activityID);
      if (result) {
        displayCompletedActivities(result);
      } else {
        displayNoData();
      }
    } catch (err) {
      displayNoData();
    }
  }

  useEffect(() => {
    onClick(activityId);
  }, [activityId]);

  if (error) return <p className="error-message">{error}</p>;
  if (!activity) return null;

  return <FundraisingActivityViewModal activity={activity} onClose={onClose} />;
}

export default viewCompletedActivityPage;
