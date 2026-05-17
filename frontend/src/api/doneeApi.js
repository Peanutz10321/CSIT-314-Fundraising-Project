import { apiRequest } from "./apiClient";

export function doneeSearchFundraisingActivity(keyword = "") {
  const params = new URLSearchParams();
  if (keyword) params.append("keyword", keyword);
  const queryString = params.toString();
  return apiRequest(
    `/api/donee/fundraising_activity/${queryString ? `?${queryString}` : ""}`
  );
}

export function doneeViewFundraisingActivity(activityId) {
  return apiRequest(`/api/donee/fundraising_activity/${activityId}`);
}

export function saveFundraisingActivity(activityId) {
  return apiRequest("/api/donee/shortlist/", {
    method: "POST",
    body: JSON.stringify({ activity_id: Number(activityId) }),
  });
}

export function searchFavoriteList(keyword = "") {
  const params = new URLSearchParams();
  if (keyword) params.append("keyword", keyword);
  const queryString = params.toString();
  return apiRequest(`/api/donee/shortlist/${queryString ? `?${queryString}` : ""}`);
}

export function viewFavoriteList() {
  return apiRequest("/api/donee/shortlist/");
}

export function searchCompletedActivity(query = "") {
  const params = new URLSearchParams();
  if (query) params.append("keyword", query);
  const queryString = params.toString();
  return apiRequest(
    `/api/donee/fundraising_activity/completed${queryString ? `?${queryString}` : ""}`
  );
}

export function viewCompletedFundraisingActivities() {
  return apiRequest("/api/donee/fundraising_activity/completed");
}
