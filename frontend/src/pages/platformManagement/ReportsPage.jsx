import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import { getReports } from "../../api/reportsApi";

const CHART_COLORS = ["#5c4033", "#c8a84b", "#7a9e7e", "#a0432f", "#2d5a36"];

function PieChart({ data }) {
  const total = data.reduce((s, d) => s + d.amount, 0);
  if (total === 0) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "220px", color: "#999" }}>
        No data
      </div>
    );
  }

  const cx = 110, cy = 110, r = 100;
  let startAngle = -Math.PI / 2;
  const slices = data.map((d, i) => {
    const angle = (d.amount / total) * 2 * Math.PI;
    const endAngle = startAngle + angle;
    const x1 = cx + r * Math.cos(startAngle);
    const y1 = cy + r * Math.sin(startAngle);
    const x2 = cx + r * Math.cos(endAngle);
    const y2 = cy + r * Math.sin(endAngle);
    const largeArc = angle > Math.PI ? 1 : 0;
    const path = `M${cx},${cy} L${x1},${y1} A${r},${r} 0 ${largeArc},1 ${x2},${y2} Z`;
    const slice = { path, color: CHART_COLORS[i % CHART_COLORS.length], name: d.name };
    startAngle = endAngle;
    return slice;
  });

  return (
    <div className="report-chart-box">
      <p className="report-chart-title">RAISED BY CATEGORY</p>
      <div style={{ display: "flex", alignItems: "center", gap: "24px", flexWrap: "wrap" }}>
        <svg width="220" height="220" viewBox="0 0 220 220">
          {slices.map((s, i) => (
            <path key={i} d={s.path} fill={s.color} />
          ))}
        </svg>
        <div className="pie-legend">
          {slices.map((s, i) => (
            <div key={i} className="pie-legend-item">
              <span className="pie-legend-dot" style={{ background: s.color }} />
              <span>{s.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function BarChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "220px", color: "#999" }}>
        No data
      </div>
    );
  }

  const maxViews = Math.max(...data.map((d) => d.view_count), 1);
  const barColor = "#c8a84b";

  return (
    <div className="report-chart-box">
      <p className="report-chart-title">MOST VIEWS ACTIVITIES</p>
      <div className="bar-chart">
        {data.map((d, i) => {
          const pct = (d.view_count / maxViews) * 100;
          const label = d.title.length > 16 ? d.title.slice(0, 14) + "..." : d.title;
          return (
            <div key={i} className="bar-row">
              <span className="bar-label">{label}</span>
              <div className="bar-track">
                <div className="bar-fill" style={{ width: `${pct}%`, background: barColor }} />
              </div>
              <span className="bar-value">{d.view_count}</span>
            </div>
          );
        })}
        <div className="bar-axis">
          {[0, maxViews * 0.25, maxViews * 0.5, maxViews * 0.75, maxViews].map((v, i) => (
            <span key={i}>{Math.round(v)}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

function ReportsPage({ onLogout, setCurrentPage }) {
  const [period, setPeriod] = useState("daily");
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");

  async function loadReport(p) {
    try {
      setError("");
      const data = await getReports(p);
      setReport(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadReport(period);
  }, [period]);

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

      {error && <p className="error-message">{error}</p>}

      {report && (
        <>
          <div className="report-stats-row">
            <div className="report-stat-card">
              <span className="stat-label">RAISED</span>
              <strong className="stat-value">${report.raised.toLocaleString()}</strong>
              <span className="stat-sub">across the platform</span>
            </div>
            <div className="report-stat-card">
              <span className="stat-label">ACTIVE ACTIVITIES</span>
              <strong className="stat-value">{report.active_activities}</strong>
              <span className="stat-sub">across the platform</span>
            </div>
            <div className="report-stat-card">
              <span className="stat-label">COMPLETED ACTIVITIES</span>
              <strong className="stat-value">{report.completed_activities}</strong>
              <span className="stat-sub">across the platform</span>
            </div>
            <div className="report-stat-card">
              <span className="stat-label">VIEWS</span>
              <strong className="stat-value">{report.views.toLocaleString()}</strong>
              <span className="stat-sub">across the platform</span>
            </div>
            <div className="report-stat-card">
              <span className="stat-label">ACTIVE USERS</span>
              <strong className="stat-value">{report.active_users.toLocaleString()}</strong>
              <span className="stat-sub">across the platform</span>
            </div>
          </div>

          <div className="report-charts-row">
            <PieChart data={report.raised_by_category} />
            <BarChart data={report.most_viewed_activities} />
          </div>
        </>
      )}
    </DashboardLayout>
  );
}

export default ReportsPage;
