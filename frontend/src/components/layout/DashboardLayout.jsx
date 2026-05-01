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
          <strong>{role === "FUNDRAISER" ? "Fundraiser" : "User Admin"}</strong>
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