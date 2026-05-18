import { useEffect, useState } from "react";
import StatusBadge from "../../../components/common/StatusBadge";
import { searchUserProfile } from "../../../api/userProfileApi";

function searchUserProfilePage({ onCreate, onView, onEdit, onSuspend, refreshKey }) {
  const [profiles, setProfiles] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [error, setError] = useState("");

  async function loadProfiles(searchKeyword = "") {
    try {
      setError("");
      const result = await searchUserProfile(searchKeyword);
      setProfiles(result.data || result || []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadProfiles();
  }, []);

  useEffect(() => {
    if (refreshKey > 0) loadProfiles(keyword);
  }, [refreshKey]);

  function onClick(e) {
    const value = e.target.value;
    setKeyword(value);
    loadProfiles(value);
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>User Profiles</h1>
        </div>
        <button className="primary-btn small-btn" onClick={onCreate}>
          +New Profile
        </button>
      </div>

      <div className="divider" />

      <div className="fundraising-toolbar">
        <div className="fundraising-search-wrapper">
          <span className="search-icon">🔍</span>
          <input
            className="fundraising-search-input"
            placeholder="search profiles..."
            value={keyword}
            onChange={onClick}
          />
        </div>
      </div>

      {error && <p className="error-message">{error}</p>}

      <table className="data-table">
        <thead>
          <tr>
            <th>PROFILE</th>
            <th>DESCRIPTION</th>
            <th>STATUS</th>
            <th>ACTIONS</th>
          </tr>
        </thead>
        <tbody>
          {profiles.length === 0 ? (
            <tr>
              <td colSpan="4" className="empty-table-message">
                No matching records found.
              </td>
            </tr>
          ) : (
            profiles.map((profile) => (
              <tr key={profile.id}>
                <td>{profile.name_of_role}</td>
                <td>{profile.description || "-"}</td>
                <td>
                  <StatusBadge status={profile.status} />
                </td>
                <td>
                  <div className="actions">
                    <button onClick={() => onView(profile)}>View</button>
                    <button onClick={() => onEdit(profile)}>EDIT</button>
                    <button
                      className="danger-btn"
                      onClick={() => onSuspend(profile)}
                      disabled={profile.status !== "ACTIVE"}
                    >
                      {profile.status === "ACTIVE" ? "SUSPEND" : "SUSPENDED"}
                    </button>
                  </div>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </>
  );
}

export default searchUserProfilePage;
