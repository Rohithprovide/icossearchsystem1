// Search Clear Icon Functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchBar = document.getElementById('search-bar');
    const clearIcon = document.getElementById('home-search-clear');
    const headerClearIcon = document.getElementById('search-clear');
    const headerSearchBar = document.querySelector('.search-bar-desktop');

    // Function to toggle clear icon visibility for homepage
    function toggleClearIcon() {
        if (searchBar && clearIcon) {
            const divider = document.getElementById('search-divider');
            if (searchBar.value.trim().length > 0) {
                clearIcon.style.display = 'block';
                if (divider) divider.style.display = 'block';
            } else {
                clearIcon.style.display = 'none';
                if (divider) divider.style.display = 'none';
            }
        }
    }

    // Function to toggle header clear icon visibility
    function toggleHeaderClearIcon() {
        if (headerSearchBar && headerClearIcon) {
            if (headerSearchBar.value.trim().length > 0) {
                headerClearIcon.classList.add('show');
            } else {
                headerClearIcon.classList.remove('show');
            }
        }
    }

    // Function to clear search input
    function clearSearch() {
        if (searchBar) {
            searchBar.value = '';
            searchBar.focus();
            toggleClearIcon();
        }
    }

    // Function to clear header search
    function clearHeaderSearch() {
        if (headerSearchBar) {
            headerSearchBar.value = '';
            headerSearchBar.focus();
            toggleHeaderClearIcon();
        }
    }

    // Add event listeners for homepage search bar
    if (searchBar && clearIcon) {
        // Show/hide clear icon on input
        searchBar.addEventListener('input', toggleClearIcon);
        searchBar.addEventListener('keyup', toggleClearIcon);
        searchBar.addEventListener('paste', function() {
            setTimeout(toggleClearIcon, 10);
        });

        // Clear search when icon is clicked
        clearIcon.addEventListener('click', clearSearch);

        // Initial check
        toggleClearIcon();
    }

    // Add event listeners for header search bar (search results page)
    if (headerSearchBar && headerClearIcon) {
        // Show/hide clear icon on input
        headerSearchBar.addEventListener('input', toggleHeaderClearIcon);
        headerSearchBar.addEventListener('keyup', toggleHeaderClearIcon);
        headerSearchBar.addEventListener('paste', function() {
            setTimeout(toggleHeaderClearIcon, 10);
        });

        // Clear search when icon is clicked
        headerClearIcon.addEventListener('click', clearHeaderSearch);

        // Initial check
        toggleHeaderClearIcon();
    }

    // Global function for header clear (used in HTML onclick)
    window.clearSearch = function() {
        if (headerSearchBar) {
            clearHeaderSearch();
        } else if (searchBar) {
            clearSearch();
        }
    };
});