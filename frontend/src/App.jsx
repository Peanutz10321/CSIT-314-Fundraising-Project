import { useState } from "react";
import LoginPage from "./pages/auth/loginPage";
import logoutPage from "./pages/auth/logoutPage";
import UserProfilePage from "./pages/userAdmin/UserProfilePage";
import UserAccountPage from "./pages/userAdmin/UserAccountPage";
import FundraisingActivityPage from "./pages/fundraiser/FundraisingActivityPage";
import CompletedFundraisingActivityPage from "./pages/fundraiser/CompletedFundraisingActivityPage";
import CategoriesPage from "./pages/platformManagement/CategoriesPage";
import ReportsPage from "./pages/platformManagement/ReportsPage";
import DoneeBrowseActivitiesPage from "./pages/donee/DoneeBrowseActivitiesPage";
import DoneeFavoritesPage from "./pages/donee/DoneeFavoritesPage";
import DoneeCompletedActivitiesPage from "./pages/donee/DoneeCompletedActivitiesPage";
import "./App.css";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    Boolean(localStorage.getItem("token"))
  );

  const [role, setRole] = useState(localStorage.getItem("role"));
  const [currentPage, setCurrentPage] = useState(
    role === "PLATFORM_MANAGER" ? "categories" : role === "DONEE" ? "doneeBrowse" : "profiles"
  );

  const handleLogin = (loginRole) => {
    setRole(loginRole);

    if (loginRole === "PLATFORM_MANAGER") {
      setCurrentPage("categories");
    } else if (loginRole === "FUNDRAISER") {
      setCurrentPage("fundraisingActivities");
    } else if (loginRole === "DONEE") {
      setCurrentPage("doneeBrowse");
    } else {
      setCurrentPage("profiles");
    }

    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    logoutPage.onClick(() => {
      setRole(null);
      setIsLoggedIn(false);
    });
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
  

  if (role === "DONEE") {
    if (currentPage === "doneeFavorites") {
      return (
        <DoneeFavoritesPage
          onLogout={handleLogout}
          setCurrentPage={setCurrentPage}
        />
      );
    }

    if (currentPage === "doneeCompleted") {
      return (
        <DoneeCompletedActivitiesPage
          onLogout={handleLogout}
          setCurrentPage={setCurrentPage}
        />
      );
    }

    return (
      <DoneeBrowseActivitiesPage
        onLogout={handleLogout}
        setCurrentPage={setCurrentPage}
      />
    );
  }

  if (role === "PLATFORM_MANAGER") {
    if (currentPage === "reports") {
      return (
        <ReportsPage
          onLogout={handleLogout}
          setCurrentPage={setCurrentPage}
        />
      );
    }
    return (
      <CategoriesPage
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