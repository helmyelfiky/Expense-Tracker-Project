// TO DISPLAY TO CATEGORY BASED ON TRANSACTION TYPE IN ADD TRANSACTION FORM
document.addEventListener('DOMContentLoaded', function() {
    const transactionTypeRadios = document.querySelectorAll('input[name="Transaction_type"]');
    const categorySelect = document.getElementById('id_Category');

    function filterCategories() {
        const selectedType = document.querySelector('input[name="Transaction_type"]:checked').value;
        const options = categorySelect.querySelectorAll('option');

        options.forEach(option => {
            if (option.getAttribute('data-type') === selectedType) {
                option.style.display = 'block';
            } else {
                option.style.display = 'none';
            }
        });

        // Reset the selected option to the first visible option
        categorySelect.value = categorySelect.querySelector('option[data-type="' + selectedType + '"]').value;
    }

    transactionTypeRadios.forEach(radio => {
        radio.addEventListener('change', filterCategories);
    });

    // Initial filter on page load
    filterCategories();
});

// TO CONFIRM DELETION OF TRANSACTION BEFORE DELETING
function confirmDelete() {
    return confirm('Transaction will be deleted. Are you sure?');
}

// EDIT TRANSACTION 
function edit_Transaction(transactionId) {
    // SHOW CARD
    var card = document.getElementById("Edit-Transaction-Card");
    if (card.style.display === "none" || card.style.display === "") {
        card.style.display = "block";
    } else {
        card.style.display = "none";
    }

    // Fetch transaction data
    fetch(`/project/edit-transaction/${transactionId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Populate the form
                document.querySelector('#edit-date').value = data.transaction.Date;
                document.querySelector('#edit-transaction-type').value = data.transaction.Transaction_type;
                document.querySelector('#edit-amount').value = data.transaction.Amount;
                document.querySelector('#edit-description').value = data.transaction.Description;
                document.querySelector('#edit-category').value = data.transaction.Category;
            } else {
                alert('Error fetching transaction data');
            }
        });
}

// Attach event listeners to edit buttons
document.querySelectorAll('#Edit-Transaction-Button').forEach(button => {
    button.addEventListener('click', function () {
        const transactionId = this.dataset.id;
        edit_Transaction(transactionId);
    });
});

// Handle save button click
document.querySelector('#save-button').addEventListener('click', async function () {
    const form = document.querySelector('#edit-transaction-form');
    const formData = new FormData(form);

    const response = await fetch(form.action, {
        method: 'POST',
        body: formData,
    });
    const data = await response.json();

    if (data.status === 'success') {
        alert(data.message);
        document.querySelector('#edit-card').style.display = 'none';
        // Refresh the table or update the edited row
    } else {
        alert('Error saving transaction');
    }
});

