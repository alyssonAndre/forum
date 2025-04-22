const togglePassword = document.getElementById("togglePassword");
const passwordField = document.getElementById("id_password");
const eyeIcon = document.getElementById("eyeIcon");

togglePassword.addEventListener("click", () => {
    const isPassword = passwordField.type === "password";
    passwordField.type = isPassword ? "text" : "password";
    eyeIcon.textContent = isPassword ? "visibility_off" : "visibility";
});