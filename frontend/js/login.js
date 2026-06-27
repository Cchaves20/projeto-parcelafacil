redirectIfAuthenticated();

const loginForm = document.getElementById("login-form");
const loginError = document.getElementById("login-error");

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError(loginError);

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  try {
    const { access_token } = await api.login({ email, password });
    setToken(access_token);
    window.location.href = "/pages/dashboard.html";
  } catch (error) {
    showError(loginError, error.message);
  }
});
