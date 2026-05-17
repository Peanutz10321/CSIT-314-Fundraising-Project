import { useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import ViewCompletedFundraisingActivityPage from "./completedActivity/viewCompletedFundraisingActivityPage";
import SearchCompletedFundraisingActivityPage from "./completedActivity/searchCompletedFundraisingActivityPage";
import ViewFundraisingActivityPage from "./browseActivity/viewFundraisingActivityPage";

function DoneeCompletedActivitiesPage({ onLogout, setCurrentPage }) {
  const [keyword, setKeyword] = useState("");
  const [selectedActivity, setSelectedActivity] = useState(null);

  return (
    <DashboardLayout
      activePage="doneeCompleted"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="DONEE"
    >
      <div className="page-header donee-page-header">
        <div><h1>Completed Activities</h1></div>
      </div>

      <div className="divider" />

      <div className="fundraising-toolbar">
        <div className="fundraising-search-wrapper">
          <span className="search-icon">🔍</span>
          <input
            className="fundraising-search-input"
            placeholder="search completed activities..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
          />
        </div>
      </div>

      {keyword
        ? <SearchCompletedFundraisingActivityPage keyword={keyword} onView={(a) => setSelectedActivity(a)} />
        : <ViewCompletedFundraisingActivityPage onView={(a) => setSelectedActivity(a)} />
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

export default DoneeCompletedActivitiesPage;
