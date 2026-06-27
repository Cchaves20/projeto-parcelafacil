function requireAuth() {
  if (!getToken()) {
    window.location.href = "/pages/login.html";
  }
}

function redirectIfAuthenticated() {
  if (getToken()) {
    window.location.href = "/pages/dashboard.html";
  }
}

function logout() {
  clearToken();
  window.location.href = "/pages/login.html";
}
