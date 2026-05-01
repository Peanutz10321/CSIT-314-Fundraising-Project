import { apiRequest } from "./apiClient";

export function getUserProfiles(keyword = "") {
  const params = new URLSearchParams();

  if (keyword) {
    params.append("keyword", keyword);
  }

  const queryString = params.toString();

  return apiRequest(`/api/user_profile/${queryString ? `?${queryString}` : ""}`);
}

export function createUserProfile(payload) {
  return apiRequest("/api/user_profile/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateUserProfile(profileId, payload) {
  return apiRequest(`/api/user_profile/${profileId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function suspendUserProfile(profileId) {
  return apiRequest(`/api/user_profile/${profileId}/suspend`, {
    method: "PATCH",
  });
}