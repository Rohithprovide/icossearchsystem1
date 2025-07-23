let searchInput;
let currentFocus;
let originalSearch;
let autocompleteResults;

const handleUserInput = () => {
    let xhrRequest = new XMLHttpRequest();
    xhrRequest.open("POST", "autocomplete");
    xhrRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhrRequest.onload = function () {
        if (xhrRequest.readyState === 4 && xhrRequest.status !== 200) {
            // Do nothing if failed to fetch autocomplete results
            return;
        }

        // Fill autocomplete with fetched results
        autocompleteResults = JSON.parse(xhrRequest.responseText)[1];
        updateAutocompleteList();
    };

    xhrRequest.send('q=' + searchInput.value);
};

const removeActive = suggestion => {
    // Remove "autocomplete-active" class from previously active suggestion
    for (let i = 0; i < suggestion.length; i++) {
        suggestion[i].classList.remove("autocomplete-active");
    }
};

const addActive = (suggestion) => {
    // Handle navigation outside of suggestion list
    if (!suggestion || !suggestion[currentFocus]) {
        if (currentFocus >= suggestion.length) {
            // Move selection back to the beginning
            currentFocus = 0;
        } else if (currentFocus < 0) {
            // Retrieve original search and remove active suggestion selection
            currentFocus = -1;
            searchInput.value = originalSearch;
            removeActive(suggestion);
            return;
        } else {
            return;
        }
    }

    removeActive(suggestion);
    suggestion[currentFocus].classList.add("autocomplete-active");

    // Autofill search bar with suggestion content
    let searchContent = suggestion[currentFocus].textContent;
    if (searchContent.indexOf('(') > 0) {
        searchInput.value = searchContent.substring(0, searchContent.indexOf('('));
    } else {
        searchInput.value = searchContent;
    }

    searchInput.focus();
};

const autocompleteInput = (e) => {
    // Handle navigation between autocomplete suggestions
    let suggestion = document.getElementById("autocomplete-list");
    if (suggestion) suggestion = suggestion.getElementsByTagName("div");
    if (e.keyCode === 40) { // down
        e.preventDefault();
        currentFocus++;
        addActive(suggestion);
    } else if (e.keyCode === 38) { //up
        e.preventDefault();
        currentFocus--;
        addActive(suggestion);
    } else if (e.keyCode === 13) { // enter
        e.preventDefault();
        if (currentFocus > -1) {
            if (suggestion) suggestion[currentFocus].click();
        }
    } else {
        originalSearch = searchInput.value;
    }
};

const updateAutocompleteList = () => {
    let autocompleteItem, i;
    let val = originalSearch;

    let autocompleteList = document.getElementById("autocomplete-list");
    autocompleteList.innerHTML = "";

    if (!val || !autocompleteResults) {
        // Remove active styling when no suggestions
        searchInput.style.borderRadius = "24px";
        searchInput.style.borderBottom = "1px solid #dfe1e5";
        searchInput.style.borderBottomColor = "#dfe1e5";
        return false;
    }

    currentFocus = -1;
    let hasResults = false;

    for (i = 0; i < autocompleteResults.length; i++) {
        if (autocompleteResults[i].substr(0, val.length).toUpperCase() === val.toUpperCase()) {
            autocompleteItem = document.createElement("div");
            autocompleteItem.setAttribute("class", "autocomplete-item");
            autocompleteItem.innerHTML = "<strong>" + autocompleteResults[i].substr(0, val.length) + "</strong>";
            autocompleteItem.innerHTML += autocompleteResults[i].substr(val.length);
            autocompleteItem.innerHTML += "<input type=\"hidden\" value=\"" + autocompleteResults[i] + "\">";
            autocompleteItem.addEventListener("click", function () {
                searchInput.value = this.getElementsByTagName("input")[0].value;
                autocompleteList.innerHTML = "";
                // Reset styling when autocomplete is closed
                searchInput.style.borderRadius = "24px";
                searchInput.style.borderBottom = "1px solid #dfe1e5";
                searchInput.style.borderBottomColor = "#dfe1e5";
                document.getElementById("search-form").submit();
            });
            autocompleteList.appendChild(autocompleteItem);
            hasResults = true;
        }
    }

    // Apply connected styling when suggestions are present
    let autocompleteContainer = searchInput.closest('.autocomplete') || searchInput.closest('.header-autocomplete');
    
    if (hasResults) {
        searchInput.style.borderRadius = "24px 24px 0 0";
        searchInput.style.borderBottom = "none";
        searchInput.style.borderBottomColor = "transparent";
        if (autocompleteContainer) {
            autocompleteContainer.classList.add('has-autocomplete');
        }
    } else {
        searchInput.style.borderRadius = "24px";
        searchInput.style.borderBottom = "1px solid #dfe1e5";
        searchInput.style.borderBottomColor = "#dfe1e5";
        if (autocompleteContainer) {
            autocompleteContainer.classList.remove('has-autocomplete');
        }
    }
};

document.addEventListener("DOMContentLoaded", function() {
    let autocompleteList = document.createElement("div");
    autocompleteList.setAttribute("id", "autocomplete-list");
    autocompleteList.setAttribute("class", "autocomplete-items");

    searchInput = document.getElementById("search-bar");
    
    // Find the proper autocomplete container (either .autocomplete or .header-autocomplete)
    let autocompleteContainer = searchInput.closest('.autocomplete') || searchInput.closest('.header-autocomplete');
    if (autocompleteContainer) {
        autocompleteContainer.appendChild(autocompleteList);
    } else {
        searchInput.parentNode.appendChild(autocompleteList);
    }

    searchInput.addEventListener("keydown", (event) => autocompleteInput(event));

    document.addEventListener("click", function (e) {
        autocompleteList.innerHTML = "";
        // Reset search bar styling when clicking outside
        if (searchInput) {
            searchInput.style.borderRadius = "24px";
            searchInput.style.borderBottom = "1px solid #dfe1e5";
            searchInput.style.borderBottomColor = "#dfe1e5";
            
            // Remove autocomplete class from container
            let autocompleteContainer = searchInput.closest('.autocomplete') || searchInput.closest('.header-autocomplete');
            if (autocompleteContainer) {
                autocompleteContainer.classList.remove('has-autocomplete');
            }
        }
    });
});
