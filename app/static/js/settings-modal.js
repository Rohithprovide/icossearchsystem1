// Settings Modal JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const settingsIcon = document.getElementById('settings-icon');
    const modal = document.getElementById('settings-modal');
    const closeModal = document.getElementById('close-modal');
    const configForm = document.getElementById('config-form');

    // Function to close modal
    function closeModalFunc() {
        if (modal) {
            modal.classList.remove('modal-open');
            document.body.style.overflow = 'auto';
        }
    }

    // Open modal when settings icon is clicked
    if (settingsIcon && modal) {
        settingsIcon.addEventListener('click', function(e) {
            e.preventDefault();
            modal.classList.add('modal-open');
            document.body.style.overflow = 'hidden';
        });
    }

    // Close modal when X is clicked
    if (closeModal) {
        closeModal.addEventListener('click', function(e) {
            e.preventDefault();
            closeModalFunc();
        });
    }

    // Close modal when clicking outside of it
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                closeModalFunc();
            }
        });
    }

    // Handle ESC key to close modal
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal && modal.classList.contains('modal-open')) {
            closeModalFunc();
        }
    });

    // Handle config form submission
    if (configForm) {
        configForm.addEventListener('submit', function(e) {
            // Don't prevent default - allow form to submit normally
            // The form will submit to /config endpoint and redirect back
            // Close modal after a short delay to allow form submission
            setTimeout(closeModalFunc, 100);
        });
    }
});