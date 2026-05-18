import { useEffect, useRef, useState } from "react";
import FundraisingActivityViewModal from "../../../components/fundraiser/FundraisingActivityViewModal";
import { doneeViewFundraisingActivity } from "../../../api/doneeApi";

function viewFundraisingActivityPage({ activityId, onClose }) {
  const [activity, setActivity] = useState(null);
  const [error, setError] = useState("");
  const hasFetched = useRef(false);

  useEffect(() => {
    if (hasFetched.current) return;
    hasFetched.current = true;

    doneeViewFundraisingActivity(activityId)
      .then((result) => setActivity(result))
      .catch((err) => setError(err.message));
  }, [activityId]);

  if (error) return <p className="error-message">{error}</p>;
  if (!activity) return null;

  return <FundraisingActivityViewModal activity={activity} onClose={onClose} role="DONEE" />;
}

export default viewFundraisingActivityPage;
