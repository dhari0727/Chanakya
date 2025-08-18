// Main JavaScript functionality for Google Search Clone

document.addEventListener('DOMContentLoaded', function() {
    initializeSearchSuggestions();
    initializeSearchForms();
});

// Initialize search suggestions functionality
function initializeSearchSuggestions() {
    const searchInputs = document.querySelectorAll('#search-input, #search-input-header');
    
    searchInputs.forEach(input => {
        const dropdownId = input.id === 'search-input' ? 'suggestions-dropdown' : 'suggestions-dropdown-header';
        const listId = input.id === 'search-input' ? 'suggestions-list' : 'suggestions-list-header';
        
        const dropdown = document.getElementById(dropdownId);
        const suggestionsList = document.getElementById(listId);
        
        if (!dropdown || !suggestionsList) return;
        
        let currentSuggestionIndex = -1;
        let suggestions = [];
        
        // Handle input events
        input.addEventListener('input', function() {
            const query = this.value.trim();
            
            if (query.length > 0) {
                fetchSuggestions(query).then(data => {
                    suggestions = data;
                    displaySuggestions(data, suggestionsList, dropdown);
                });
            } else {
                hideSuggestions(dropdown);
            }
        });
        
        // Handle keyboard navigation
        input.addEventListener('keydown', function(e) {
            if (!dropdown.classList.contains('show')) return;
            
            switch(e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    currentSuggestionIndex = Math.min(currentSuggestionIndex + 1, suggestions.length - 1);
                    highlightSuggestion(suggestionsList, currentSuggestionIndex);
                    break;
                    
                case 'ArrowUp':
                    e.preventDefault();
                    currentSuggestionIndex = Math.max(currentSuggestionIndex - 1, -1);
                    highlightSuggestion(suggestionsList, currentSuggestionIndex);
                    break;
                    
                case 'Enter':
                    if (currentSuggestionIndex >= 0) {
                        e.preventDefault();
                        this.value = suggestions[currentSuggestionIndex];
                        hideSuggestions(dropdown);
                        this.form.submit();
                    }
                    break;
                    
                case 'Escape':
                    hideSuggestions(dropdown);
                    currentSuggestionIndex = -1;
                    break;
            }
        });
        
        // Handle focus events
        input.addEventListener('focus', function() {
            if (suggestions.length > 0) {
                dropdown.classList.add('show');
            }
        });
        
        // Handle clicks outside
        document.addEventListener('click', function(e) {
            if (!input.contains(e.target) && !dropdown.contains(e.target)) {
                hideSuggestions(dropdown);
                currentSuggestionIndex = -1;
            }
        });
    });
}

// Fetch search suggestions from API
async function fetchSuggestions(query) {
    try {
        const response = await fetch(`/api/suggestions?q=${encodeURIComponent(query)}`);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.error('Error fetching suggestions:', error);
    }
    return [];
}

// Display suggestions in dropdown
function displaySuggestions(suggestions, list, dropdown) {
    list.innerHTML = '';
    
    if (suggestions.length === 0) {
        hideSuggestions(dropdown);
        return;
    }
    
    suggestions.forEach((suggestion, index) => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        li.addEventListener('click', function() {
            const input = dropdown.previousElementSibling.querySelector('input');
            input.value = suggestion;
            hideSuggestions(dropdown);
            input.form.submit();
        });
        list.appendChild(li);
    });
    
    dropdown.classList.add('show');
}

// Hide suggestions dropdown
function hideSuggestions(dropdown) {
    dropdown.classList.remove('show');
}

// Highlight suggestion for keyboard navigation
function highlightSuggestion(list, index) {
    const items = list.querySelectorAll('li');
    
    items.forEach((item, i) => {
        if (i === index) {
            item.style.backgroundColor = '#e8f0fe';
        } else {
            item.style.backgroundColor = '';
        }
    });
}

// Initialize search form functionality
function initializeSearchForms() {
    const searchForms = document.querySelectorAll('.search-form, .search-form-header');
    
    searchForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const input = form.querySelector('input[name="q"]');
            if (!input.value.trim()) {
                e.preventDefault();
                input.focus();
            }
        });
    });
}

// Voice search simulation (placeholder)
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('mic-icon') || e.target.classList.contains('mic-icon-header')) {
        alert('Voice search is not implemented in this demo');
    }
});

// Camera search simulation (placeholder)
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('camera-icon') || e.target.classList.contains('camera-icon-header')) {
        alert('Image search is not implemented in this demo');
    }
});

// Add loading state for search
function showLoadingState() {
    const searchButtons = document.querySelectorAll('.search-btn');
    searchButtons.forEach(btn => {
        btn.disabled = true;
        btn.textContent = 'Searching...';
    });
}

// Smooth scrolling for pagination
document.addEventListener('click', function(e) {
    if (e.target.closest('.pagination-link, .pagination-number')) {
        // Add smooth scrolling to top when navigating pages
        setTimeout(() => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }, 100);
    }
});

// Apps menu simulation
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('apps-icon')) {
        alert('Google Apps menu is not implemented in this demo');
    }
});

// Profile menu simulation
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('profile-circle')) {
        alert('Profile menu is not implemented in this demo');
    }
});
