/**
 * AEGLERO - Main JavaScript
 * View Counter Integration with Unique Visitor Tracking (GET + POST)
 */

// Global variable to hold the scroll position for the smart header logic
let lastScrollY = 0;
const header = document.querySelector(".main-header");

// --- LOAD COMMON HEAD TEMPLATE ---
async function loadHeadTemplate() {
    try {
        const response = await fetch('includes/head-template.html');
        if (!response.ok) {
            throw new Error('Failed to load head template');
        }
        const html = await response.text();
        
        // Create temporary container to parse the HTML
        const temp = document.createElement('div');
        temp.innerHTML = html;
        
        // Get all elements from the template
        const elements = temp.querySelectorAll('meta, link, script');
        
        // Insert each element into the document head
        elements.forEach(element => {
            // For meta tags, check if one with the same name/property already exists
            if (element.tagName === 'META') {
                const name = element.getAttribute('name') || element.getAttribute('property');
                if (name) {
                    const existing = document.querySelector(`meta[name="${name}"], meta[property="${name}"]`);
                    // Only add if it doesn't exist (page-specific meta tags take priority)
                    if (!existing) {
                        document.head.appendChild(element.cloneNode(true));
                    }
                } else {
                    // Meta tag without name/property (like charset) - add if not exists
                    const charset = element.getAttribute('charset');
                    if (charset && !document.querySelector('meta[charset]')) {
                        document.head.appendChild(element.cloneNode(true));
                    }
                }
            } else {
                // For link and script tags, always append (they can have duplicates or load order matters)
                document.head.appendChild(element.cloneNode(true));
            }
        });
        
        console.log('Common head template loaded successfully');
    } catch (error) {
        console.error('Error loading head template:', error);
        // Fail silently - page will still work without common head elements
    }
}

// Load head template immediately
loadHeadTemplate();

document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. VIEW COUNTER (UNIQUE VISITOR TRACKING WITH GET/POST) ---
    
    const API_ENDPOINT = 'https://2whekina0g.execute-api.us-west-1.amazonaws.com/dev/proxy';
    
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

// Hamburger Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburgerMenu');
    const mainNav = document.querySelector('.main-nav');
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    if (hamburger) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            mainNav.classList.toggle('mobile-active');
        });
    }

    // Handle dropdown clicks on mobile
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            if (window.innerWidth <= 900) {
                e.preventDefault();
                const parent = this.parentElement;
                parent.classList.toggle('mobile-dropdown-active');
            }
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 900) {
            if (!e.target.closest('.main-header')) {
                hamburger.classList.remove('active');
                mainNav.classList.remove('mobile-active');
            }
        }
    });
});


// Tech Repair Services - ZIP code checker
if (document.getElementById('zipCode')) {
    const validZipCodes = new Set([
        '90001', '90002', '90003', '90011', '90022', '90023', '90040', '90044', 
        '90052', '90058', '90059', '90061', '90063', '90201', '90220', '90221', 
        '90222', '90240', '90241', '90242', '90247', '90248', '90249', '90255', 
        '90262', '90270', '90280', '90601', '90602', '90603', '90604', '90605', 
        '90606', '90620', '90621', '90623', '90630', '90638', '90639', '90640', 
        '90650', '90660', '90670', '90701', '90703', '90706', '90712', '90713', 
        '90715', '90716', '90720', '90723', '90745', '90746', '90747', '90755', 
        '90804', '90805', '90806', '90807', '90808', '90810', '90813', '90814', 
        '90815', '90822', '90840', '91754'
    ]);

    window.checkServiceRange = function() {
        const zipInput = document.getElementById('zipCode');
        const resultDiv = document.getElementById('rangeResult');
        const zipCode = zipInput.value.trim();
        
        if (zipCode.length !== 5 || isNaN(zipCode)) {
            resultDiv.innerHTML = '<span style="color: #bf0000;">Please enter a valid 5-digit ZIP code.</span>';
            return;
        }
        
        if (validZipCodes.has(zipCode)) {
            resultDiv.innerHTML = `
                <span style="color: #28a745;">
                    ✓ Great news! You're within our 10-mile service area. Mobile service is available for phone repairs!
                </span>
            `;
        } else {
            resultDiv.innerHTML = `
                <span style="color: #bf0000;">
                    Your ZIP code is outside our 10-mile mobile service range. 
                    However, you can still bring your device to us or we can arrange a drop-off/pick-up!
                </span>
            `;
        }
    };
    
    document.getElementById('zipCode').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            checkServiceRange();
        }
    });
}