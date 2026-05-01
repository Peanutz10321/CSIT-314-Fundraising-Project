import { apiRequest } from "./apiClient";

export function getFundraisingActivities(keyword = "") {
  const params = new URLSearchParams();

  if (keyword) {
    params.append("keyword", keyword);
  }

  const queryString = params.toString();

  return apiRequest(
    `/api/fundraising_activity/${queryString ? `?${queryString}` : ""}`
  );
}

export function getCompletedFundraisingActivities(keyword = "") {
  const params = new URLSearchParams();

  if (keyword) {
    params.append("keyword", keyword);
  }

  const queryString = params.toString();

  return apiRequest(
    `/api/fundraising_activity/completed${queryString ? `?${queryString}` : ""}`
  );
}

export function createFundraisingActivity(payload) {
  return apiRequest("/api/fundraising_activity/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateFundraisingActivity(activityId, payload) {
  return apiRequest(`/api/fundraising_activity/${activityId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function suspendFundraisingActivity(activityId) {
  return apiRequest(`/api/fundraising_activity/${activityId}/suspend`, {
    method: "PATCH",
  });
}