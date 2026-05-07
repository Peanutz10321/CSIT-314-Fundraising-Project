import { apiRequest } from "./apiClient";

export function getDailyReport(date) {
  return apiRequest(`/api/report/daily?date=${date}`);
}

export function getWeeklyReport(weekStart) {
  return apiRequest(`/api/report/weekly?week_start=${weekStart}`);
}

export function getMonthlyReport(month) {
  return apiRequest(`/api/report/monthly?month=${month}`);
}