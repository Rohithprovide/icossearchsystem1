// Voice Search Implementation for Whoogle Search
// Provides Google-like voice search functionality with UI transformation

class VoiceSearch {
    constructor() {
        this.isVoiceMode = false;
        this.isListening = false;
        this.hasTranscript = false;
        this.noSpeechTimeout = null;
        this.init();
    }

    init() {
        // Initialize voice search when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupVoiceSearch());
        } else {
            this.setupVoiceSearch();
        }
    }

    setupVoiceSearch() {        
        this.searchBar = document.getElementById('search-bar');
        this.micButton = document.querySelector('.fa-microphone, .fa-solid.fa-microphone');
        
        if (!this.searchBar || !this.micButton) {
            // Voice search elements not found - disabling voice search functionality
            console.log('Voice search elements not available - voice search disabled');
            return;
        }

        // Check for speech recognition support
        if (!this.checkSpeechRecognitionSupport()) {
            console.warn('Speech recognition not supported in this browser');
            return;
        }

        // Setup speech recognition
        this.setupSpeechRecognition();
        
        // Add click handler to microphone button
        this.micButton.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleVoiceSearch();
        });

        // Create voice search UI elements
        this.createVoiceSearchUI();
        
        console.log('Voice search initialized successfully');
    }

    checkSpeechRecognitionSupport() {
        return 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
    }

    setupSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateVoiceUI('listening');
            
            // Set a timeout to show "no speech" message if no speech is detected
            this.noSpeechTimeout = setTimeout(() => {
                if (this.isVoiceMode && !this.hasTranscript) {
                    this.showNoSpeechMessage();
                }
            }, 5000); // 5 seconds timeout
        };
        
        this.recognition.onresult = (event) => {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            
            if (this.isVoiceMode) {
                this.updateListeningText(transcript);
                this.hasTranscript = true; // Mark that we received some speech
                
                // Clear the no speech timeout since we got speech
                if (this.noSpeechTimeout) {
                    clearTimeout(this.noSpeechTimeout);
                    this.noSpeechTimeout = null;
                }
                
                // If result is final, perform search
                if (event.results[event.results.length - 1].isFinal) {
                    this.performVoiceSearch(transcript);
                }
            }
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.stopVoiceSearch();
            this.updateVoiceUI('error');
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            if (this.isVoiceMode) {
                // Check if no speech was captured
                if (!this.hasTranscript) {
                    this.showNoSpeechMessage();
                } else {
                    this.updateVoiceUI('idle');
                }
            }
        };
    }

    createVoiceSearchUI() {
        // Create voice search overlay
        this.voiceSearchContainer = document.createElement('div');
        this.voiceSearchContainer.className = 'voice-search-overlay';
        this.voiceSearchContainer.style.display = 'none';
        
        this.voiceSearchContainer.innerHTML = `
            <div class="voice-search-content">
                <div class="voice-search-header">
                    <div class="voice-listening-text">Listening...</div>
                </div>
                <div class="voice-microphone-container">
                    <div class="voice-microphone-icon">
                        <i class="fa-solid fa-microphone"></i>
                    </div>
                    <div class="voice-pulse-animation"></div>
                </div>
                <div class="voice-transcript-text"></div>
                <div class="voice-instructions">Try saying: "What's the weather today?"</div>
            </div>
        `;
        
        document.body.appendChild(this.voiceSearchContainer);
        
        // Force white background on content with inline styles
        const contentDiv = this.voiceSearchContainer.querySelector('.voice-search-content');
        if (contentDiv) {
            contentDiv.style.background = '#ffffff';
            contentDiv.style.backgroundColor = '#ffffff';
            contentDiv.style.opacity = '1';
            contentDiv.style.backdropFilter = 'none';
            contentDiv.style.webkitBackdropFilter = 'none';
        }
        
        // Add click outside to close
        this.voiceSearchContainer.addEventListener('click', (e) => {
            if (e.target === this.voiceSearchContainer) {
                this.stopVoiceSearch();
            }
        });
    }

    toggleVoiceSearch() {
        if (this.isVoiceMode) {
            this.stopVoiceSearch();
        } else {
            this.startVoiceSearch();
        }
    }

    startVoiceSearch() {
        this.isVoiceMode = true;
        this.hasTranscript = false; // Reset transcript flag
        this.voiceSearchContainer.style.display = 'flex';
        
        // Add body class to prevent scrolling
        document.body.classList.add('voice-search-active');
        
        // Start speech recognition
        try {
            this.recognition.start();
        } catch (error) {
            console.error('Failed to start speech recognition:', error);
            this.stopVoiceSearch();
        }
    }

    showNoSpeechMessage() {
        const listeningText = this.voiceSearchContainer.querySelector('.voice-listening-text');
        const micIcon = this.voiceSearchContainer.querySelector('.voice-microphone-icon');
        const pulseAnimation = this.voiceSearchContainer.querySelector('.voice-pulse-animation');
        
        // Update UI to show no speech message
        listeningText.textContent = 'No speech was found';
        micIcon.classList.remove('listening');
        pulseAnimation.classList.remove('active');
        
        // Auto-close after 2 seconds
        setTimeout(() => {
            this.stopVoiceSearch();
        }, 2000);
    }

    stopVoiceSearch() {
        this.isVoiceMode = false;
        this.isListening = false;
        
        // Clear any pending timeout
        if (this.noSpeechTimeout) {
            clearTimeout(this.noSpeechTimeout);
            this.noSpeechTimeout = null;
        }
        
        if (this.recognition) {
            this.recognition.stop();
        }
        
        this.voiceSearchContainer.style.display = 'none';
        document.body.classList.remove('voice-search-active');
        
        // Reset UI
        this.updateVoiceUI('idle');
    }

    updateVoiceUI(state) {
        const listeningText = this.voiceSearchContainer.querySelector('.voice-listening-text');
        const micIcon = this.voiceSearchContainer.querySelector('.voice-microphone-icon');
        const pulseAnimation = this.voiceSearchContainer.querySelector('.voice-pulse-animation');
        
        switch (state) {
            case 'listening':
                listeningText.textContent = 'Listening...';
                micIcon.classList.add('listening');
                pulseAnimation.classList.add('active');
                break;
            case 'processing':
                listeningText.textContent = 'Processing...';
                micIcon.classList.remove('listening');
                pulseAnimation.classList.remove('active');
                break;
            case 'error':
                listeningText.textContent = 'Sorry, I didn\'t catch that. Try again.';
                micIcon.classList.remove('listening');
                pulseAnimation.classList.remove('active');
                break;
            default:
                listeningText.textContent = 'Listening...';
                micIcon.classList.remove('listening');
                pulseAnimation.classList.remove('active');
        }
    }

    updateListeningText(transcript) {
        const transcriptElement = this.voiceSearchContainer.querySelector('.voice-transcript-text');
        transcriptElement.textContent = transcript;
    }

    performVoiceSearch(query) {
        if (!query.trim()) return;
        
        this.updateVoiceUI('processing');
        
        // Fill the search bar with the recognized text
        this.searchBar.value = query;
        
        // Submit the search form
        setTimeout(() => {
            const searchForm = document.getElementById('search-form');
            if (searchForm) {
                searchForm.submit();
            }
        }, 500);
    }
}

// Initialize voice search
const voiceSearch = new VoiceSearch();