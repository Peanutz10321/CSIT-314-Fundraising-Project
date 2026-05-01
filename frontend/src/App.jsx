import { useState } from "react";
import LoginPage from "./pages/auth/LoginPage";
import UserProfilePage from "./pages/userAdmin/UserProfilePage";
import UserAccountPage from "./pages/userAdmin/UserAccountPage";
import FundraisingActivityPage from "./pages/fundraiser/FundraisingActivityPage";
import CompletedFundraisingActivityPage from "./pages/fundraiser/CompletedFundraisingActivityPage";
import "./App.css";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    Boolean(localStorage.getItem("token"))
  );

  const [role, setRole] = useState(localStorage.getItem("role"));
  const [currentPage, setCurrentPage] = useState("profiles");

  const handleLogin = (loginRole) => {
    setRole(loginRole);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    setRole(null);
    setIsLoggedIn(false);
  };

  

  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />;
  }


  if (role === "USER_ADMIN") {
    if (currentPage === "accounts") {
      return (
        <UserAccountPage
          onLogout={handleLogout}
          setCurrentPage={setCurrentPage}
        />
      );
    }

    return (
      <UserProfilePage
        onLogout={handleLogout}
        setCurrentPage={setCurrentPage}
      />
    );
  }
  if (role === "FUNDRAISER") {
    if (currentPage === "completedActivities") {
      return (
        <CompletedFundraisingActivityPage
          onLogout={handleLogout}
          setCurrentPage={setCurrentPage}
        />
      );
    }

    return (
      <FundraisingActivityPage
        onLogout={handleLogout}
        setCurrentPage={setCurrentPage}
      />
    );
  }
  
  return (
    <div style={{ padding: "40px" }}>
      <h1>Dashboard not ready yet</h1>
      <p>Logged in as: {role || "Unknown role"}</p>
      <button onClick={handleLogout}>Log out</button>
    </div>
  );
}

export default App;