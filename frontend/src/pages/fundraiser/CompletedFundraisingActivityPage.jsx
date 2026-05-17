import { useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import SearchCompletedActivitiesPage from "./completedActivity/searchCompletedActivitiesPage";
import ViewCompletedActivityPage from "./completedActivity/viewCompletedActivityPage";

function CompletedFundraisingActivityPage({ onLogout, setCurrentPage }) {
  const [selectedActivityId, setSelectedActivityId] = useState(null);

  return (
    <DashboardLayout
      activePage="completedActivities"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="FUNDRAISER"
    >
      <div className="fundraising-page-content">
        <SearchCompletedActivitiesPage
          onView={(a) => setSelectedActivityId(a.id)}
          refreshKey={0}
        />

        {selectedActivityId && (
          <ViewCompletedActivityPage
            activityId={selectedActivityId}
            onClose={() => setSelectedActivityId(null)}
          />
        )}
      </div>
    </DashboardLayout>
  );
}

export default CompletedFundraisingActivityPage;
