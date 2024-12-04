function confirmDeleteAccount(event) {
    event.preventDefault(); // Prevent the default action
    const userConfirmed = confirm("Are you sure you want to delete your account? This action cannot be undone.");
    if (userConfirmed) {
        // If the user confirms, proceed with the deletion
        window.location.href = event.target.href;
    }
}

function toggleEditMode() {
    const inputs = document.querySelectorAll('.form-control');
    const editButton = document.getElementById("edit-account-button");
    const saveButton = document.getElementById("save-account-button");
    const deleteButton = document.getElementById("delete-account-button");

    inputs.forEach(input => {
        // Toggle the readonly attribute for all input fields
        if (input.hasAttribute('readonly')) {
            input.removeAttribute('readonly');
        } else {
            input.setAttribute('readonly', true);
        }
    });

    // Show/Hide buttons
    if (editButton.style.display !== "none") {
        editButton.style.display = "none";
        deleteButton.style.display = "none";
        saveButton.style.display = "inline-block";
    } else {
        editButton.style.display = "inline-block";
        deleteButton.style.display = "inline-block";
        saveButton.style.display = "none";
    }
}

function saveProfile(event) {
    event.preventDefault();
    const form = document.getElementById("profile-form");
    form.submit();
}