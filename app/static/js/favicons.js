/**
 * Favicon functionality for Whoogle Search
 * Adds website favicons to search results dynamically and removes Google icons
 */

function removeGoogleIcons() {
    // Remove Google logos and icons from footer and search results
    // Avoid touching navigation elements to prevent conflicts with Maps icon
    const googleElements = document.querySelectorAll(`
        img[src*="googlelogo"],
        img[src*="google.com/images/branding"],
        img[alt*="Google"],
        img[title*="Google"],
        svg[class*="google"],
        .google-icon,
        .gicon,
        [aria-label*="Google"],
        [title*="Google logo"],
        [alt*="Google logo"],
        [class*="google-logo"],
        [class*="googlelogo"],
        [id*="google-logo"],
        [id*="googlelogo"],
        svg[viewBox*="0 0 272 92"],
        svg[viewBox*="0 0 136 46"]
    `);
    
    googleElements.forEach(element => {
        // Only remove if it's clearly not part of navigation
        if (!element.closest('.desktop-header') && 
            !element.closest('.mobile-header') && 
            !element.closest('[role="navigation"]') &&
            !element.closest('.header-tab-div')) {
            element.remove();
        }
    });
    
    // Remove footer elements containing location, privacy, terms (but preserve search results)
    const footerTexts = ['mumbai', 'maharashtra', 'from your ip address', 'privacy', 'terms'];
    const allDivs = document.querySelectorAll('div');
    
    allDivs.forEach(div => {
        const text = div.textContent.toLowerCase().trim();
        const hasFooterText = footerTexts.some(footerText => text.includes(footerText));
        
        if (hasFooterText) {
            // Only remove if it's small (footer-like) and doesn't contain search result indicators
            const isSmall = text.length < 200;
            const hasSearchIndicators = /www\.|http|\.com|\.org|search|result/.test(text);
            const isNotNavigation = !div.closest('.desktop-header') && 
                                   !div.closest('.mobile-header') && 
                                   !div.closest('[role="navigation"]') &&
                                   !div.closest('.header-tab-div');
            
            if (isSmall && !hasSearchIndicators && isNotNavigation) {
                div.remove();
            }
        }
    });
    
    // Remove Privacy and Terms links specifically
    const privacyTermsLinks = document.querySelectorAll('a[href*="privacy"], a[href*="terms"]');
    privacyTermsLinks.forEach(link => {
        const parent = link.parentElement;
        // If parent only contains footer-type links, remove the parent
        if (parent && parent.querySelectorAll('a').length <= 3) {
            parent.remove();
        } else {
            link.remove();
        }
    });
    
    // Remove "Next >" pagination at bottom if it's in a footer context
    const nextElements = document.querySelectorAll('*');
    nextElements.forEach(element => {
        if (element.textContent.trim().toLowerCase() === 'next >') {
            const parent = element.parentElement;
            if (parent && parent.textContent.trim().length < 50) {
                parent.remove();
            }
        }
    });
    
    // Also remove parent containers that only contain Google logos
    const containerSelectors = [
        'div:has(img[src*="google"])',
        'div:has(img[alt*="Google"])',
        'span:has(img[src*="google"])',
        'a:has(img[src*="google"])'
    ];
    
    containerSelectors.forEach(selector => {
        try {
            const containers = document.querySelectorAll(selector);
            containers.forEach(container => {
                if (!container.closest('.desktop-header') && 
                    !container.closest('.mobile-header') && 
                    !container.closest('[role="navigation"]') &&
                    !container.closest('.header-tab-div')) {
                    container.remove();
                }
            });
        } catch (e) {
            // Some browsers might not support :has() selector
        }
    });
}

function addFavicons() {
    // Find all result links that should have favicons - be very specific
    const resultLinks = document.querySelectorAll('a[href*="://"]');
    
    resultLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // Skip if not a proper external link or already has favicon
        if (!href || !href.startsWith('http') || 
            link.querySelector('.site-favicon') || 
            link.previousElementSibling?.classList.contains('site-favicon')) {
            return;
        }
        
        // Skip ALL Google services and navigation - be very strict
        if (href.includes('google.com') || 
            href.includes('maps.google.com') ||
            href.includes('images.google.com') ||
            href.includes('news.google.com') ||
            href.includes('youtube.com') ||
            href.includes('googleusercontent.com') ||
            href.includes('gstatic.com') ||
            href.includes('search?') ||
            href.includes('tbm=') ||
            href.startsWith('#') ||
            href.includes('javascript:') ||
            link.closest('.desktop-header') ||
            link.closest('.mobile-header') ||
            link.closest('[role="navigation"]') ||
            link.closest('.header-tab-div') ||
            link.closest('.header-container') ||
            link.closest('nav') ||
            // Skip if it's clearly a navigation element by its text content
            (linkText.toLowerCase() === 'maps') ||
            (linkText.toLowerCase() === 'images') ||
            (linkText.toLowerCase() === 'videos') ||
            (linkText.toLowerCase() === 'news') ||
            (linkText.toLowerCase() === 'all')) {
            return;
        }
        
        // Skip if link doesn't have meaningful text (likely not a title link)
        const linkText = link.textContent.trim();
        if (!linkText || linkText.length < 3) {
            return;
        }
        
        // Only add to links that are clearly search results
        const isSearchResult = link.closest('[data-ved]') || 
                              link.closest('.g') || 
                              link.closest('[class*="result"]') ||
                              (link.parentElement && !link.closest('nav'));
        
        if (!isSearchResult) {
            return;
        }
        
        // Extract domain from URL
        try {
            const url = new URL(href);
            const domain = url.hostname;
            
            // Create favicon element
            const favicon = document.createElement('img');
            favicon.className = 'site-favicon';
            favicon.src = `https://www.google.com/s2/favicons?domain=${domain}&sz=32`;
            favicon.alt = '';
            favicon.style.cssText = `
                width: 18px !important;
                height: 18px !important;
                margin-right: 8px !important;
                margin-top: 2px !important;
                border-radius: 50% !important;
                object-fit: cover !important;
                vertical-align: top !important;
                display: inline-block !important;
                flex-shrink: 0 !important;
            `;
            
            // Handle favicon load error - use a fallback
            favicon.onerror = function() {
                this.src = `https://icons.duckduckgo.com/ip3/${domain}.ico`;
                this.onerror = function() {
                    // Final fallback - create a colored circle with first letter
                    const canvas = document.createElement('canvas');
                    canvas.width = 18;
                    canvas.height = 18;
                    const ctx = canvas.getContext('2d');
                    
                    // Generate color based on domain
                    const colors = ['#4285f4', '#34a853', '#fbbc05', '#ea4335', '#9c27b0', '#ff9800'];
                    const colorIndex = domain.charCodeAt(0) % colors.length;
                    
                    ctx.fillStyle = colors[colorIndex];
                    ctx.beginPath();
                    ctx.arc(9, 9, 9, 0, 2 * Math.PI);
                    ctx.fill();
                    
                    ctx.fillStyle = 'white';
                    ctx.font = 'bold 10px Arial';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(domain.charAt(0).toUpperCase(), 9, 9);
                    
                    this.src = canvas.toDataURL();
                    this.onerror = null;
                };
            };
            
            // Insert favicon before the link
            link.parentNode.insertBefore(favicon, link);
            
        } catch (e) {
            console.log('Error adding favicon for:', href, e);
        }
    });
}

// Run when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        removeGoogleIcons();
        addFavicons();
    });
} else {
    removeGoogleIcons();
    addFavicons();
}

// Also run after a short delay to catch any dynamically loaded content
setTimeout(function() {
    removeGoogleIcons();
    addFavicons();
}, 500);

// Run periodically to catch any dynamically loaded footer content
setInterval(function() {
    removeGoogleIcons();
}, 1000);