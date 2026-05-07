import { apiRequest } from "./apiClient";

export function getBrowseActivities(keyword = "") {
  const params = new URLSearchParams();

  if (keyword) {
    params.append("keyword", keyword);
  }

  const queryString = params.toString();

  return apiRequest(
    `/api/donee/fundraising_activity/${queryString ? `?${queryString}` : ""}`
  );
}

export function viewActivity(activityId) {
  return apiRequest(`/api/donee/fundraising_activity/${activityId}`);
}

export function getCompletedActivities(keyword = "") {
  const params = new URLSearchParams();

  if (keyword) {
    params.append("keyword", keyword);
  }

  const queryString = params.toString();

  return apiRequest(
    `/api/donee/fundraising_activity/completed${queryString ? `?${queryString}` : ""}`
  );
}

export function viewCompletedActivity(activityId) {
  return apiRequest(`/api/donee/fundraising_activity/completed/${activityId}`);
}

export function getFavoriteActivities(keyword = "") {
  const params = new URLSearchParams();

  if (keyword) {
    params.append("keyword", keyword);
  }

  const queryString = params.toString();

  return apiRequest(`/api/donee/shortlist/${queryString ? `?${queryString}` : ""}`);
}

export function saveActivity(activityId) {
  return apiRequest("/api/donee/shortlist/", {
    method: "POST",
    body: JSON.stringify({
      activity_id: Number(activityId),
    }),
  });
}