import { apiRequest } from "./apiClient";

export function getActiveCategories() {
  return apiRequest("/api/category/");
}

export function getCategories(keyword = "") {
  const params = new URLSearchParams();
  if (keyword) params.append("keyword", keyword);
  const qs = params.toString();
  return apiRequest(`/api/category/${qs ? `?${qs}` : ""}`);
}

export function createCategory(payload) {
  return apiRequest("/api/category/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getCategory(id) {
  return apiRequest(`/api/category/${id}`);
}

export function updateCategory(id, payload) {
  return apiRequest(`/api/category/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function suspendCategory(id) {
  return apiRequest(`/api/category/${id}/suspend`, { method: "PATCH" });
}
