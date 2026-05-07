import { useState } from "react";
import LogoutConfirmModal from "../common/LogoutConfirmModal";

function DashboardLayout({ children, activePage, onLogout, setCurrentPage, role }) {
  const [showLogoutModal, setShowLogoutModal] = useState(false);

  return (
    <div className="dashboard-page">
      <aside className="sidebar">
        <div className="brand">Fundser</div>

        <div className="login-info">
          <p>Logged in as</p>
          <strong>
            {role === "FUNDRAISER"
              ? "Fundraiser"
              : role === "PLATFORM_MANAGER"
              ? "Platform Management"
              : role === "DONEE"
              ? "Donee"
              : "User Admin"}
          </strong>
        </div>

        <nav>
          {role === "USER_ADMIN" && (
            <>
              <button
                className={activePage === "profiles" ? "active" : ""}
                onClick={() => setCurrentPage("profiles")}
              >
                User Profiles
              </button>

              <button
                className={activePage === "accounts" ? "active" : ""}
                onClick={() => setCurrentPage("accounts")}
              >
                User Accounts
              </button>
            </>
          )}

          {role === "FUNDRAISER" && (
            <>
              <button
                className={activePage === "fundraisingActivities" ? "active" : ""}
                onClick={() => setCurrentPage("fundraisingActivities")}
              >
                Activities
              </button>

              <button
                className={activePage === "completedActivities" ? "active" : ""}
                onClick={() => setCurrentPage("completedActivities")}
              >
                Activities History
              </button>
            </>
          )}

          {role === "PLATFORM_MANAGER" && (
            <>
              <button
                className={activePage === "categories" ? "active" : ""}
                onClick={() => setCurrentPage("categories")}
              >
                Categories
              </button>

              <button
                className={activePage === "reports" ? "active" : ""}
                onClick={() => setCurrentPage("reports")}
              >
                Reports
              </button>
            </>
          )}

          {role === "DONEE" && (
            <>
              <button
                className={activePage === "doneeBrowse" ? "active" : ""}
                onClick={() => setCurrentPage("doneeBrowse")}
              >
                Browse Activities
              </button>

              <button
                className={activePage === "doneeFavorites" ? "active" : ""}
                onClick={() => setCurrentPage("doneeFavorites")}
              >
                My Favorites
              </button>

              <button
                className={activePage === "doneeCompleted" ? "active" : ""}
                onClick={() => setCurrentPage("doneeCompleted")}
              >
                Completed History
              </button>
            </>
          )}
        </nav>

        <button
          className="logout-btn"
          onClick={() => setShowLogoutModal(true)}
        >
          Log out
        </button>
      </aside>

      <main className="main-content">{children}</main>

      {showLogoutModal && (
        <LogoutConfirmModal
          onClose={() => setShowLogoutModal(false)}
          onConfirm={onLogout}
        />
      )}
    </div>
  );
}

export default DashboardLayout;