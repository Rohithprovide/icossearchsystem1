// Settings Modal JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const settingsIcon = document.getElementById('settings-icon');
    const modal = document.getElementById('settings-modal');
    const closeModal = document.getElementById('close-modal');

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
        if (event.key === 'Escape' && modal && modal.style.display === 'block') {
            closeModalFunc();
        }
    });
});