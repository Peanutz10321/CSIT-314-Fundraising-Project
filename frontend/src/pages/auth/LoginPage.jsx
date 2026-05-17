import { useState } from "react";
import { validateCredentials } from "../../api/userAccountApi";

function getUserIdFromToken(token) {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.sub;
  } catch {
    return null;
  }
}

function loginPage({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  function displaySuccess(data) {
    localStorage.setItem("token", data.token);
    localStorage.setItem("role", data.role);
    const userId = data.user_id || getUserIdFromToken(data.token);
    if (userId) localStorage.setItem("userId", userId);
    onLogin(data.role);
  }

  function displayError(message) {
    setError(message);
  }

  async function onClick(e) {
    e.preventDefault();
    setError("");
    try {
      const data = await validateCredentials(email, password);
      displaySuccess(data);
    } catch (err) {
      displayError(err.message);
    }
  }

  return (
    <div className="login-page">
      <div className="login-box">
        <h1>Sign in</h1>

        <form onSubmit={onClick}>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {error && <p className="error-message">{error}</p>}

          <button type="submit" className="primary-btn">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default loginPage;
