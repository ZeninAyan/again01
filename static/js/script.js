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
    
    // Show welcome message
    showWelcomeMessage();
    
    // Setup random quotes display
    setupQuotesDisplay();
    
    // Setup guest features if available
    setupGuestFeatures();
    
    // Setup interactive jokes if available
    setupInteractiveJokes();
    
    // Setup music trivia if on homepage
    setupMusicTrivia();
    
    // Setup quick mood test on homepage for everyone
    setupQuickMoodTest();
});

// Show welcome message on first load
function showWelcomeMessage() {
    const welcomeContainer = document.createElement('div');
    welcomeContainer.classList.add('welcome-popup');
    welcomeContainer.innerHTML = '<h3>HOW U DOINN BRUH?</h3>';
    document.body.appendChild(welcomeContainer);
    
    // Show message for 1 second then fade out with growing animation (changed from 2 sec)
    setTimeout(() => {
        welcomeContainer.classList.add('fadeout');
        setTimeout(() => {
            if (welcomeContainer.parentNode === document.body) {
                document.body.removeChild(welcomeContainer);
            }
        }, 800);
    }, 1000); // Changed from 2000 to 1000 ms
}

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
        
        // Remove the quote after 4 seconds
        setTimeout(() => {
            quoteBox.classList.add('quote-exit');
            setTimeout(() => {
                if (quoteBox.parentNode === quoteContainer) {
                    quoteContainer.removeChild(quoteBox);
                }
            }, 500);
        }, 4000);
    }
    
    // Display first quote immediately
    displayRandomQuote();
    
    // Then display a new quote every 10 seconds exactly
    setInterval(displayRandomQuote, 10000);
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
    
    // Setup mood test demo for guests - make it available for everyone
    setupGuestMoodTest();
}

// Setup a separate mood test function that can be used by both guests and registered users
function setupGuestMoodTest() {
    const guestMoodTest = document.querySelector('#guest-mood-test');
    if (guestMoodTest) {
        guestMoodTest.addEventListener('click', function(e) {
            e.preventDefault();
            const moodResult = document.querySelector('#guest-mood-result');
            
            // Display loading animation
            moodResult.innerHTML = '<div class="loading mb-3"></div><p class="text-center">Analyzing...</p>';
            
            // Simulate processing
            setTimeout(() => {
                const moods = ['happy', 'energetic', 'calm', 'focused'];
                const randomMood = moods[Math.floor(Math.random() * moods.length)];
                
                moodResult.innerHTML = '<div class="alert alert-info">' +
                    '<h5>Your current mood seems to be: <strong>' + randomMood + '</strong></h5>' +
                    '<p>Create an account to get personalized music recommendations and track your mood history!</p>' +
                    '<a href="/register" class="btn btn-primary btn-sm mt-2">Sign Up Now</a>' +
                    '<button class="btn btn-success btn-sm mt-2 ms-2" id="try-another-mood">Try Again</button>' +
                    '</div>';
                
                // Add event listener for the try again button
                const tryAgainBtn = document.getElementById('try-another-mood');
                if (tryAgainBtn) {
                    tryAgainBtn.addEventListener('click', function() {
                        setupGuestMoodTest();
                        // Trigger the click event
                        guestMoodTest.click();
                    });
                }
            }, 2000);
        });
    }
}

// Setup interactive jokes feature
function setupInteractiveJokes() {
    const jokeContainer = document.getElementById('interactive-jokes');
    if (!jokeContainer) return;
    
    // Expanded joke collection with more variety including dank jokes
    const jokes = [
        // Classic jokes
        { 
            question: "Why did the scarecrow win an award?", 
            answer: "Because he was outstanding in his field!"
        },
        { 
            question: "Why don't scientists trust atoms?", 
            answer: "Because they make up everything!"
        },
        { 
            question: "What's the best thing about Switzerland?", 
            answer: "I don't know, but the flag is a big plus!"
        },
        { 
            question: "How does a penguin build its house?", 
            answer: "Igloos it together!"
        },
        { 
            question: "Why couldn't the bicycle stand up by itself?", 
            answer: "It was two tired!"
        },
        // Music-related jokes
        {
            question: "What do you call a musician with problems?",
            answer: "A trebled person!"
        },
        {
            question: "How do you make a band stand?",
            answer: "Take away their chairs!"
        },
        {
            question: "What's an astronaut's favorite key on the piano?",
            answer: "The space bar!"
        },
        // Internet/Dank jokes
        {
            question: "Why don't programmers like nature?",
            answer: "It has too many bugs!"
        },
        {
            question: "What did the router say to the doctor?",
            answer: "It hurts when IP!"
        },
        {
            question: "Why do Java developers wear glasses?",
            answer: "Because they don't C#!"
        },
        {
            question: "What did the ocean say to the beach?",
            answer: "Nothing, it just waved!"
        },
        {
            question: "What do you call it when your crush doesn't text back?",
            answer: "Depression!"
        },
        {
            question: "Why did the FBI agent go to an art exhibition?",
            answer: "He was searching for sketchy characters!"
        },
        {
            question: "How did the hipster burn his tongue?",
            answer: "He drank his coffee before it was cool!"
        },
        {
            question: "What's the difference between a poorly dressed man on a trampoline and a well-dressed man on a trampoline?",
            answer: "Attire!"
        },
        {
            question: "What do you call a fish with no eyes?",
            answer: "Fsh!"
        },
        {
            question: "What happens when you eat too many spaghetti?",
            answer: "You pasta way!"
        },
        {
            question: "Two guys walk into a bar. The third one ducks.",
            answer: "Ba dum tss!"
        },
        {
            question: "Why don't skeletons fight each other?",
            answer: "They don't have the guts!"
        },
        {
            question: "Did you hear about the guy who invented knock-knock jokes?",
            answer: "He won the 'no-bell' prize!"
        }
    ];
    
    // Smart responses based on user input
    const smartResponses = {
        "i don't know": "Okay, I'll tell you!",
        "dont know": "Let me enlighten you!",
        "no idea": "Time to learn something fun!",
        "tell me": "Here's the answer:",
        "i give up": "Don't worry, here's the answer:",
        "idk": "Allow me to share the answer:",
        "what": "I know, right? Here's the answer:",
        "why": "Good question! Here's why:",
        "how": "I'll explain how:",
        "default": "Nahh buddy, you are wrong!"
    };
    
    // Name jokes with weird reasoning
    const nameJokes = [
        name => `${name}? That's interesting! Did you know people named ${name} have a statistically higher chance of becoming professional bubble wrap poppers?`,
        name => `Ah, ${name}! In ancient folklore, it was believed that people named ${name} could communicate telepathically with houseplants.`,
        name => `${name}? According to a study I just made up, people named ${name} are 73% more likely to accidentally put their phone in the refrigerator.`,
        name => `Fun fact: The name ${name} originated from an ancient tribe of people who believed that sneezing was a form of time travel.`,
        name => `${name}? That's interesting! Studies show people with your name have an uncanny ability to find lost socks in parallel dimensions.`,
        name => `Did you know that ${name} is considered the most musical name in at least three made-up countries?`,
        name => `${name}? Legend has it that people with this name can taste the color blue and hear the sound of silence.`,
        name => `The name ${name} actually translates to "one who dances with imaginary squirrels" in a language I just invented.`
    ];
    
    let currentJoke = null;
    let askedName = false;
    
    // Initialize joke interface
    function initJokeInterface() {
        jokeContainer.innerHTML = `
            <div class="card shadow-sm">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h3 class="h4 mb-0">Interactive Jokes</h3>
                    <button type="button" id="new-joke-btn" class="btn btn-sm glossy-button">New Joke</button>
                </div>
                <div class="card-body">
                    <div id="joke-content">
                        <p class="text-center">Click "New Joke" to start!</p>
                    </div>
                    <div id="joke-response" class="mt-3 d-none">
                        <input type="text" id="joke-answer-input" class="form-control mb-2" placeholder="Type your answer...">
                        <div class="d-grid">
                            <button type="button" id="submit-answer-btn" class="btn btn-primary">Submit Answer</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Setup event listeners
        document.getElementById('new-joke-btn').addEventListener('click', startNewJoke);
        document.getElementById('submit-answer-btn').addEventListener('click', submitAnswer);
        
        // Also allow submitting with enter key
        document.getElementById('joke-answer-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                submitAnswer();
            }
        });
    }
    
    // Start a new joke or name prompt
    function startNewJoke() {
        const jokeContent = document.getElementById('joke-content');
        const jokeResponse = document.getElementById('joke-response');
        const answerInput = document.getElementById('joke-answer-input');
        
        // Toggle between name jokes and regular jokes
        if (!askedName && Math.random() > 0.5) {
            askedName = true;
            jokeContent.innerHTML = '<p class="mb-3">What\'s your name?</p>';
            answerInput.placeholder = "Type your name...";
            jokeResponse.classList.remove('d-none');
            currentJoke = { type: 'name' };
        } else {
            // Regular joke
            askedName = false;
            currentJoke = jokes[Math.floor(Math.random() * jokes.length)];
            currentJoke.type = 'regular';
            jokeContent.innerHTML = `<p class="mb-3">${currentJoke.question}</p>`;
            answerInput.placeholder = "Type your answer...";
            jokeResponse.classList.remove('d-none');
        }
        
        // Clear previous answer
        answerInput.value = '';
        answerInput.focus();
    }
    
    // Get smart response based on user's answer
    function getSmartResponse(userAnswer) {
        const lowerAnswer = userAnswer.toLowerCase().trim();
        
        // Check for common phrases
        for (const [phrase, response] of Object.entries(smartResponses)) {
            if (lowerAnswer.includes(phrase)) {
                return response;
            }
        }
        
        // Check if answer contains joke-specific keywords
        if (currentJoke && currentJoke.type === 'regular') {
            const keywords = currentJoke.answer.toLowerCase().split(' ');
            for (const keyword of keywords) {
                // Skip short or common words
                if (keyword.length < 4 || ['the', 'and', 'but', 'for', 'was', 'with'].includes(keyword)) continue;
                
                if (lowerAnswer.includes(keyword)) {
                    return "You're on the right track!";
                }
            }
        }
        
        // Default response
        return smartResponses.default;
    }
    
    // Submit joke answer
    function submitAnswer() {
        if (!currentJoke) return;
        
        const jokeContent = document.getElementById('joke-content');
        const jokeResponse = document.getElementById('joke-response');
        const answerInput = document.getElementById('joke-answer-input');
        const userAnswer = answerInput.value.trim();
        
        if (userAnswer === '') return;
        
        if (currentJoke.type === 'name') {
            // Process name joke
            const nameJoke = nameJokes[Math.floor(Math.random() * nameJokes.length)];
            const jokeText = nameJoke(userAnswer);
            
            jokeContent.innerHTML = `
                <div class="alert alert-info">
                    <p class="mb-1"><strong>${userAnswer}</strong>, nice to meet you!</p>
                    <p class="mb-0">${jokeText}</p>
                </div>
            `;
        } else {
            // Process regular joke with smart response
            const smartResponse = getSmartResponse(userAnswer);
            
            jokeContent.innerHTML = `
                <div>
                    <p class="mb-1"><strong>Your answer:</strong> ${userAnswer}</p>
                    <div class="alert alert-warning mb-2">
                        <p class="mb-0">${smartResponse}</p>
                    </div>
                    <div class="alert alert-info">
                        <p class="mb-1"><strong>The question:</strong> ${currentJoke.question}</p>
                        <p class="mb-0"><strong>Actual answer:</strong> ${currentJoke.answer}</p>
                    </div>
                </div>
            `;
        }
        
        // Hide the response area
        jokeResponse.classList.add('d-none');
    }
    
    // Initialize the joke interface
    initJokeInterface();
}

// Setup music trivia feature
function setupMusicTrivia() {
    // Only run on homepage
    if (!document.querySelector('.hero-section')) return;
    
    const triviaContainer = document.createElement('div');
    triviaContainer.classList.add('row', 'mt-4', 'py-4');
    triviaContainer.innerHTML = `
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h3 class="h4 mb-0">Music Trivia</h3>
                    <button type="button" id="new-trivia-btn" class="btn btn-sm glossy-button">New Trivia</button>
                </div>
                <div class="card-body">
                    <div id="trivia-content">
                        <p class="text-center">Click "New Trivia" to test your music knowledge!</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add trivia section before the features section
    const featuresSection = document.querySelector('.features-section');
    if (featuresSection) {
        featuresSection.parentNode.insertBefore(triviaContainer, featuresSection);
    }
    
    // Trivia questions and answers
    const triviaQuestions = [
        { 
            question: "Which band released the album 'Dark Side of the Moon'?",
            answer: "Pink Floyd",
            options: ["Led Zeppelin", "Pink Floyd", "The Beatles", "The Rolling Stones"]
        },
        {
            question: "Who was known as the 'King of Pop'?",
            answer: "Michael Jackson",
            options: ["Elvis Presley", "Michael Jackson", "Prince", "Freddie Mercury"]
        },
        {
            question: "Which instrument has 88 keys?",
            answer: "Piano",
            options: ["Organ", "Synthesizer", "Piano", "Harpsichord"]
        },
        {
            question: "Who wrote the composition 'Für Elise'?",
            answer: "Beethoven",
            options: ["Mozart", "Bach", "Chopin", "Beethoven"]
        },
        {
            question: "What music genre originated in Jamaica in the late 1960s?",
            answer: "Reggae",
            options: ["Reggae", "Hip Hop", "Jazz", "Blues"]
        },
        {
            question: "Which female artist released the album 'Lemonade' in 2016?",
            answer: "Beyoncé",
            options: ["Rihanna", "Adele", "Beyoncé", "Taylor Swift"]
        },
        {
            question: "Which music technology replaced cassettes in the 1990s?",
            answer: "Compact Disc (CD)",
            options: ["MP3 Player", "Vinyl Record", "8-Track", "Compact Disc (CD)"]
        }
    ];
    
    // Setup event listeners
    setTimeout(() => {
        const newTriviaBtn = document.getElementById('new-trivia-btn');
        if (newTriviaBtn) {
            newTriviaBtn.addEventListener('click', () => {
                showRandomTrivia();
            });
        }
    }, 500);
    
    // Show random trivia question
    function showRandomTrivia() {
        const triviaContent = document.getElementById('trivia-content');
        if (!triviaContent) return;
        
        const randomTrivia = triviaQuestions[Math.floor(Math.random() * triviaQuestions.length)];
        
        let optionsHTML = '';
        randomTrivia.options.forEach((option, index) => {
            optionsHTML += `
                <div class="form-check mb-2">
                    <input class="form-check-input" type="radio" name="triviaOption" id="option${index}" value="${option}">
                    <label class="form-check-label" for="option${index}">
                        ${option}
                    </label>
                </div>
            `;
        });
        
        triviaContent.innerHTML = `
            <div class="mb-3">
                <p class="fw-bold">${randomTrivia.question}</p>
                <div class="mt-3">
                    ${optionsHTML}
                </div>
                <button type="button" id="check-answer-btn" class="btn btn-primary mt-3">Check Answer</button>
            </div>
        `;
        
        // Add event listener to check answer button
        const checkAnswerBtn = document.getElementById('check-answer-btn');
        if (checkAnswerBtn) {
            checkAnswerBtn.addEventListener('click', () => {
                const selectedOption = document.querySelector('input[name="triviaOption"]:checked');
                
                if (!selectedOption) {
                    alert('Please select an answer.');
                    return;
                }
                
                const userAnswer = selectedOption.value;
                const isCorrect = userAnswer === randomTrivia.answer;
                
                triviaContent.innerHTML = `
                    <div class="alert ${isCorrect ? 'alert-success' : 'alert-danger'}">
                        <p class="mb-1"><strong>${isCorrect ? 'Correct!' : 'Sorry, that\'s incorrect!'}</strong></p>
                        <p class="mb-0">The answer is: ${randomTrivia.answer}</p>
                    </div>
                    <button type="button" id="next-trivia-btn" class="btn glossy-button btn-sm mt-2">Next Question</button>
                `;
                
                const nextTriviaBtn = document.getElementById('next-trivia-btn');
                if (nextTriviaBtn) {
                    nextTriviaBtn.addEventListener('click', showRandomTrivia);
                }
            });
        }
    }
}

// Setup quick mood test on the homepage
function setupQuickMoodTest() {
    // Only run on homepage
    if (!document.querySelector('.hero-section')) return;
    
    // Don't add to the page if the user is already logged in
    if (document.querySelector('.hero-section') && !document.querySelector('a[href="/register"]')) return;
    
    // Updated to use situational questions
    const moodTestContainer = document.createElement('div');
    moodTestContainer.classList.add('row', 'mt-4', 'py-4', 'bg-light', 'rounded-5');
    moodTestContainer.innerHTML = `
        <div class="col-12 text-center mb-4">
            <h2 class="gradient-text mb-3">Quick Mood Test</h2>
            <p class="lead text-muted">Find out your current mood through situational questions</p>
        </div>
        
        <div class="col-md-8 offset-md-2">
            <div class="glass-card p-4">
                <div id="mood-question-container">
                    <h5 class="mb-4 text-center" id="mood-question">Ready to find out your mood?</h5>
                    <div class="d-grid gap-2">
                        <button id="start-mood-test" class="btn glossy-button mb-3">Start Mood Test</button>
                    </div>
                </div>
                <div id="quick-mood-result" class="mt-4"></div>
            </div>
        </div>
    `;
    
    // Add mood test container before the interactive jokes section
    const jokesSection = document.getElementById('interactive-jokes');
    if (jokesSection && jokesSection.parentNode && jokesSection.parentNode.parentNode) {
        const jokesRow = jokesSection.parentNode.parentNode;
        jokesRow.parentNode.insertBefore(moodTestContainer, jokesRow);
    }
    
    // Situational questions to analyze mood
    const moodQuestions = [
        {
            question: "You're stuck in traffic and running late for an important meeting. How do you react?",
            options: [
                { text: "Anxiously check the time every few seconds", mood: "anxious" },
                { text: "Stay calm and call ahead to let them know", mood: "calm" },
                { text: "Get frustrated and honk at other drivers", mood: "angry" },
                { text: "Use the time to listen to your favorite music", mood: "happy" }
            ]
        },
        {
            question: "Your friend cancels plans at the last minute. What's your response?",
            options: [
                { text: "Feel disappointed but understand things happen", mood: "calm" },
                { text: "Get upset and tell them how inconsiderate they are", mood: "angry" },
                { text: "Feel relieved as you wanted to stay home anyway", mood: "happy" },
                { text: "Worry that they might be avoiding you", mood: "anxious" }
            ]
        },
        {
            question: "You receive unexpected good news. How do you celebrate?",
            options: [
                { text: "Jump around and share it with everyone", mood: "energetic" },
                { text: "Smile to yourself and feel content", mood: "happy" },
                { text: "Worry about what could go wrong", mood: "anxious" },
                { text: "Plan a small celebration with close friends", mood: "calm" }
            ]
        },
        {
            question: "It's a rainy Sunday afternoon. What do you do?",
            options: [
                { text: "Feel gloomy and just stare out the window", mood: "sad" },
                { text: "Get productive and organize your space", mood: "energetic" },
                { text: "Curl up with a book and enjoy the peaceful sound", mood: "calm" },
                { text: "Feel restless because outdoor plans are ruined", mood: "anxious" }
            ]
        },
        {
            question: "Someone cuts in line in front of you. Your reaction is to:",
            options: [
                { text: "Confront them directly about their behavior", mood: "angry" },
                { text: "Say nothing but feel annoyed inside", mood: "anxious" },
                { text: "Politely point out that there's a line", mood: "calm" },
                { text: "Shrug it off – not worth the energy", mood: "happy" }
            ]
        }
    ];
    
    // Setup event listeners after a short delay
    setTimeout(() => {
        const startButton = document.getElementById('start-mood-test');
        if (startButton) {
            startButton.addEventListener('click', () => startMoodTest());
        }
    }, 500);
    
    let currentQuestionIndex = 0;
    const userResponses = [];
    
    // Start the mood test
    function startMoodTest() {
        currentQuestionIndex = 0;
        userResponses.length = 0;
        showNextQuestion();
    }
    
    // Show the next question
    function showNextQuestion() {
        const questionContainer = document.getElementById('mood-question-container');
        const resultContainer = document.getElementById('quick-mood-result');
        resultContainer.innerHTML = '';
        
        if (currentQuestionIndex < moodQuestions.length) {
            const question = moodQuestions[currentQuestionIndex];
            
            let optionsHTML = '';
            question.options.forEach((option, index) => {
                optionsHTML += `
                    <button class="btn btn-outline-primary mb-2 w-100 text-start mood-option-btn" 
                            data-mood="${option.mood}" data-index="${index}">
                        ${option.text}
                    </button>
                `;
            });
            
            questionContainer.innerHTML = `
                <div class="progress mb-4">
                    <div class="progress-bar" role="progressbar" style="width: ${(currentQuestionIndex / moodQuestions.length) * 100}%"></div>
                </div>
                <h5 class="mb-4">${question.question}</h5>
                <div class="d-grid gap-2 mb-3">
                    ${optionsHTML}
                </div>
                <p class="text-muted small text-center">Question ${currentQuestionIndex + 1} of ${moodQuestions.length}</p>
            `;
            
            // Add event listeners to option buttons
            document.querySelectorAll('.mood-option-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const selectedMood = this.getAttribute('data-mood');
                    const selectedIndex = this.getAttribute('data-index');
                    userResponses.push({
                        question: currentQuestionIndex,
                        mood: selectedMood,
                        option: parseInt(selectedIndex)
                    });
                    
                    currentQuestionIndex++;
                    if (currentQuestionIndex < moodQuestions.length) {
                        showNextQuestion();
                    } else {
                        analyzeMoodResults();
                    }
                });
            });
        }
    }
    
    // Analyze mood test results
    function analyzeMoodResults() {
        const moodCounts = {};
        userResponses.forEach(response => {
            if (!moodCounts[response.mood]) {
                moodCounts[response.mood] = 0;
            }
            moodCounts[response.mood]++;
        });
        
        // Find the dominant mood
        let dominantMood = 'calm'; // Default
        let maxCount = 0;
        
        for (const mood in moodCounts) {
            if (moodCounts[mood] > maxCount) {
                maxCount = moodCounts[mood];
                dominantMood = mood;
            }
        }
        
        showMoodResults(dominantMood);
    }
    
    // Show mood results
    function showMoodResults(mood) {
        const questionContainer = document.getElementById('mood-question-container');
        const resultContainer = document.getElementById('quick-mood-result');
        
        // Define mood descriptions
        const moodDescriptions = {
            'happy': {
                icon: 'smile',
                color: 'primary',
                description: 'You\'re feeling joyful and upbeat! We recommend energetic, uplifting music to match your positive vibe.',
                sample: ['\"Happy\" by Pharrell Williams', '\"Good Feeling\" by Flo Rida', '\"Uptown Funk\" by Mark Ronson ft. Bruno Mars']
            },
            'sad': {
                icon: 'frown',
                color: 'secondary',
                description: 'You\'re feeling a bit down. Music can help process emotions - try some reflective tracks or gentle uplifting melodies.',
                sample: ['\"Someone Like You\" by Adele', '\"Fix You\" by Coldplay', '\"Everybody Hurts\" by R.E.M.']
            },
            'energetic': {
                icon: 'bolt',
                color: 'success',
                description: 'You\'re full of energy! Fast-paced, dynamic tracks will help channel that excitement.',
                sample: ['\"Can\'t Hold Us\" by Macklemore', '\"Blinding Lights\" by The Weeknd', '\"Physical\" by Dua Lipa']
            },
            'calm': {
                icon: 'wind',
                color: 'info',
                description: 'You\'re in a tranquil state of mind. Peaceful, ambient music will complement your relaxed mood.',
                sample: ['\"Weightless\" by Marconi Union', '\"Claire de Lune\" by Debussy', '\"Gymnopédie No.1\" by Erik Satie']
            },
            'anxious': {
                icon: 'hourglass-half',
                color: 'warning',
                description: 'You\'re feeling a bit on edge. Music with steady rhythms can help ground you and ease anxiety.',
                sample: ['\"Breathe Me\" by Sia', '\"Weightless\" by Marconi Union', '\"Everything\'s Not Lost\" by Coldplay']
            },
            'angry': {
                icon: 'fire',
                color: 'danger',
                description: 'You\'re feeling heated! Cathartic music can help process these emotions in a healthy way.',
                sample: ['\"Break Stuff\" by Limp Bizkit', '\"Killing In The Name\" by Rage Against The Machine', '\"Given Up\" by Linkin Park']
            }
        };
        
        const moodInfo = moodDescriptions[mood] || moodDescriptions.calm;
        
        questionContainer.innerHTML = `
            <h4 class="text-center mb-4">Mood Analysis Complete!</h4>
        `;
        
        resultContainer.innerHTML = `
            <div class="alert alert-${moodInfo.color} mb-4">
                <div class="d-flex align-items-center">
                    <div class="display-4 me-3">
                        <i class="fas fa-${moodInfo.icon}"></i>
                    </div>
                    <div>
                        <h5 class="mb-1">Your dominant mood: <strong>${mood}</strong></h5>
                        <p class="mb-0">${moodInfo.description}</p>
                    </div>
                </div>
            </div>
            
            <h5 class="mb-3">Recommended tracks for you:</h5>
            <ul class="list-group mb-3">
                ${moodInfo.sample.map(track => `<li class="list-group-item"><i class="fas fa-music me-2"></i>${track}</li>`).join('')}
            </ul>
            
            <div class="d-flex justify-content-between align-items-center mt-4">
                <button id="retake-mood-test" class="btn btn-outline-primary">Try Again</button>
                <div>
                    <a href="/register" class="btn btn-primary">Sign up for personalized playlists</a>
                </div>
            </div>
        `;
        
        // Add event listener for retake button
        const retakeButton = document.getElementById('retake-mood-test');
        if (retakeButton) {
            retakeButton.addEventListener('click', startMoodTest);
        }
    }
}