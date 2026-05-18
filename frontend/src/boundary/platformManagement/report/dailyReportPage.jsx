import { useEffect, useState } from "react";
import { generateDailyReport } from "../../../api/reportsApi";

const CHART_COLORS = ["#5c4033", "#c8a84b", "#7a9e7e", "#a0432f", "#2d5a36"];

function PieChart({ data }) {
  const totalRaised = data.reduce((sum, d) => sum + Number(d.total_raised || 0), 0);
  const useActivityCountFallback = totalRaised <= 0;
  const total = data.reduce(
    (sum, d) => sum + (useActivityCountFallback ? Number(d.activity_count || 0) : Number(d.total_raised || 0)),
    0
  );

  if (!data.length || total <= 0) return <p className="empty-chart-message">No category data yet</p>;

  const cx = 110, cy = 110, r = 100;
  const slices = data.reduce((acc, d, i) => {
    const value = useActivityCountFallback ? Number(d.activity_count || 0) : Number(d.total_raised || 0);
    const angle = (value / total) * 2 * Math.PI;
    const endAngle = acc.startAngle + angle;
    const x1 = cx + r * Math.cos(acc.startAngle), y1 = cy + r * Math.sin(acc.startAngle);
    const x2 = cx + r * Math.cos(endAngle), y2 = cy + r * Math.sin(endAngle);
    const largeArc = angle > Math.PI ? 1 : 0;
    return {
      startAngle: endAngle,
      slices: [...acc.slices, { path: `M${cx},${cy} L${x1},${y1} A${r},${r} 0 ${largeArc},1 ${x2},${y2} Z`, color: CHART_COLORS[i % CHART_COLORS.length], name: d.category }],
    };
  }, { startAngle: -Math.PI / 2, slices: [] }).slices;

  return (
    <div className="pie-chart-content">
      <p className="report-chart-title">RAISED BY CATEGORY</p>
      <div className="pie-chart-center">
        <svg className="pie-chart-svg" viewBox="0 0 220 220">
          {slices.map((slice, i) => <path key={i} d={slice.path} fill={slice.color} />)}
        </svg>
      </div>
      <div className="pie-legend pie-legend-bottom">
        {data.map((item, i) => (
          <div className="pie-legend-item" key={item.category}>
            <span className="pie-legend-color" style={{ backgroundColor: CHART_COLORS[i % CHART_COLORS.length] }} />
            <span>{item.category}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function BarChart({ data }) {
  if (!data || data.length === 0) return <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "220px", color: "#999" }}>No data</div>;
  const gridPositions = [10, 30, 50, 70, 90, 100];
  const axisLabels = [10, 30, 50, 70, 90, "100+"];
  return (
    <>
      <p className="report-chart-title">MOST VIEWS ACTIVITIES</p>
      <div className="bar-chart">
        {data.map((d, i) => {
          const views = Number(d.views || 0);
          const pct = Math.min((views / 100) * 100, 100);
          const label = d.title.length > 16 ? d.title.slice(0, 14) + "..." : d.title;
          return (
            <div key={i} className="bar-row">
              <span className="bar-label">{label}</span>
              <div className="bar-track">
                {gridPositions.map((pos, gi) => <div key={gi} className="bar-gridline" style={{ left: `${pos}%` }} />)}
                <div className="bar-fill" style={{ width: `${pct}%` }} />
              </div>
            </div>
          );
        })}
        <div className="bar-axis">{axisLabels.map((label, i) => <span key={i}>{label}</span>)}</div>
      </div>
    </>
  );
}

function dailyReportPage() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");

  async function onClick() {
    try {
      setError("");
      const date = new Date().toISOString().slice(0, 10);
      const data = await generateDailyReport(date);
      setReport(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    onClick();
  }, []);

  if (error) return <p className="error-message">{error}</p>;
  if (!report) return null;

  return (
    <>
      <div className="report-stats-row">
        <div className="report-stat-card"><span className="stat-label">RAISED</span><strong className="stat-value">${report.summary.total_raised.toLocaleString()}</strong><span className="stat-sub">across the platform</span></div>
        <div className="report-stat-card"><span className="stat-label">ACTIVE ACTIVITIES</span><strong className="stat-value">{report.summary.active_activities}</strong><span className="stat-sub">across the platform</span></div>
        <div className="report-stat-card"><span className="stat-label">COMPLETED ACTIVITIES</span><strong className="stat-value">{report.summary.completed_activities}</strong><span className="stat-sub">across the platform</span></div>
        <div className="report-stat-card"><span className="stat-label">VIEWS</span><strong className="stat-value">{report.summary.views.toLocaleString()}</strong><span className="stat-sub">across the platform</span></div>
        <div className="report-stat-card"><span className="stat-label">ACTIVE USERS</span><strong className="stat-value">{report.summary.active_users.toLocaleString()}</strong><span className="stat-sub">across the platform</span></div>
      </div>
      <div className="report-charts-grid">
        <div className="report-chart-card"><PieChart data={report.raised_by_category || []} /></div>
        <div className="report-chart-card"><BarChart data={report.most_viewed_activities || []} /></div>
      </div>
    </>
  );
}

export default dailyReportPage;
