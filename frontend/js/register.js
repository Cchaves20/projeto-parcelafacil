redirectIfAuthenticated();

const registerForm = document.getElementById("register-form");
const registerError = document.getElementById("register-error");

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError(registerError);

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  try {
    await api.register({ name, email, password });
    const { access_token } = await api.login({ email, password });
    setToken(access_token);
    window.location.href = "/pages/dashboard.html";
  } catch (error) {
    showError(registerError, error.message);
  }
});
