import { invalidateSession } from "../../api/userAccountApi";

async function onClick(onLogout) {
  const token = localStorage.getItem("token");
  try {
    if (token) await invalidateSession(token);
  } finally {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("userId");
    onLogout();
  }
}

const logoutPage = { onClick };

export default logoutPage;
