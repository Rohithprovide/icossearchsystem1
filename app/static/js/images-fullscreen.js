// Images Full Screen Layout Handler

class ImagesFullscreenHandler {
    constructor() {
        this.init();
    }

    init() {
        // Check if we're on the images tab and apply full screen layout
        this.checkAndApplyImagesLayout();
        
        // Monitor for navigation changes to other tabs
        this.monitorTabChanges();
    }

    checkAndApplyImagesLayout() {
        const urlParams = new URLSearchParams(window.location.search);
        const tbm = urlParams.get('tbm');
        
        console.log('ImagesFullscreenHandler: Checking layout - URL:', window.location.href);
        console.log('ImagesFullscreenHandler: tbm parameter:', tbm);
        
        // Check if we're on the images tab
        const isImagesTab = tbm === 'isch';
        
        if (isImagesTab) {
            // We're on the images tab
            document.body.classList.add('images-tab');
            console.log('ImagesFullscreenHandler: ✓ Applied full screen layout for images tab');
            console.log('ImagesFullscreenHandler: Body classes:', document.body.className);
            
            // Also add a data attribute for CSS targeting
            document.body.setAttribute('data-images-fullscreen', 'true');
            
            // Force immediate layout application
            this.forceLayoutUpdate();
        } else {
            // We're not on the images tab
            document.body.classList.remove('images-tab');
            document.body.removeAttribute('data-images-fullscreen');
            console.log('ImagesFullscreenHandler: ✗ Removed full screen layout, not on images tab');
        }
    }
    
    forceLayoutUpdate() {
        // Simplified layout update without expensive reflow operations
        this.applyDirectStyles();
    }
    
    applyDirectStyles() {
        // Directly override styles using JavaScript for immediate effect
        const main = document.getElementById('main');
        if (main) {
            main.style.marginLeft = '0';
            main.style.marginRight = '0';
            main.style.maxWidth = '100%';
            main.style.width = '100%';
            main.style.paddingLeft = '0';
            main.style.paddingRight = '0';
        }
        
        // Target all direct children of body (excluding header elements)
        const bodyChildren = Array.from(document.body.children);
        bodyChildren.forEach(child => {
            if (!child.className.includes('header') && !child.id.includes('header')) {
                child.style.marginLeft = '0';
                child.style.marginRight = '0';
                child.style.maxWidth = '100%';
                child.style.width = '100%';
            }
        });
        
        // Target the image container specifically
        const imageContainer = document.querySelector('.GpQGbf');
        if (imageContainer) {
            imageContainer.style.marginLeft = '0';
            imageContainer.style.marginRight = '0';
            imageContainer.style.maxWidth = '100%';
            imageContainer.style.width = '100%';
        }
        
        console.log('ImagesFullscreenHandler: Applied direct styles for full screen layout');
        
        // Force rebuild of image grid with proper columns
        this.rebuildImageGrid();
    }
    
    rebuildImageGrid() {
        const imageTable = document.querySelector('.GpQGbf');
        if (!imageTable) return;
        
        // Get all existing image cells
        const imageCells = Array.from(imageTable.querySelectorAll('td.e3goi'));
        if (imageCells.length === 0) return;
        
        console.log('ImagesFullscreenHandler: Optimizing', imageCells.length, 'images for quality and spacing');
        
        // Optimize each image for quality preservation
        imageCells.forEach(cell => {
            const imageContainer = cell.querySelector('.RAyV4b');
            const image = cell.querySelector('.t0fcAb');
            
            if (imageContainer && image) {
                // Preserve original aspect ratio and reduce artificial sizing
                image.style.width = 'auto';
                image.style.height = 'auto';
                image.style.maxWidth = this.getOptimalImageSize() + 'px';
                image.style.maxHeight = this.getOptimalImageSize() + 'px';
                image.style.objectFit = 'contain';
                
                imageContainer.style.width = 'auto';
                imageContainer.style.height = 'auto';
                imageContainer.style.maxWidth = this.getOptimalImageSize() + 'px';
                imageContainer.style.maxHeight = this.getOptimalImageSize() + 'px';
                imageContainer.style.lineHeight = 'normal';
                imageContainer.style.overflow = 'visible';
                
                // Reduce spacing between images
                cell.style.padding = '4px';
                cell.style.margin = '0';
                cell.style.width = 'auto';
                cell.style.height = 'auto';
            }
        });
        
        // Create flexible layout instead of fixed table
        imageTable.innerHTML = '';
        
        // Create a wrapper div for flexible layout
        const flexWrapper = document.createElement('div');
        flexWrapper.style.display = 'flex';
        flexWrapper.style.flexWrap = 'wrap';
        flexWrapper.style.gap = '8px';
        flexWrapper.style.alignItems = 'flex-start';
        flexWrapper.style.justifyContent = 'flex-start';
        flexWrapper.style.width = '100%';
        flexWrapper.style.padding = '0';
        flexWrapper.style.margin = '0';
        
        // Add all images to the flexible container
        imageCells.forEach(cell => {
            cell.style.flex = '0 0 auto';
            cell.style.display = 'block';
            flexWrapper.appendChild(cell);
        });
        
        // Wrap the flex container in table structure for compatibility
        const row = document.createElement('tr');
        const tableCell = document.createElement('td');
        tableCell.style.width = '100%';
        tableCell.style.padding = '0';
        tableCell.style.margin = '0';
        tableCell.appendChild(flexWrapper);
        row.appendChild(tableCell);
        imageTable.appendChild(row);
        
        console.log('ImagesFullscreenHandler: Optimized layout with preserved image quality and reduced spacing');
    }
    
    getOptimalImageSize() {
        const screenWidth = window.innerWidth;
        // Smaller sizes to fit 6-7 images per row without stretching
        if (screenWidth >= 1920) return 120;  // ~7-8 images per row
        if (screenWidth >= 1400) return 110;  // ~6-7 images per row
        if (screenWidth >= 1024) return 100;  // ~6 images per row
        if (screenWidth >= 768) return 90;    // ~5 images per row
        if (screenWidth >= 480) return 70;    // ~4 images per row
        return 50;                            // ~3 images per row
    }

    monitorTabChanges() {
        // Monitor clicks on navigation tabs - be more specific about Images tab
        document.addEventListener('click', (event) => {
            const target = event.target.closest('a');
            if (target && (target.href.includes('tbm=isch') || target.textContent.includes('Images'))) {
                console.log('ImagesFullscreenHandler: Images tab clicked, applying layout');
                setTimeout(() => {
                    this.checkAndApplyImagesLayout();
                }, 200);
            }
        });

        // Monitor URL changes for single page navigation
        let currentUrl = window.location.href;
        const urlObserver = new MutationObserver(() => {
            if (currentUrl !== window.location.href) {
                currentUrl = window.location.href;
                console.log('ImagesFullscreenHandler: URL changed, checking layout');
                this.checkAndApplyImagesLayout();
            }
        });

        urlObserver.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Also monitor popstate events for browser navigation
        window.addEventListener('popstate', () => {
            setTimeout(() => {
                this.checkAndApplyImagesLayout();
            }, 200);
        });
        
        // Monitor window resize to rebuild grid
        window.addEventListener('resize', () => {
            if (document.body.classList.contains('images-tab')) {
                this.rebuildImageGrid();
            }
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ImagesFullscreenHandler();
});

// Also initialize immediately in case DOM is already loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ImagesFullscreenHandler();
    });
} else {
    new ImagesFullscreenHandler();
}