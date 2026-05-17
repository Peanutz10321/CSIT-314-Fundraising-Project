import { useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import ViewFavoriteListPage from "./favoriteList/viewFavoriteListPage";
import SearchFavoriteListPage from "./favoriteList/searchFavoriteListPage";
import ViewFundraisingActivityPage from "./browseActivity/viewFundraisingActivityPage";

function DoneeFavoritesPage({ onLogout, setCurrentPage }) {
  const [keyword, setKeyword] = useState("");
  const [selectedActivity, setSelectedActivity] = useState(null);

  return (
    <DashboardLayout
      activePage="doneeFavorites"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="DONEE"
    >
      <div className="page-header donee-page-header">
        <div><h1>My Favorites</h1></div>
      </div>

      <div className="divider" />

      <div className="fundraising-toolbar">
        <div className="fundraising-search-wrapper">
          <span className="search-icon">🔍</span>
          <input
            className="fundraising-search-input"
            placeholder="search favorites..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
          />
        </div>
      </div>

      {keyword
        ? <SearchFavoriteListPage keyword={keyword} onView={(a) => setSelectedActivity(a)} />
        : <ViewFavoriteListPage onView={(a) => setSelectedActivity(a)} />
      }

      {selectedActivity && (
        <ViewFundraisingActivityPage
          activityId={selectedActivity.id}
          onClose={() => setSelectedActivity(null)}
        />
      )}
    </DashboardLayout>
  );
}

export default DoneeFavoritesPage;
