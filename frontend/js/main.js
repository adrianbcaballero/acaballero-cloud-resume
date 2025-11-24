/**
 * AEGLERO - Main JavaScript
 * View Counter Integration with Unique Visitor Tracking (GET + POST)
 */

// Global variable to hold the scroll position for the smart header logic
let lastScrollY = 0;
const header = document.querySelector(".main-header");

document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. VIEW COUNTER (UNIQUE VISITOR TRACKING WITH GET/POST) ---
    
    const API_ENDPOINT = 'https://r05eb4w5b0.execute-api.us-west-1.amazonaws.com/dev/proxy';
    
    // Configuration for visit tracking
    const VISIT_KEY = 'aeglero_has_visited';
    
    // Check if user has EVER visited before
    const hasVisitedBefore = localStorage.getItem(VISIT_KEY);
    
    // Determine if we should count this visit
    let shouldCount = false;
    
    if (!hasVisitedBefore) {
        // First time visitor EVER - count them
        shouldCount = true;
        console.log('First time visitor - incrementing counter');
    } else {
        // This user has visited before - don't count
        shouldCount = false;
        console.log('Returning visitor - not counting (already counted)');
    }
    
    if (shouldCount) {
        // --- POST: Increment the counter ---
        fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to increment counter');
            }
            return response.json(); 
        })
        .then(data => {
            const parsedBody = JSON.parse(data.body); 
            const newValue = parsedBody.value; 
            
            // Update the view count display
            document.getElementById('viewCount').innerText = `Eyes reached: ${newValue}`;
            
            // Mark this user as having visited (forever)
            localStorage.setItem(VISIT_KEY, 'true');
            
            console.log('View counter incremented to:', newValue);
        })
        .catch(error => {
            console.error('Error incrementing view count:', error);
            document.getElementById('viewCount').innerText = 'Eyes Reached: --';
        });
        
    } else {
        // --- GET: Fetch current count WITHOUT incrementing ---
        fetch(API_ENDPOINT, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch current count');
            }
            return response.json();
        })
        .then(data => {
            const parsedBody = JSON.parse(data.body);
            const currentValue = parsedBody.value;
            
            // Display the current count (without incrementing)
            document.getElementById('viewCount').innerText = `Eyes reached: ${currentValue}`;
            
            console.log('Current count (not incremented):', currentValue);
        })
        .catch(error => {
            console.error('Error fetching current count:', error);
            // Fallback: show a friendly message
            document.getElementById('viewCount').innerText = 'Eyes Reached: Welcome back!';
        });
    }

    // --- 2. SMOOTH SCROLL FOR NAVIGATION LINKS ---
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// --- 3. SMART HEADER (HIDE ON SCROLL DOWN) ---

window.addEventListener('scroll', function() {
    const currentScrollY = window.scrollY;

    // Smart Header Logic
    if (header) {
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            // Scrolling down - hide header
            header.classList.add("header-hidden");
        } 
        else if (currentScrollY < lastScrollY || currentScrollY < 100) {
            // Scrolling up or at top - show header
            header.classList.remove("header-hidden");
        }
    }

    lastScrollY = currentScrollY;
});