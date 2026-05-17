import { apiRequest } from "./apiClient";

export function searchUserAccount(keyword = "") {
  const params = new URLSearchParams();

  if (keyword) {
    params.append("keyword", keyword);
  }

  const queryString = params.toString();

  return apiRequest(`/api/user_account/${queryString ? `?${queryString}` : ""}`);
}

export function viewUserAccount(accountId) {
  return apiRequest(`/api/user_account/${accountId}`);
}

export function createUserAccount(payload) {
  return apiRequest("/api/user_account/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateUserAccount(accountId, payload) {
  return apiRequest(`/api/user_account/${accountId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function suspendUserAccount(accountId) {
  return apiRequest(`/api/user_account/${accountId}/suspend`, {
    method: "PATCH",
  });
}

export function validateCredentials(email, password) {
  return apiRequest("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function invalidateSession(token) {
  return apiRequest("/api/auth/logout", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}