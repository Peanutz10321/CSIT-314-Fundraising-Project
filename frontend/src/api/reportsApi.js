import { apiRequest } from "./apiClient";

export function getReports(period = "daily") {
  return apiRequest(`/api/reports/?period=${period}`);
}
