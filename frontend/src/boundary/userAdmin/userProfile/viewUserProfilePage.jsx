import { useEffect, useState } from "react";
import UserProfileViewModal from "../../../components/userAdmin/UserProfileViewModal";
import { getUserProfileByID } from "../../../api/userProfileApi";

function viewUserProfilePage({ profileId, onClose }) {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");

  async function onClick(profileID) {
    try {
      const result = await getUserProfileByID(profileID);
      setProfile(result);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    onClick(profileId);
  }, [profileId]);

  if (error) return <p className="error-message">{error}</p>;
  if (!profile) return null;

  return <UserProfileViewModal profile={profile} onClose={onClose} />;
}

export default viewUserProfilePage;
