import { useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import DailyReportPage from "./report/dailyReportPage";
import WeeklyReportPage from "./report/weeklyReportPage";
import MonthlyReportPage from "./report/monthlyReportPage";

function ReportsPage({ onLogout, setCurrentPage }) {
  const [period, setPeriod] = useState("daily");

  return (
    <DashboardLayout
      activePage="reports"
      onLogout={onLogout}
      setCurrentPage={setCurrentPage}
      role="PLATFORM_MANAGER"
    >
      <div className="page-header">
        <h1>Reports</h1>
        <div className="period-tabs">
          {["daily", "weekly", "monthly"].map((p) => (
            <button
              key={p}
              className={period === p ? "period-tab active" : "period-tab"}
              onClick={() => setPeriod(p)}
            >
              {p.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      <div className="divider" />

      {period === "daily" && <DailyReportPage />}
      {period === "weekly" && <WeeklyReportPage />}
      {period === "monthly" && <MonthlyReportPage />}
    </DashboardLayout>
  );
}

export default ReportsPage;
