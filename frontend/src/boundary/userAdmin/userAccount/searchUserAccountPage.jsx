import { useEffect, useState } from "react";
import StatusBadge from "../../../components/common/StatusBadge";
import { searchUserAccount } from "../../../api/userAccountApi";

function searchUserAccountPage({ onCreate, onView, onEdit, onSuspend, refreshKey }) {
  const [accounts, setAccounts] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [error, setError] = useState("");

  async function loadAccounts(searchKeyword = "") {
    try {
      setError("");
      const result = await searchUserAccount(searchKeyword);
      setAccounts(result.data || result || []);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadAccounts();
  }, []);

  useEffect(() => {
    if (refreshKey > 0) loadAccounts(keyword);
  }, [refreshKey]);

  function onClick(e) {
    const value = e.target.value;
    setKeyword(value);
    loadAccounts(value);
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>User Accounts</h1>
        </div>
        <button className="primary-btn small-btn" onClick={onCreate}>
          +New Account
        </button>
      </div>

      <div className="divider" />

      <div className="fundraising-toolbar">
        <div className="fundraising-search-wrapper">
          <span className="search-icon">🔍</span>
          <input
            className="fundraising-search-input"
            placeholder="search accounts..."
            value={keyword}
            onChange={onClick}
          />
        </div>
      </div>

      {error && <p className="error-message">{error}</p>}

      <table className="data-table">
        <thead>
          <tr>
            <th>NAME</th>
            <th>EMAIL</th>
            <th>PROFILE</th>
            <th>STATUS</th>
            <th>ACTIONS</th>
          </tr>
        </thead>
        <tbody>
          {accounts.length === 0 ? (
            <tr>
              <td colSpan="5" className="empty-table-message">
                No matching records found.
              </td>
            </tr>
          ) : (
            accounts.map((account) => (
              <tr key={account.id}>
                <td>{account.name}</td>
                <td>{account.email}</td>
                <td>{account.name_of_role || "-"}</td>
                <td>
                  <StatusBadge status={account.status} />
                </td>
                <td>
                  <div className="actions">
                    <button onClick={() => onView(account)}>View</button>
                    <button onClick={() => onEdit(account)}>EDIT</button>
                    <button
                      className="danger-btn"
                      onClick={() => onSuspend(account)}
                      disabled={account.status !== "ACTIVE"}
                    >
                      {account.status === "ACTIVE" ? "SUSPEND" : "SUSPENDED"}
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

export default searchUserAccountPage;
