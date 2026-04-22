const API_BASE_URL = "http://127.0.0.1:8000";

let users = [];
let accounts = [];
let searchKeyword = '';
let accountSearchKeyword = '';
let currentUserId = null;
let currentAccountId = null;
let authToken = localStorage.getItem("token") || "";
let loggedInRole = localStorage.getItem("role") || "";

function getAuthHeaders(includeJson = false) {
    const headers = {};
    if (includeJson) headers["Content-Type"] = "application/json";
    if (authToken) headers["Authorization"] = `Bearer ${authToken}`;
    return headers;
}

function getErrorMessage(data, fallback = 'Something went wrong') {
    if (!data) return fallback;

    if (typeof data.detail === 'string') {
        return data.detail;
    }

    if (Array.isArray(data.detail)) {
        return data.detail
            .map(err => {
                if (typeof err === 'string') return err;
                const field = Array.isArray(err.loc) ? err.loc.slice(1).join(' > ') : 'field';
                return `${field}: ${err.msg}`;
            })
            .join('\n');
    }

    if (typeof data.message === 'string') {
        return data.message;
    }

    return fallback;
}

function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    const d = new Date(dateStr);
    if (Number.isNaN(d.getTime())) return dateStr;
    return d.toLocaleDateString('en-GB');
}

function openModal(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = 'flex';
}

function closeModal(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
}

function setupTabs() {
    const tabs = document.querySelectorAll('.tab-link');
    const profileDiv = document.getElementById('profileTab');
    const accountDiv = document.getElementById('accountTab');

    tabs.forEach(tab => {
        tab.addEventListener('click', async () => {
            const target = tab.getAttribute('data-tab');
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            if (target === 'profile') {
                profileDiv.classList.add('active-tab');
                accountDiv.classList.remove('active-tab');
                renderTable();
                updateStats();
            } else {
                accountDiv.classList.add('active-tab');
                profileDiv.classList.remove('active-tab');
                renderAccountTable();
                updateAccountStats();
                if (accountSearchKeyword) {
                    await loadAccounts(accountSearchKeyword);
                }
            }
        });
    });
}

// USER PROFILE
function getActiveCount() { return users.filter(u => u.status === 'active').length; }
function getSuspendedCount() { return users.filter(u => u.status === 'suspended').length; }
function getFilteredUsers() {
    if (!searchKeyword) return users;
    return users.filter(u => u.name.toLowerCase().includes(searchKeyword.toLowerCase()));
}

function renderTable() {
    const tbody = document.getElementById('profileTableBody');
    if (!tbody) return;

    const filtered = getFilteredUsers();
    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center">No user profiles found</td></tr>';
        return;
    }

    tbody.innerHTML = filtered.map(u => `
        <tr>
            <td>${escapeHtml(u.name)}</td>
            <td>${escapeHtml(u.description)}</td>
            <td class="${u.status === 'active' ? 'status-active' : 'status-suspended'}">${u.status === 'active' ? '● Active' : '● Suspended'}</td>
            <td>
                <a class="action-link" onclick="viewUser(${u.id})">View</a>
                <a class="action-link" onclick="editUser(${u.id})">Edit</a>
                ${u.status === 'active'
                    ? `<a class="action-link" onclick="suspendUser(${u.id})">Suspend</a>`
                    : ''}
            </td>
        </tr>
    `).join('');
}

function updateStats() {
    const totalEl = document.getElementById('profileTotalUsers');
    const activeEl = document.getElementById('profileActiveUsers');
    const suspendedEl = document.getElementById('profileSuspendedUsers');

    if (totalEl) totalEl.innerText = users.length;
    if (activeEl) activeEl.innerText = getActiveCount();
    if (suspendedEl) suspendedEl.innerText = getSuspendedCount();
}

async function loadUsers(keyword = "") {
    try {
        const url = keyword
            ? `${API_BASE_URL}/api/user_profile/?keyword=${encodeURIComponent(keyword)}`
            : `${API_BASE_URL}/api/user_profile/`;

        const response = await fetch(url, { method: "GET", headers: getAuthHeaders() });
        const data = await response.json();

        if (!response.ok) {
            alert(getErrorMessage(data, "Failed to load user profiles"));
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

async function onSearchProfile() {
    const input = document.getElementById('profileSearchInput');
    if (!input) return;
    searchKeyword = input.value.trim();
    await loadUsers(searchKeyword);
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
            body: JSON.stringify({ name_of_role: name, description: desc })
        });

        const data = await response.json();
        if (!response.ok) {
            alert(getErrorMessage(data, "Failed to create user profile"));
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
            alert(getErrorMessage(user, "Failed to load user profile"));
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
            body: JSON.stringify({ name_of_role: name, description })
        });

        const data = await response.json();
        if (!response.ok) {
            alert(getErrorMessage(data, "Failed to update user profile"));
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
            alert(getErrorMessage(data, "Failed to suspend user profile"));
            return;
        }

        closeModal('suspendModal');
        await loadUsers(searchKeyword);
    } catch (error) {
        console.error(error);
        alert("Unable to suspend user profile");
    }
}



// USER ACCOUNT
function normalizeAccount(account) {
    return {
        id: account.id,
        name: account.name || '',
        email: account.email || '',
        phone: account.phone_no || account.phone || '',
        dob: account.dob || '',
        address: account.address || '',
        userProfile: account.user_profile || account.name_of_role || '',
        status: (account.status || '').toLowerCase(),
    };
}

function getActiveCountAccount() { return accounts.filter(u => u.status === 'active').length; }
function getSuspendedCountAccount() { return accounts.filter(u => u.status === 'suspended').length; }
function getFilteredUsersAccount() {
    if (!accountSearchKeyword) return accounts;
    const keyword = accountSearchKeyword.toLowerCase();
    return accounts.filter(u =>
        (u.name || '').toLowerCase().includes(keyword) ||
        (u.email || '').toLowerCase().includes(keyword) ||
        (u.phone || '').toLowerCase().includes(keyword)
    );
}

function renderAccountTable() {
    const tbody = document.getElementById('accountTableBody');
    if (!tbody) return;
    const filtered = getFilteredUsersAccount();

    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center">No user accounts found</td></tr>';
        return;
    }

    tbody.innerHTML = filtered.map(u => `
        <tr>
            <td>${escapeHtml(u.name)}</td>
            <td>${escapeHtml(u.email)}</td>
            <td>${escapeHtml(u.phone)}</td>
            <td class="${u.status === 'active' ? 'status-active' : 'status-suspended'}">${u.status === 'active' ? '● Active' : '● Suspended'}</td>
            <td>
                <a class="action-link" onclick="viewAccountUser(${u.id})">View</a>
                <a class="action-link" onclick="editAccountUser(${u.id})">Edit</a>
                ${u.status === 'active'
                    ? `<a class="action-link" onclick="suspendAccountUser(${u.id})">Suspend</a>`
                    : ''}
            </td>
        </tr>
    `).join('');
}

function updateAccountStats() {
    const totalEl = document.getElementById('accountTotalUsers');
    const activeEl = document.getElementById('accountActiveUsers');
    const suspendedEl = document.getElementById('accountSuspendedUsers');

    if (totalEl) totalEl.innerText = accounts.length;
    if (activeEl) activeEl.innerText = getActiveCountAccount();
    if (suspendedEl) suspendedEl.innerText = getSuspendedCountAccount();
}

async function loadAccounts(keyword = "") {
    try {
        const url = keyword
            ? `${API_BASE_URL}/api/user_account/?keyword=${encodeURIComponent(keyword)}`
            : `${API_BASE_URL}/api/user_account/`;

        const response = await fetch(url, {
            method: 'GET',
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (!response.ok) {
            alert(getErrorMessage(data, 'Failed to load user accounts'));
            accounts = [];
            renderAccountTable();
            updateAccountStats();
            return;
        }

        accounts = (data.data || []).map(normalizeAccount);
        renderAccountTable();
        updateAccountStats();
    } catch (error) {
        console.error(error);
        alert('Unable to load user accounts');
    }
}

async function onSearchAccount() {
    const input = document.getElementById('accountSearchInput');
    if (!input) return;
    accountSearchKeyword = input.value.trim();
    await loadAccounts(accountSearchKeyword);
}

async function populateUserProfileOptions(selectId, selectedValue = '') {
    const select = document.getElementById(selectId);
    if (!select) return;

    if (users.length === 0) {
        await loadUsers();
    }

    select.innerHTML = users.map(profile => `
        <option value="${escapeHtml(profile.name)}" ${profile.name === selectedValue ? 'selected' : ''}>${escapeHtml(profile.name)}</option>
    `).join('');
}


async function showCreateAccountModal() {
    await populateUserProfileOptions('createUserProfile');
    document.getElementById('createAccountName').value = '';
    document.getElementById('createBirthdate').value = '';
    document.getElementById('createEmail').value = '';
    document.getElementById('createPassword').value = '';
    document.getElementById('createConfirmPassword').value = '';
    document.getElementById('createPhone').value = '';
    document.getElementById('createAddress').value = '';
    openModal('createAccountModal');
}

async function createAccountUser() {

    const password = document.getElementById('createPassword').value;
    const confirmPassword = document.getElementById('createConfirmPassword').value;

    const payload = {
        name: document.getElementById('createAccountName').value.trim(),
        dob: document.getElementById('createBirthdate').value,
        email: document.getElementById('createEmail').value.trim(),
        password,
        phone_no: document.getElementById('createPhone').value.trim(),
        address: document.getElementById('createAddress').value.trim(),
        user_profile: document.getElementById('createUserProfile').value,
        status: 'ACTIVE'
    };

    if (!payload.name || !payload.email || !password || !confirmPassword || !payload.user_profile) {
        alert('Name, email, password, and user profile are required');
        return;
    }
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/user_account/`, {
            method: 'POST',
            headers: getAuthHeaders(true),
            body: JSON.stringify(payload)
        });
        const data = await response.json();

        if (!response.ok) {
            alert(getErrorMessage(data, 'Failed to create user account'));
            return;
        }

        const createdAccount = normalizeAccount(data);
        const searchValue = createdAccount.email || createdAccount.name || payload.email || payload.name;
        accountSearchKeyword = searchValue;
        const searchInput = document.getElementById('accountSearchInput');
        if (searchInput) searchInput.value = searchValue;
        closeModal('createAccountModal');
        await loadAccounts(accountSearchKeyword);
    } catch (error) {
        console.error(error);
        alert('Unable to create user account');
    }
}

async function viewAccountUser(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/user_account/${id}`, { method: 'GET', headers: getAuthHeaders() });
        const data = await response.json();
        if (!response.ok) {
            alert(getErrorMessage(data, 'Failed to load user account'));
            return;
        }
        const user = normalizeAccount(data);
        document.getElementById('viewAccountStatus').innerText = user.status || '';
        document.getElementById('viewAccountName').innerText = user.name;
        document.getElementById('viewAccountEmail').innerText = user.email;
        document.getElementById('viewAccountDob').innerText = formatDate(user.dob) || 'Not specified';
        document.getElementById('viewAccountPhone').innerText = user.phone || 'Not specified';
        document.getElementById('viewAccountUserProfile').innerText = user.userProfile || 'Not specified';
        document.getElementById('viewAccountAddress').innerText = user.address || 'Not specified';
        openModal('viewAccountModal');
    } catch (error) {
        console.error(error);
        alert('Unable to load user account');
    }
}

async function editAccountUser(id) {
    const user = accounts.find(u => u.id === id);
    if (!user) return;
    currentAccountId = id;
    await populateUserProfileOptions('editUserProfile', user.userProfile);
    document.getElementById('editAccountName').value = user.name;
    document.getElementById('editAccountEmail').value = user.email || '';
    document.getElementById('editBirthdate').value = user.dob || '';
    document.getElementById('editPassword').value = '';
    document.getElementById('editConfirmPassword').value = '';
    document.getElementById('editPhone').value = user.phone || '';
    document.getElementById('editAddress').value = user.address || '';
    openModal('editAccountModal');
}

async function updateAccountUser() {
    const account = accounts.find(u => u.id === currentAccountId);
    const name = document.getElementById('editAccountName').value.trim();
    const email = document.getElementById('editAccountEmail').value.trim();
    const dob = document.getElementById('editBirthdate').value;
    const password = document.getElementById('editPassword').value;
    const confirmPassword = document.getElementById('editConfirmPassword').value;
    const phone_no = document.getElementById('editPhone').value.trim();
    const address = document.getElementById('editAddress').value.trim();
    const user_profile = document.getElementById('editUserProfile').value;

    if (!account) {
        alert('User account not found in table');
        return;
    }
    if (!name) {
        alert('Name is required');
        return;
    }
    if (!email) {
        alert('Email is required');
        return;
    }
    if (password && password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    const payload = {
        name,
        email,
        user_profile,
        status: account.status ? account.status.toUpperCase() : 'ACTIVE',
        phone_no: phone_no || null,
        address: address || null,
        dob: dob || null,
        password: password || null
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/user_account/${currentAccountId}`, {
            method: 'PATCH',
            headers: getAuthHeaders(true),
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            alert(getErrorMessage(data, 'Failed to update user account'));
            return;
        }

        const updatedAccount = normalizeAccount(data);
        const searchValue = accountSearchKeyword || updatedAccount.email || updatedAccount.name;
        if (searchValue) {
            accountSearchKeyword = searchValue;
            const searchInput = document.getElementById('accountSearchInput');
            if (searchInput) searchInput.value = searchValue;
            await loadAccounts(accountSearchKeyword);
        }

        closeModal('editAccountModal');
    } catch (error) {
        console.error(error);
        alert('Unable to update user account');
    }
}

function suspendAccountUser(id) {
    const user = accounts.find(u => u.id === id);
    if (!user) return;
    currentAccountId = id;
    document.getElementById('suspendAccountName').innerText = user.name;
    openModal('suspendAccountModal');
}

async function confirmSuspendAccount() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/user_account/${currentAccountId}/suspend`, {
            method: 'PATCH',
            headers: getAuthHeaders()
        });
        const data = await response.json();

        if (!response.ok) {
            alert(getErrorMessage(data, 'Failed to suspend user account'));
            return;
        }

        const account = accounts.find(u => u.id === currentAccountId);
        if (account) account.status = 'suspended';
        closeModal('suspendAccountModal');
        renderAccountTable();
        updateAccountStats();
    } catch (error) {
        console.error(error);
        alert('Unable to suspend user account');
    }
}

// AUTH / PAGE RENDERING
async function confirmLogout() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/logout`, { method: 'POST', headers: getAuthHeaders() });
        if (response.ok) await response.json();
    } catch (error) {
        console.error(error);
    }

    authToken = "";
    loggedInRole = "";
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    closeModal('logoutModal');
    showLoginPage();
}

function showLogoutModal() { openModal('logoutModal'); }

function showLoginPage() {
    document.body.className = 'login-body';
    document.body.innerHTML = `
        <div class="login-box">
            <div class="login-title">Online Fundraising Platform</div>
            <div class="input-group"><label>Email</label><input type="email" id="loginEmail"></div>
            <div class="input-group"><label>Password</label><input type="password" id="loginPassword"></div>
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
            method: 'POST',
            headers: getAuthHeaders(true),
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();

        if (!response.ok) {
            alert(getErrorMessage(data, 'Login failed'));
            return;
        }

        authToken = data.token;
        loggedInRole = data.role;
        localStorage.setItem('token', authToken);
        localStorage.setItem('role', loggedInRole);

        if (loggedInRole === 'USER_ADMIN') {
            await showDashboard();
        } else {
            alert(`Logged in as ${loggedInRole}. This frontend currently supports the User Admin dashboard only.`);
        }
    } catch (error) {
        console.error(error);
        alert('Unable to connect to backend');
    }
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
                <div class="view-row"><label>Name</label><span id="viewName"></span></div>
                <div class="view-row"><label>STATUS</label><span id="viewStatus"></span></div>
                <div class="view-row"><label>DESCRIPTION</label><span id="viewDescription"></span></div>
                <div class="modal-actions"><button class="btn-save" onclick="closeModal('viewModal')">Close</button></div>
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

        <div id="createAccountModal" class="modal">
            <div class="modal-content">
                <h2>Create User Account</h2>
                <label>User Profile</label>
                <select id="createUserProfile"></select>
                <label>Name</label>
                <input type="text" id="createAccountName">
                <label>Birthdate</label>
                <input type="date" id="createBirthdate">
                <label>Email</label>
                <input type="email" id="createEmail">
                <label>Password</label>
                <input type="password" id="createPassword">
                <label>Confirm Password</label>
                <input type="password" id="createConfirmPassword">
                <label>Phone Number</label>
                <input type="text" id="createPhone">
                <label>Address</label>
                <textarea id="createAddress" rows="2"></textarea>
                <div class="modal-actions">
                    <button class="btn-cancel" onclick="closeModal('createAccountModal')">Cancel</button>
                    <button class="btn-save" onclick="createAccountUser()">Create Account</button>
                </div>
            </div>
        </div>

        <div id="viewAccountModal" class="modal">
            <div class="modal-content">
                <div class="view-row"><label>STATUS</label><span id="viewAccountStatus"></span></div>
                <div class="view-row"><label>Name</label><span id="viewAccountName"></span></div>
                <div class="view-row"><label>Email</label><span id="viewAccountEmail"></span></div>
                <div class="view-row"><label>Date of Birth</label><span id="viewAccountDob"></span></div>
                <div class="view-row"><label>Phone Number</label><span id="viewAccountPhone"></span></div>
                <div class="view-row"><label>User Profile</label><span id="viewAccountUserProfile"></span></div>
                <div class="view-row"><label>Address</label><span id="viewAccountAddress"></span></div>
                <div class="modal-actions"><button class="btn-save" onclick="closeModal('viewAccountModal')">Close</button></div>
            </div>
        </div>

        <div id="editAccountModal" class="modal">
            <div class="modal-content">
                <h2>Update User Account</h2>
                <label>User Profile</label>
                <select id="editUserProfile"></select>
                <label>Name</label>
                <input type="text" id="editAccountName">
                <label>Email</label>
                <input type="email" id="editAccountEmail">
                <label>Birthdate</label>
                <input type="date" id="editBirthdate">
                <label>Password</label>
                <input type="password" id="editPassword" placeholder="Leave blank to keep current">
                <label>Confirm Password</label>
                <input type="password" id="editConfirmPassword">
                <label>Phone Number</label>
                <input type="text" id="editPhone">
                <label>Address</label>
                <textarea id="editAddress" rows="2"></textarea>
                <div class="modal-actions">
                    <button class="btn-cancel" onclick="closeModal('editAccountModal')">Cancel</button>
                    <button class="btn-save" onclick="updateAccountUser()">Save Changes</button>
                </div>
            </div>
        </div>

        <div id="suspendAccountModal" class="modal">
            <div class="modal-content">
                <h2>Suspend User</h2>
                <p><span id="suspendAccountName"></span> will no longer be able to access the system</p>
                <div class="modal-actions">
                    <button class="btn-cancel" onclick="closeModal('suspendAccountModal')">Cancel</button>
                    <button class="btn-suspend" onclick="confirmSuspendAccount()">Suspend</button>
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

        <div class="tab-nav">
            <div class="tab-link active" data-tab="profile">User Profile</div>
            <div class="tab-link" data-tab="account">User Account</div>
        </div>

        <div id="profileTab" class="tab-content active-tab">
            <div class="unified-container">
                <button class="unified-btn" onclick="showCreateModal()">+ Create User Profile</button>
                <div class="unified-stats">
                    <div class="unified-stat-card"><div class="unified-stat-number" id="profileTotalUsers">0</div><div class="unified-stat-label">Total Users</div></div>
                    <div class="unified-stat-card"><div class="unified-stat-number" id="profileActiveUsers">0</div><div class="unified-stat-label">Active</div></div>
                    <div class="unified-stat-card"><div class="unified-stat-number" id="profileSuspendedUsers">0</div><div class="unified-stat-label">Suspended</div></div>
                </div>
                <div class="unified-search-wrapper"><input type="text" id="profileSearchInput" class="unified-search-input" placeholder="search..." oninput="onSearchProfile()"></div>
                <table class="unified-table">
                    <thead><tr><th>NAME</th><th>Description</th><th>STATUS</th><th>ACTIONS</th></tr></thead>
                    <tbody id="profileTableBody"></tbody>
                </table>
            </div>
        </div>

        <div id="accountTab" class="tab-content">
            <div class="unified-container">
                <button class="unified-btn" onclick="showCreateAccountModal()">+ Create User Account</button>
                <div class="unified-stats">
                    <div class="unified-stat-card"><div class="unified-stat-number" id="accountTotalUsers">0</div><div class="unified-stat-label">Total Users</div></div>
                    <div class="unified-stat-card"><div class="unified-stat-number" id="accountActiveUsers">0</div><div class="unified-stat-label">Active</div></div>
                    <div class="unified-stat-card"><div class="unified-stat-number" id="accountSuspendedUsers">0</div><div class="unified-stat-label">Suspended</div></div>
                </div>
                <div class="unified-search-wrapper"><input type="text" id="accountSearchInput" class="unified-search-input" placeholder="search by name, email, etc..." oninput="onSearchAccount()"></div>
                <p style="margin-bottom: 1rem; color: #666; font-size: 0.9rem;">This backend supports searching user accounts by keyword. Start typing to load results.</p>
                <table class="unified-table">
                    <thead><tr><th>NAME</th><th>EMAIL</th><th>Phone</th><th>STATUS</th><th>ACTIONS</th></tr></thead>
                    <tbody id="accountTableBody"></tbody>
                </table>
            </div>
        </div>
    `;

    setupTabs();
    await loadUsers();
    await loadAccounts();
}

if (authToken && loggedInRole === 'USER_ADMIN') {
    showDashboard();
} else {
    showLoginPage();
}
