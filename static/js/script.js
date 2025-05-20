// Main JavaScript file for MoodMusic application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips & popovers
    initializeTooltips();
    initializePopovers();
    
    // Auto-hide alerts with animation
    setupAlertDismissal();
    
    // Mood selection enhancement
    setupMoodSelection();
    
    // Audio player enhancements
    setupAudioPlayers();
    
    // Add scroll animations
    setupScrollAnimations();
    
    // Add navbar scroll effect
    setupNavbarScroll();
    
    // Setup random quotes display
    setupQuotesDisplay();
    
    // Setup guest features if available
    setupGuestFeatures();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize Bootstrap popovers
function initializePopovers() {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Setup alert auto-dismissal with fade animation
function setupAlertDismissal() {
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            if (alert) {
                // Fade out gradually
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                
                // Remove after animation completes
                setTimeout(function() {
                    if (alert.parentNode) {
                        try {
                            var bsAlert = new bootstrap.Alert(alert);
                            bsAlert.close();
                        } catch (e) {
                            alert.parentNode.removeChild(alert);
                        }
                    }
                }, 500);
            }
        });
    }, 5000);
}

// Enhanced mood selection with visual feedback
function setupMoodSelection() {
    const moodOptions = document.querySelectorAll('.mood-option input[type="radio"]');
    if (moodOptions.length > 0) {
        moodOptions.forEach(function(radio) {
            radio.addEventListener('change', function() {
                // Add visual feedback when a mood is selected
                const selectedMood = this.value;
                console.log('Selected mood:', selectedMood);
                
                // Remove previous selection style
                document.querySelectorAll('.mood-label').forEach(function(label) {
                    label.classList.remove('selected-mood');
                });
                
                // Add selection style with animation
                const label = this.nextElementSibling;
                label.classList.add('selected-mood');
                
                // Add subtle bounce animation
                label.animate([
                    { transform: 'scale(1)' },
                    { transform: 'scale(1.05)' },
                    { transform: 'scale(1)' }
                ], {
                    duration: 400,
                    easing: 'ease-in-out'
                });
                
                // Update any associated mood description text
                const moodDescription = document.getElementById('mood-description');
                if (moodDescription) {
                    updateMoodDescription(selectedMood, moodDescription);
                }
            });
        });
    }
}

// Update mood description based on selection
function updateMoodDescription(mood, element) {
    const descriptions = {
        'happy': 'Feeling joyful and upbeat! We\'ll find some energetic tracks to match your mood.',
        'sad': 'Feeling blue? Music can help process those emotions and provide comfort.',
        'energetic': 'Bursting with energy! Let\'s channel that with some high-tempo tracks.',
        'calm': 'Seeking tranquility? We\'ll find some peaceful melodies for your relaxation.',
        'anxious': 'Music can help ease your mind when you\'re feeling anxious or stressed.',
        'angry': 'Let\'s release that frustration with some powerful tracks.',
        'romantic': 'In a loving mood? We\'ll find the perfect soundtrack for those feelings.',
        'focused': 'Need to concentrate? We\'ll recommend music to boost your productivity.',
        'relaxed': 'Enjoying some downtime? We\'ll enhance that relaxed state with perfect tunes.',
        'melancholic': 'Embrace the reflective, bittersweet feeling with our thoughtful selections.'
    };
    
    element.textContent = descriptions[mood] || 'Select your current mood and we\'ll recommend the perfect music.';
    
    // Fade in the description text
    element.animate([
        { opacity: 0 },
        { opacity: 1 }
    ], {
        duration: 500,
        easing: 'ease-in'
    });
}

// Audio player enhancements
function setupAudioPlayers() {
    const audioPlayers = document.querySelectorAll('audio');
    if (audioPlayers.length > 0) {
        audioPlayers.forEach(function(player) {
            // Create unique audio visualization if canvas is available
            const canvas = player.parentElement.querySelector('.audio-visualization');
            if (canvas) {
                setupAudioVisualization(player, canvas);
            }
            
            player.addEventListener('play', function() {
                // Pause all other audio players when one starts playing
                audioPlayers.forEach(function(otherPlayer) {
                    if (otherPlayer !== player && !otherPlayer.paused) {
                        otherPlayer.pause();
                    }
                });
                
                // Update UI to show currently playing track
                const trackItems = document.querySelectorAll('.track-item');
                trackItems.forEach(function(item) {
                    item.classList.remove('now-playing');
                });
                
                const parentTrack = player.closest('.track-item');
                if (parentTrack) {
                    parentTrack.classList.add('now-playing');
                }
            });
        });
    }
}

// Setup scroll animations for elements
function setupScrollAnimations() {
    // Only setup if IntersectionObserver is available
    if ('IntersectionObserver' in window) {
        const elementsToAnimate = document.querySelectorAll('.card, .track-item, .mood-option, .glass-card, .feature-mini-card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        elementsToAnimate.forEach(element => {
            observer.observe(element);
            element.classList.add('animate-on-scroll');
        });
    }
}

// Add navbar scroll effect
function setupNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
}

// Setup audio visualization if Web Audio API is available
function setupAudioVisualization(audioElement, canvas) {
    if (!window.AudioContext && !window.webkitAudioContext) return;
    
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const audioCtx = new AudioContext();
    const analyser = audioCtx.createAnalyser();
    const source = audioCtx.createMediaElementSource(audioElement);
    
    source.connect(analyser);
    analyser.connect(audioCtx.destination);
    
    analyser.fftSize = 256;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    function draw() {
        requestAnimationFrame(draw);
        
        analyser.getByteFrequencyData(dataArray);
        
        ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.fillRect(0, 0, width, height);
        
        const barWidth = (width / bufferLength) * 2.5;
        let barHeight;
        let x = 0;
        
        for (let i = 0; i < bufferLength; i++) {
            barHeight = dataArray[i] / 2;
            
            const gradient = ctx.createLinearGradient(0, 0, 0, height);
            gradient.addColorStop(0, '#6e8efb');
            gradient.addColorStop(1, '#a777e3');
            
            ctx.fillStyle = gradient;
            ctx.fillRect(x, height - barHeight, barWidth, barHeight);
            
            x += barWidth + 1;
        }
    }
    
    audioElement.addEventListener('play', function() {
        audioCtx.resume().then(() => {
            draw();
        });
    });
}

// Setup quotes display functionality
function setupQuotesDisplay() {
    // Create container for quotes if it doesn't exist
    let quoteContainer = document.querySelector('.quote-container');
    if (!quoteContainer) {
        quoteContainer = document.createElement('div');
        quoteContainer.classList.add('quote-container');
        document.body.appendChild(quoteContainer);
    }
    
    // Collection of happy quotes and jokes
    const quotes = [
        { text: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
        { text: "Happiness is not something ready-made. It comes from your own actions.", author: "Dalai Lama" },
        { text: "The most wasted of all days is one without laughter.", author: "E. E. Cummings" },
        { text: "Happiness is a warm puppy.", author: "Charles M. Schulz" },
        { text: "Don't worry, be happy!", author: "Bobby McFerrin" },
        { text: "Today is your day, your mountain is waiting. So get on your way!", author: "Dr. Seuss" },
        { text: "Why do we tell actors to 'break a leg?' Because every play has a cast.", author: "" },
        { text: "What's the best thing about Switzerland? I don't know, but the flag is a big plus.", author: "" },
        { text: "Why don't scientists trust atoms? Because they make up everything!", author: "" },
        { text: "What do you call a fake noodle? An impasta!", author: "" },
        { text: "Life is short. Smile while you still have teeth.", author: "" },
        { text: "Music washes away from the soul the dust of everyday life.", author: "Berthold Auerbach" },
        { text: "Where words fail, music speaks.", author: "Hans Christian Andersen" },
        { text: "Music gives a soul to the universe, wings to the mind, flight to the imagination, and life to everything.", author: "Plato" },
        { text: "One good thing about music, when it hits you, you feel no pain.", author: "Bob Marley" }
    ];

    // Display a new quote
    function displayRandomQuote() {
        const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
        
        const quoteBox = document.createElement('div');
        quoteBox.classList.add('quote-box', 'quote-enter');
        
        const quoteText = document.createElement('p');
        quoteText.classList.add('quote-text');
        quoteText.textContent = randomQuote.text;
        
        quoteBox.appendChild(quoteText);
        
        if (randomQuote.author) {
            const quoteAuthor = document.createElement('p');
            quoteAuthor.classList.add('quote-author');
            quoteAuthor.textContent = '- ' + randomQuote.author;
            quoteBox.appendChild(quoteAuthor);
        }
        
        quoteContainer.appendChild(quoteBox);
        
        // Remove the quote after 10 seconds
        setTimeout(() => {
            quoteBox.classList.add('quote-exit');
            setTimeout(() => {
                if (quoteBox.parentNode === quoteContainer) {
                    quoteContainer.removeChild(quoteBox);
                }
            }, 500);
        }, 10000);
    }
    
    // Display first quote immediately
    displayRandomQuote();
    
    // Then display a new quote every 15 seconds
    setInterval(displayRandomQuote, 15000);
}

// Setup guest features functionality
function setupGuestFeatures() {
    // Setup mini playlist player functionality
    const playButtons = document.querySelectorAll('.play-now-btn');
    if (playButtons.length > 0) {
        playButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const playlistId = this.getAttribute('data-playlist');
                
                // Here we would normally initialize a Spotify player
                // For demo purposes, just show an alert
                alert('Playing sample playlist: ' + playlistId);
            });
        });
    }
    
    // Setup mood test demo for guests
    const guestMoodTest = document.querySelector('#guest-mood-test');
    if (guestMoodTest) {
        guestMoodTest.addEventListener('click', function(e) {
            e.preventDefault();
            const moodResult = document.querySelector('#guest-mood-result');
            
            // Display loading animation
            moodResult.innerHTML = '<div class="loading mb-3"></div><p>Analyzing...</p>';
            
            // Simulate processing
            setTimeout(() => {
                const moods = ['happy', 'energetic', 'calm', 'focused'];
                const randomMood = moods[Math.floor(Math.random() * moods.length)];
                
                moodResult.innerHTML = '<div class="alert alert-info">' +
                    '<h5>Your current mood seems to be: <strong>' + randomMood + '</strong></h5>' +
                    '<p>Create an account to get personalized music recommendations!</p>' +
                    '<a href="/register" class="btn btn-primary btn-sm mt-2">Sign Up Now</a>' +
                    '</div>';
            }, 2000);
        });
    }
}