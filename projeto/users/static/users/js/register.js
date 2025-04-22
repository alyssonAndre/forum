const passwordField1 = document.getElementById("id_password1");
const passwordField2 = document.getElementById("id_password2");
const submitBtn = document.getElementById("submitBtn");

function checkPasswordStrength() {
    const password = passwordField1.value;
    const confirmPassword = passwordField2.value;

    const emptyError = document.getElementById("emptyError");
    const lengthError = document.getElementById("lengthError");
    const sequenceError = document.getElementById("sequenceError");
    const matchError = document.getElementById("matchError");
    const specialCharError = document.getElementById("missingSpecialCareError");

    const emptyIcon = document.getElementById("emptyIcon");
    const lengthIcon = document.getElementById("lengthIcon");
    const sequenceIcon = document.getElementById("sequenceIcon");
    const matchIcon = document.getElementById("matchIcon");
    const specialCharIcon = document.getElementById("missingSpecialCareIcon");

    if (password === "") {
        setInvalid(emptyError, emptyIcon);
    } else {
        setValid(emptyError, emptyIcon);
    }

    if (password.length >= 8) {
        setValid(lengthError, lengthIcon);
    } else {
        setInvalid(lengthError, lengthIcon);
    }

    const sequenceRegex = /([a-z]{5}|[0-9]{5})/i;
    if (!sequenceRegex.test(password)) {
        setValid(sequenceError, sequenceIcon);
    } else {
        setInvalid(sequenceError, sequenceIcon);
    }

    if (password !== "" && password === confirmPassword) {
        setValid(matchError, matchIcon);
    } else {
        setInvalid(matchError, matchIcon);
    }

    const specialCharRegex = /[!@#$%^&*(),.?":{}|<>]/;
    if (specialCharRegex.test(password)) {
        setValid(specialCharError, specialCharIcon);
    } else {
        setInvalid(specialCharError, specialCharIcon);
    }

    toggleSubmit();
}

function setValid(el, icon) {
    el.style.color = "green";
    icon.textContent = "✔️";
}

function setInvalid(el, icon) {
    el.style.color = "red";
    icon.textContent = "❌";
}

function toggleSubmit() {
    const errors = document.querySelectorAll("#passwordErrors li");
    const allValid = Array.from(errors).every(
        (el) => el.style.color === "green"
    );

    if (allValid) {
        submitBtn.disabled = false;
        submitBtn.classList.remove("bg-gray-400", "cursor-not-allowed");
        submitBtn.classList.add(
            "bg-blue-600",
            "hover:bg-blue-700",
            "cursor-pointer"
        );
    } else {
        submitBtn.disabled = true;
        submitBtn.classList.remove(
            "bg-blue-600",
            "hover:bg-blue-700",
            "cursor-pointer"
        );
        submitBtn.classList.add("bg-gray-400", "cursor-not-allowed");
    }
}

passwordField1.addEventListener("input", checkPasswordStrength);
passwordField2.addEventListener("input", checkPasswordStrength);

const togglePassword1 = document.getElementById("togglePassword1");
const eyeIcon1 = document.getElementById("eyeIcon1");
togglePassword1.addEventListener("click", () => {
    const isPassword = passwordField1.type === "password";
    passwordField1.type = isPassword ? "text" : "password";
    eyeIcon1.textContent = isPassword ? "visibility_off" : "visibility";
});

const togglePassword2 = document.getElementById("togglePassword2");
const eyeIcon2 = document.getElementById("eyeIcon2");
togglePassword2.addEventListener("click", () => {
    const isPassword = passwordField2.type === "password";
    passwordField2.type = isPassword ? "text" : "password";
    eyeIcon2.textContent = isPassword ? "visibility_off" : "visibility";
});