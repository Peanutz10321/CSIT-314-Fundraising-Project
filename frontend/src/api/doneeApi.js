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

export function getFavoriteActivities(doneeId, keyword = "") {
  const params = new URLSearchParams();

  params.append("donee_id", doneeId);

  if (keyword) {
    params.append("keyword", keyword);
  }

  return apiRequest(`/api/donee/shortlist/?${params.toString()}`);
}

export function saveActivity(doneeId, activityId) {
  return apiRequest("/api/donee/shortlist/", {
    method: "POST",
    body: JSON.stringify({
      donee_id: Number(doneeId),
      activity_id: Number(activityId),
    }),
  });
}