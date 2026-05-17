import { useEffect, useState } from "react";
import StatusBadge from "../../../components/common/StatusBadge";
import { searchCategory } from "../../../api/categoryApi";

function searchFundraisingCategoryPage({ onCreate, onView, onEdit, onSuspend, refreshKey }) {
  const [categories, setCategories] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [error, setError] = useState("");

  async function displayResults(query = "") {
    try {
      setError("");
      const result = await searchCategory(query);
      setCategories(result.data || result || []);
    } catch (err) {
      setError(err.message);
    }
  }

  function displayNoData() {
    return <div className="empty-card-state">No matching categories found.</div>;
  }

  useEffect(() => {
    displayResults();
  }, []);

  useEffect(() => {
    if (refreshKey > 0) displayResults(keyword);
  }, [refreshKey]);

  function onClick(e) {
    const value = e.target.value;
    setKeyword(value);
    displayResults(value);
  }

  return (
    <>
      <div className="page-header">
        <h1>Activity Categories</h1>
        <button className="primary-btn small-btn" onClick={onCreate}>+New Category</button>
      </div>

      <div className="divider" />

      <div className="fundraising-search-wrapper" style={{ marginBottom: "24px", maxWidth: "1200px" }}>
        <span className="search-icon">🔍</span>
        <input
          className="fundraising-search-input"
          placeholder="search categories..."
          value={keyword}
          onChange={onClick}
        />
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="category-card-grid">
        {categories.length === 0 ? displayNoData() : (
          categories.map((cat) => (
            <div className="category-card" key={cat.id}>
              <div className="category-card-header">
                <span className="category-card-name">{cat.name}</span>
                <StatusBadge status={cat.status} />
              </div>
              <p className="category-card-desc">{cat.description || "-"}</p>
              <div className="category-card-footer">
                <span className="category-activity-count">{cat.activity_count ?? 0} activities</span>
                <div className="actions">
                  <button onClick={() => onView(cat)}>View</button>
                  <button onClick={() => onEdit(cat)}>EDIT</button>
                  <button
                    className="danger-btn"
                    onClick={() => onSuspend(cat)}
                    disabled={cat.status !== "ACTIVE"}
                  >
                    {cat.status === "ACTIVE" ? "SUSPEND" : "SUSPENDED"}
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </>
  );
}

export default searchFundraisingCategoryPage;
