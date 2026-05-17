import { useEffect, useState } from "react";
import FundraisingActivityViewModal from "../../../components/fundraiser/FundraisingActivityViewModal";
import { doneeViewFundraisingActivity } from "../../../api/doneeApi";

function viewFundraisingActivityPage({ activityId, onClose }) {
  const [activity, setActivity] = useState(null);
  const [error, setError] = useState("");

  async function onClick(activityID) {
    try {
      const result = await doneeViewFundraisingActivity(activityID);
      setActivity(result);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    onClick(activityId);
  }, [activityId]);

  if (error) return <p className="error-message">{error}</p>;
  if (!activity) return null;

  return <FundraisingActivityViewModal activity={activity} onClose={onClose} role="DONEE" />;
}

export default viewFundraisingActivityPage;
