/**
 * Transform pagination to Google-style numbered pagination
 */

document.addEventListener('DOMContentLoaded', function() {
    transformPagination();
});

// Also run when the page URL changes (for single-page navigation)
window.addEventListener('popstate', function() {
    // Small delay to ensure DOM is updated
    setTimeout(transformPagination, 100);
});

function transformPagination() {
    // Find the pagination container (usually table.uZgmoc)
    const paginationTable = document.querySelector('table.uZgmoc');
    
    if (!paginationTable) {
        return; // No pagination found
    }
    
    // Get current page number from URL or assume page 1
    const urlParams = new URLSearchParams(window.location.search);
    const currentStart = parseInt(urlParams.get('start')) || 0;
    // Check search type and set appropriate results per page
    const searchType = urlParams.get('tbm');
    let resultsPerPage;
    
    if (searchType === 'isch') {
        // Images tab - 100 results per page
        resultsPerPage = 100;
    } else if (!searchType || searchType === '' || searchType === 'vid' || searchType === 'nws') {
        // All, Videos, and News tabs - 15 results per page
        resultsPerPage = 15;
    } else {
        // Other tabs (maps, etc.) - keep original 10 results per page
        resultsPerPage = 10;
    }
    const currentPage = Math.floor(currentStart / resultsPerPage) + 1;
    
    // Create new pagination structure
    const newPagination = createGoogleStylePagination(currentPage, paginationTable, resultsPerPage);
    
    // Replace old pagination with new one
    if (newPagination) {
        paginationTable.parentNode.replaceChild(newPagination, paginationTable);
    }
}

function createGoogleStylePagination(currentPage, originalTable, resultsPerPage = 10) {
    // Extract links from original pagination
    const originalLinks = originalTable.querySelectorAll('a');
    const links = [];
    
    originalLinks.forEach(link => {
        const href = link.getAttribute('href');
        const text = link.textContent.trim();
        
        if (href) {
            links.push({ href, text });
        }
    });
    
    // If no links found, return null
    if (links.length === 0) {
        return null;
    }
    
    // Create new pagination container
    const paginationDiv = document.createElement('div');
    paginationDiv.className = 'google-pagination';
    paginationDiv.style.cssText = `
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 30px 0;
        gap: 4px;
        font-family: arial, sans-serif;
    `;
    
    // Generate page numbers (show current page ± 2 pages)
    const startPage = Math.max(1, currentPage - 2);
    const endPage = currentPage + 2;
    
    // Add page numbers
    for (let i = startPage; i <= endPage; i++) {
        const pageElement = createPageElement(i, currentPage, links, resultsPerPage);
        if (pageElement) {
            paginationDiv.appendChild(pageElement);
        }
    }
    

    
    // Add "Next" button if available
    const nextLink = links.find(link => 
        link.text.toLowerCase().includes('next') || 
        link.text.includes('>')
    );
    
    if (nextLink) {
        const nextElement = createNextElement(nextLink, currentPage, resultsPerPage);
        paginationDiv.appendChild(nextElement);
    }
    
    return paginationDiv;
}

function createPageElement(pageNum, currentPage, links, resultsPerPage = 10) {
    const isCurrentPage = pageNum === currentPage;
    
    if (isCurrentPage) {
        // Current page (with blue underline)
        const span = document.createElement('span');
        span.textContent = pageNum;
        span.className = 'current-page';
        span.style.cssText = `
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 40px;
            height: 40px;
            padding: 8px 16px;
            margin: 0 4px;
            font-size: 14px;
            color: #1a73e8;
            font-weight: 500;
            border-bottom: 3px solid #4285f4;
            border-radius: 0;
            background: transparent;
            box-sizing: border-box;
        `;
        return span;
    } else {
        // Calculate the start parameter for this page
        const start = (pageNum - 1) * resultsPerPage;
        
        // Find a link that might work for this page or construct URL
        const currentUrl = new URL(window.location);
        currentUrl.searchParams.set('start', start);
        
        const link = document.createElement('a');
        link.href = currentUrl.toString();
        link.textContent = pageNum;
        link.className = 'page-link';
        link.style.cssText = `
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 40px;
            height: 40px;
            padding: 8px 16px;
            margin: 0 4px;
            font-size: 14px;
            color: #1a73e8;
            text-decoration: none;
            border-radius: 50%;
            background: transparent;
            transition: background-color 0.3s ease;
            box-sizing: border-box;
        `;
        
        // Add hover effect
        link.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.backgroundColor = 'transparent';
        });
        

        
        return link;
    }
}

function createNextElement(nextLink, currentPage, resultsPerPage) {
    const link = document.createElement('a');
    
    // Calculate next page URL properly
    const nextPageStart = currentPage * resultsPerPage;
    const currentUrl = new URL(window.location);
    currentUrl.searchParams.set('start', nextPageStart);
    
    link.href = currentUrl.toString();
    link.textContent = '>';
    link.className = 'next-link';
    link.style.cssText = `
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 40px;
        height: 40px;
        padding: 8px 12px;
        margin: 0 4px;
        font-size: 14px;
        color: #5f6368;
        text-decoration: none;
        border-radius: 4px;
        background: transparent;
        transition: background-color 0.3s ease;
        box-sizing: border-box;
    `;
    
    // Add hover effect
    link.addEventListener('mouseenter', function() {
        this.style.backgroundColor = '#f8f9fa';
    });
    
    link.addEventListener('mouseleave', function() {
        this.style.backgroundColor = 'transparent';
    });
    

    
    return link;
}

// Handle theme changes
function updatePaginationTheme() {
    const isDark = document.body.classList.contains('dark') || 
                   document.documentElement.getAttribute('data-theme') === 'dark';
    
    if (isDark) {
        const pageLinks = document.querySelectorAll('.page-link, .next-link');
        pageLinks.forEach(link => {
            link.style.color = '#8ab4f8';
        });
        
        const currentPage = document.querySelector('.current-page');
        if (currentPage) {
            currentPage.style.color = '#8ab4f8';
            currentPage.style.borderBottomColor = '#8ab4f8';
        }
    }
}

// Watch for theme changes
const observer = new MutationObserver(updatePaginationTheme);
observer.observe(document.body, { 
    attributes: true, 
    attributeFilter: ['class', 'data-theme'] 
});
observer.observe(document.documentElement, { 
    attributes: true, 
    attributeFilter: ['data-theme'] 
});