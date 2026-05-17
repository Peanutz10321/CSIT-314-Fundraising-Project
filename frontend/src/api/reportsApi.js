import { apiRequest } from "./apiClient";

export function generateDailyReport(date) {
  return apiRequest(`/api/report/daily?date=${date}`);
}

export function generateWeeklyReport(startDate, endDate) {
  return apiRequest(`/api/report/weekly?startDate=${startDate}&endDate=${endDate}`);
}

export function generateMonthlyReport(month) {
  return apiRequest(`/api/report/monthly?month=${month}`);
}
