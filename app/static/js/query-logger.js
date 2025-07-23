/**
 * Query Logger - Captures search queries from the search bar and logs them to console
 * This file extracts the query value and console logs it for debugging/monitoring
 */

class QueryLogger {
    constructor() {
        this.currentQuery = '';
        this.searchInput = null;
        
        this.init();
    }

    async init() {
        console.log('=== Query Logger Init Starting ===');
        
        // Find the search input field
        this.searchInput = document.querySelector('input[name="q"]');
        
        if (!this.searchInput) {
            console.log('Search input not found - will retry...');
            // Retry after a short delay in case the DOM isn't fully loaded
            setTimeout(async () => {
                this.searchInput = document.querySelector('input[name="q"]');
                if (this.searchInput) {
                    this.setupEventListeners();
                    await this.captureCurrentQuery();
                }
            }, 500);
            return;
        }
        
        this.setupEventListeners();
        await this.captureCurrentQuery();
        
        console.log('=== Query Logger Init Complete ===');
    }

    setupEventListeners() {
        if (!this.searchInput) return;
        
        // Monitor form submissions
        const searchForm = this.searchInput.closest('form');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                this.logQuery('Form Submit');
            });
        }
        
        // Monitor Enter key presses
        this.searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.logQuery('Enter Key');
            }
        });
        
        // Monitor input changes (real-time)
        this.searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            if (query) {
                console.log('Query input changed:', query);
            }
        });
        
        // Monitor search button clicks
        const searchButton = document.querySelector('button[type="submit"]');
        if (searchButton) {
            searchButton.addEventListener('click', () => {
                this.logQuery('Search Button Click');
            });
        }
    }

    async captureCurrentQuery() {
        if (!this.searchInput) return;
        
        const query = this.searchInput.value.trim();
        
        if (query) {
            console.log('=== CURRENT SEARCH QUERY ===');
            console.log('Query:', query);
            console.log('Query length:', query.length);
            console.log('Query source: Page load');
            console.log('========================');
            
            this.currentQuery = query;
            
            // Check if AI sidebar is enabled before sending to Gemini
            if (this.isAISidebarEnabled()) {
                console.log('AI Sidebar enabled - sending query to Gemini...');
                await this.sendToGemini(query);
                console.log('sendToGemini completed');
            } else {
                console.log('AI Sidebar disabled - skipping Gemini API call');
            }
        }
    }

    async logQuery(source = 'Unknown') {
        if (!this.searchInput) return;
        
        const query = this.searchInput.value.trim();
        
        if (query && query !== this.currentQuery) {
            console.log('=== NEW SEARCH QUERY ===');
            console.log('Query:', query);
            console.log('Query length:', query.length);
            console.log('Query source:', source);
            console.log('Previous query:', this.currentQuery);
            console.log('Timestamp:', new Date().toISOString());
            console.log('=======================');
            
            this.currentQuery = query;
            
            // Check if AI sidebar is enabled before sending to Gemini
            if (this.isAISidebarEnabled()) {
                console.log('AI Sidebar enabled - sending query to Gemini...');
                await this.sendToGemini(query);
            } else {
                console.log('AI Sidebar disabled - skipping Gemini API call');
            }
        } else if (query) {
            console.log('=== REPEATED SEARCH QUERY ===');
            console.log('Query:', query);
            console.log('Query source:', source);
            console.log('============================');
        }
    }

    // Public method to get current query
    getCurrentQuery() {
        if (this.searchInput) {
            return this.searchInput.value.trim();
        }
        return '';
    }

    // Public method to manually trigger query logging
    logCurrentQuery(source = 'Manual') {
        this.logQuery(source);
    }

    // Check if AI sidebar is enabled based on configuration
    isAISidebarEnabled() {
        // Primary check: look for the AI sidebar element in DOM
        // If the backend config.ai_sidebar is false, the sidebar won't be rendered
        const aiSidebar = document.getElementById('right-sidebar');
        if (!aiSidebar) {
            console.log('AI Sidebar not found in DOM - setting is disabled');
            return false;
        }
        
        // Secondary check: look for config form setting (for settings modal)
        const configForm = document.getElementById('config-form');
        if (configForm) {
            const aiSidebarInput = configForm.querySelector('input[name="ai_sidebar"]');
            if (aiSidebarInput) {
                console.log('AI Sidebar setting found in config form:', aiSidebarInput.checked);
                return aiSidebarInput.checked;
            }
        }
        
        // If sidebar exists in DOM but no form setting found, it means it's enabled
        console.log('AI Sidebar exists in DOM - setting is enabled');
        return true;
    }

    // Update sidebar with different states (loading, response, error)
    updateSidebar(state, query, response = null) {
        // Check if AI sidebar is enabled first
        if (!this.isAISidebarEnabled()) {
            console.log('AI Sidebar disabled - hiding sidebar');
            const sidebar = document.getElementById('right-sidebar');
            if (sidebar) {
                sidebar.style.display = 'none';
            }
            return;
        }
        
        const sidebar = document.getElementById('right-sidebar');
        if (!sidebar) return;
        
        // Show sidebar if AI is enabled
        sidebar.style.display = 'block';
        
        const content = sidebar.querySelector('.sidebar-content');
        if (!content) return;
        
        switch(state) {
            case 'loading':
                content.innerHTML = `
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 300px; text-align: center;">
                        <div style="margin-bottom: 24px;">
                            <div class="ai-loader"></div>
                        </div>
                        <h3 style="margin: 0 0 12px 0; color: #1976d2; font-size: 18px; font-weight: 500;">Getting AI Response</h3>
                        <p style="color: #5f6368; font-size: 14px; margin: 0; line-height: 1.4;">Processing your query...</p>
                    </div>
                    <style>
                        .ai-loader {
                            width: 60px;
                            height: 60px;
                            position: relative;
                            margin: 0 auto;
                            display: inline-block;
                        }
                        .ai-loader::before {
                            content: '';
                            position: absolute;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            border: 4px solid #e0e0e0;
                            border-top: 4px solid #1976d2;
                            border-radius: 50%;
                            animation: spinLoader 1s linear infinite;
                        }
                        @keyframes spinLoader {
                            0% { transform: rotate(0deg); }
                            100% { transform: rotate(360deg); }
                        }
                    </style>
                `;
                break;
                
            case 'response':
                // Process markdown formatting in the response
                const processedResponse = this.processMarkdown(response);
                
                content.innerHTML = `
                    <div style="padding: 24px;">
                        <h3 style="margin: 0 0 20px 0; color: #1976d2; font-size: 18px; font-weight: 500;">
                            AI Response
                        </h3>
                        <div style="background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            <div style="color: #202124; font-size: 15px; line-height: 1.6; margin: 0;">${processedResponse}</div>
                        </div>
                        <p style="color: #5f6368; font-size: 12px; margin: 0; text-align: center; font-weight: 500;">Powered by Google Gemini</p>
                    </div>
                `;
                break;
                
            case 'error':
                content.innerHTML = `
                    <div style="padding: 24px; text-align: center;">
                        <h3 style="margin: 0 0 20px 0; color: #d32f2f; font-size: 18px; font-weight: 500; display: flex; align-items: center; justify-content: center;">
                            <span style="margin-right: 10px; font-size: 20px;">⚠️</span>
                            Error
                        </h3>
                        <div style="background: #ffebee; border: 1px solid #ffcdd2; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                            <p style="color: #d32f2f; font-size: 15px; margin: 0; line-height: 1.4;">Unable to get AI response. Please try again later.</p>
                        </div>
                    </div>
                `;
                break;
        }
    }

    // Process markdown formatting in text
    processMarkdown(text) {
        if (!text) return '';
        
        // Convert **text** to <strong>text</strong>
        let processed = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Convert *text* to <em>text</em>
        processed = processed.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Convert line breaks to <br> tags
        processed = processed.replace(/\n/g, '<br>');
        
        return processed;
    }

    // Send query to Gemini API and display response in sidebar
    async sendToGemini(query) {
        console.log('🚀 sendToGemini function called with query:', query);
        
        // Show loading message in sidebar
        this.updateSidebar('loading', query);
        
        try {
            console.log('=== SENDING TO GEMINI API ===');
            console.log('Query being sent:', query);
            console.log('Fetch URL:', '/gemini-query');
            console.log('Request payload:', JSON.stringify({ query: query }));
            
            const response = await fetch('/gemini-query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query })
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);

            if (!response.ok) {
                const errorText = await response.text();
                console.log('Error response body:', errorText);
                throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
            }

            const data = await response.json();
            
            console.log('=== GEMINI API RESPONSE ===');
            console.log('Status:', data.status);
            console.log('Response:', data.response);
            console.log('Query processed:', data.query);
            console.log('Response length:', data.response ? data.response.length : 0);
            console.log('Full response object:', data);
            console.log('==========================');
            
            // Display AI response in sidebar
            this.updateSidebar('response', query, data.response);
            
        } catch (error) {
            console.error('=== GEMINI API ERROR ===');
            console.error('Error:', error.message);
            console.error('Error stack:', error.stack);
            console.error('Query that failed:', query);
            console.error('========================');
            
            // Show error message in sidebar
            this.updateSidebar('error', query, error.message);
        }
    }
}

// Initialize Query Logger when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Small delay to ensure all elements are loaded
    setTimeout(() => {
        window.queryLogger = new QueryLogger();
    }, 100);
});

// Also initialize when window loads (fallback)
window.addEventListener('load', () => {
    setTimeout(() => {
        if (!window.queryLogger) {
            window.queryLogger = new QueryLogger();
        }
    }, 200);
});

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QueryLogger;
}