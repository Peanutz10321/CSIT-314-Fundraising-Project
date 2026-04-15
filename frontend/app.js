const API_BASE_URL = "http://127.0.0.1:8000";

let users = [];
let searchKeyword = '';
let currentUserId = null;
let authToken = localStorage.getItem("token") || "";
let loggedInRole = localStorage.getItem("role") || "";

function getAuthHeaders(includeJson = false) {
    const headers = {};

    if (includeJson) {
        headers["Content-Type"] = "application/json";
    }

    if (authToken) {
        headers["Authorization"] = `Bearer ${authToken}`;
    }

    return headers;
}

function getActiveCount() {
    return users.filter(u => u.status === 'active').length;
}

function getSuspendedCount() {
    return users.filter(u => u.status === 'suspended').length;
}

function getFilteredUsers() {
    if (!searchKeyword) return users;
    return users.filter(u => u.name.toLowerCase().includes(searchKeyword.toLowerCase()));
}

function renderTable() {
    const tbody = document.getElementById('userTableBody');
    if (!tbody) return;

    const filtered = getFilteredUsers();
    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center">No users found</td></tr>';
        return;
    }

    let html = '';
    for (const u of filtered) {
        html += '<tr>';
        html += `<td>${u.name}</td>`;
        html += `<td>${u.description}</td>`;
        html += `<td class="${u.status === 'active' ? 'status-active' : 'status-suspended'}">`;
        html += (u.status === 'active' ? '● Active' : '● Suspended');
        html += '</td>';
        html += '<td>';
        html += `<a class="action-link" onclick="viewUser(${u.id})">View</a>`;
        html += `<a class="action-link" onclick="editUser(${u.id})">Edit</a>`;
        if (u.status === 'active') {
            html += `<a class="action-link" onclick="suspendUser(${u.id})">Suspend</a>`;
        }
        html += '</td>';
        html += '</tr>';
    }

    tbody.innerHTML = html;
}

function updateStats() {
    const totalEl = document.getElementById('totalUsers');
    const activeEl = document.getElementById('activeUsers');
    const suspendedEl = document.getElementById('suspendedUsers');

    if (totalEl) totalEl.innerText = users.length;
    if (activeEl) activeEl.innerText = getActiveCount();
    if (suspendedEl) suspendedEl.innerText = getSuspendedCount();
}

async function loadUsers(keyword = "") {
    try {
        const url = keyword
            ? `${API_BASE_URL}/api/user_profile/?keyword=${encodeURIComponent(keyword)}`
            : `${API_BASE_URL}/api/user_profile/`;

        const response = await fetch(url, {
            method: "GET",
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Failed to load user profiles");
            return;
        }

        users = (data.data || []).map(profile => ({
            id: profile.id,
            name: profile.name_of_role,
            description: profile.description || "",
            status: (profile.status || "").toLowerCase()
        }));

        renderTable();
        updateStats();
    } catch (error) {
        console.error(error);
        alert("Unable to load user profiles");
    }
}

async function onSearch() {
    const input = document.getElementById('searchInput');
    if (!input) return;

    searchKeyword = input.value.trim();
    await loadUsers(searchKeyword);
}

function openModal(id) {
    document.getElementById(id).style.display = 'flex';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

function showCreateModal() {
    document.getElementById('createName').value = '';
    document.getElementById('createDescription').value = '';
    openModal('createModal');
}

async function createUser() {
    const name = document.getElementById('createName').value.trim();
    const desc = document.getElementById('createDescription').value.trim();

    if (!name) {
        alert('Name is required');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/user_profile/`, {
            method: "POST",
            headers: getAuthHeaders(true),
            body: JSON.stringify({
                name_of_role: name,
                description: desc
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Failed to create user profile");
            return;
        }

        closeModal('createModal');
        await loadUsers(searchKeyword);
    } catch (error) {
        console.error(error);
        alert("Unable to create user profile");
    }
}

async function viewUser(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/user_profile/${id}`, {
            method: "GET",
            headers: getAuthHeaders()
        });

        const user = await response.json();

        if (!response.ok) {
            alert(user.detail || "Failed to load user profile");
            return;
        }

        document.getElementById('viewName').innerText = user.name_of_role;
        document.getElementById('viewStatus').innerText = user.status;
        document.getElementById('viewDescription').innerText = user.description || '';

        openModal('viewModal');
    } catch (error) {
        console.error(error);
        alert("Unable to load user profile");
    }
}

function editUser(id) {
    const user = users.find(u => u.id === id);
    if (!user) return;

    currentUserId = id;
    document.getElementById('editName').value = user.name;
    document.getElementById('editDescription').value = user.description;
    openModal('editModal');
}

async function updateUser() {
    const name = document.getElementById('editName').value.trim();
    const description = document.getElementById('editDescription').value.trim();

    if (!name) {
        alert('Name is required');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/user_profile/${currentUserId}`, {
            method: "PATCH",
            headers: getAuthHeaders(true),
            body: JSON.stringify({
                name_of_role: name,
                description
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Failed to update user profile");
            return;
        }

        closeModal('editModal');
        await loadUsers(searchKeyword);
    } catch (error) {
        console.error(error);
        alert("Unable to update user profile");
    }
}

function suspendUser(id) {
    const user = users.find(u => u.id === id);
    if (!user) return;

    currentUserId = id;
    document.getElementById('suspendUserName').innerText = user.name;
    openModal('suspendModal');
}

async function confirmSuspend() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/user_profile/${currentUserId}/suspend`, {
            method: "PATCH",
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Failed to suspend user profile");
            return;
        }

        closeModal('suspendModal');
        await loadUsers(searchKeyword);
    } catch (error) {
        console.error(error);
        alert("Unable to suspend user profile");
    }
}

function reactivateUser(id) {
    const user = users.find(u => u.id === id);
    if (!user) return;

    document.getElementById('reactivateUserName').innerText = user.name;
    currentUserId = id;
    openModal('reactivateModal');
}

function confirmReactivate() {
    const user = users.find(u => u.id === currentUserId);
    if (!user) return;

    user.status = 'active';
    renderTable();
    updateStats();
    closeModal('reactivateModal');
}

async function confirmLogout() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/logout`, {
            method: "POST",
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Logout failed");
            return;
        }
    } catch (error) {
        console.error(error);
    }

    authToken = "";
    loggedInRole = "";
    localStorage.removeItem("token");
    localStorage.removeItem("role");

    closeModal('logoutModal');
    showLoginPage();
}

function showLoginPage() {
    document.body.className = 'login-body';
    document.body.innerHTML = `
        <div class="login-box">
            <div class="login-title">Online Fundraising Platform</div>
            <div class="input-group">
                <label>Email</label>
                <input type="email" id="loginEmail">
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" id="loginPassword">
            </div>
            <button class="login-btn" onclick="doLogin()">Login</button>
        </div>
    `;
}

async function doLogin() {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;

    if (!email || !password) {
        alert('Email and password are required');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: "POST",
            headers: getAuthHeaders(true),
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Login failed");
            return;
        }

        authToken = data.token;
        loggedInRole = data.role;

        localStorage.setItem("token", authToken);
        localStorage.setItem("role", loggedInRole);

        if (loggedInRole === "USER_ADMIN") {
            await showDashboard();
        } else {
            alert(`Logged in as ${loggedInRole}. This frontend currently supports the User Admin dashboard only.`);
        }
    } catch (error) {
        console.error(error);
        alert("Unable to connect to backend");
    }
}

function showLogoutModal() {
    openModal('logoutModal');
}

async function showDashboard() {
    document.body.className = 'dashboard-body';
    document.body.innerHTML = `
        <div id="logoutModal" class="modal">
            <div class="modal-content">
                <h3>Log Out</h3>
                <p>Are you sure want to exit the system?</p>
                <div class="modal-actions">
                    <button class="btn-cancel" onclick="closeModal('logoutModal')">Cancel</button>
                    <button class="btn-save" onclick="confirmLogout()">Log Out</button>
                </div>
            </div>
        </div>

        <div id="createModal" class="modal">
            <div class="modal-content">
                <h3>Create User Profile</h3>
                <input type="text" id="createName" placeholder="Name">
                <textarea id="createDescription" placeholder="Description"></textarea>
                <div class="modal-actions">
                    <button class="btn-cancel" onclick="closeModal('createModal')">Cancel</button>
                    <button class="btn-save" onclick="createUser()">Save Changes</button>
                </div>
            </div>
        </div>

        <div id="viewModal" class="modal">
            <div class="modal-content">
                <h3>User Profile</h3>
                <div class="view-row">
                    <label>Name</label>
                    <span id="viewName"></span>
                </div>
                <div class="view-row">
                    <label>STATUS</label>
                    <span id="viewStatus"></span>
                </div>
                <div class="view-row">
                    <label>DESCRIPTION</label>
                    <span id="viewDescription"></span>
                </div>
                <div class="modal-actions">
                    <button class="btn-save" onclick="closeModal('viewModal')">Close</button>
                </div>
            </div>
        </div>

        <div id="editModal" class="modal">
            <div class="modal-content">
                <h3>Update User Profile</h3>
                <input type="text" id="editName" placeholder="Name">
                <textarea id="editDescription" placeholder="Description"></textarea>
                <div class="modal-actions">
                    <button class="btn-cancel" onclick="closeModal('editModal')">Cancel</button>
                    <button class="btn-save" onclick="updateUser()">Save Changes</button>
                </div>
            </div>
        </div>

        <div id="suspendModal" class="modal">
            <div class="modal-content">
                <h3>Suspend User</h3>
                <p><span id="suspendUserName"></span> will no longer be able to access the system</p>
                <div class="modal-actions">
                    <button class="btn-cancel" onclick="closeModal('suspendModal')">Cancel</button>
                    <button class="btn-suspend" onclick="confirmSuspend()">Suspend</button>
                </div>
            </div>
        </div>

        <div id="reactivateModal" class="modal">
            <div class="modal-content">
                <h3>Reactivate User</h3>
                <p><span id="reactivateUserName"></span> will regain access to the system</p>
                <div class="modal-actions">
                    <button class="btn-cancel" onclick="closeModal('reactivateModal')">Cancel</button>
                    <button class="btn-reactivate" onclick="confirmReactivate()">Reactivate</button>
                </div>
            </div>
        </div>

        <div class="dashboard-header">
            <h1>Fundraising Platform</h1>
            <div class="header-right">
                <span>Logged in as <strong>User Admin</strong></span>
                <a class="log-out-link" onclick="showLogoutModal()">Log out</a>
            </div>
        </div>

        <div class="dashboard-container">
            <button class="create-user-btn" onclick="showCreateModal()">+ Create User</button>

            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-number" id="totalUsers">0</div>
                    <div class="stat-label">Total Users</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="activeUsers">0</div>
                    <div class="stat-label">Active</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="suspendedUsers">0</div>
                    <div class="stat-label">Suspended</div>
                </div>
            </div>

            <div class="search-row">
                <input type="text" id="searchInput" placeholder="search..." oninput="onSearch()">
            </div>

            <table class="user-table">
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>Description</th>
                        <th>STATUS</th>
                        <th>ACTIONS</th>
                    </tr>
                </thead>
                <tbody id="userTableBody"></tbody>
            </table>
        </div>
    `;

    await loadUsers();
}

if (authToken && loggedInRole === "USER_ADMIN") {
    showDashboard();
} else {
    showLoginPage();
}
