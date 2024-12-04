function HandleRegister(event) {
    togglePasswordVisibility(event);
    validatePassword();
    validateForm(event);
}

// SHOW PASSWORD BUTTON
function togglePasswordVisibility(event) {
    var passwordInput = document.getElementById("password");
    var button = event.target;
    var icon = button.querySelector('i');
    
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = "password";
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// VALIDATE PASSWORD
function validatePassword() {
    var password = document.getElementById("#password");
    var confirmPassword = document.getElementById("#confirm_password");
    var message = document.getElementById("password-message");

    if (password.value !== confirmPassword.value) {
        message.innerHTML = "Passwords do not match";
        message.style.color = "red";
        confirmPassword.setCustomValidity("Passwords do not match");
    } else {
        message.innerHTML = "";
        confirmPassword.setCustomValidity("");
    }
}
