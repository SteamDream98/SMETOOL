// SME Debt Management Tool - Mobile-Optimized JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile-specific initialization
    initializeMobileFeatures();
    initializeTouchInteractions();
    initializeFormValidation();
    initializeAnimations();
});

// Mobile-specific features
function initializeMobileFeatures() {
    // Prevent zoom on input focus (iOS)
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            if (window.innerWidth < 768) {
                const viewport = document.querySelector('meta[name="viewport"]');
                viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
            }
        });
        
        input.addEventListener('blur', function() {
            if (window.innerWidth < 768) {
                const viewport = document.querySelector('meta[name="viewport"]');
                viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, user-scalable=no');
            }
        });
    });
    
    // Add touch-friendly classes
    addTouchFriendlyClasses();
    
    // Initialize mobile navigation
    initializeMobileNavigation();
}

// Touch-friendly interactions
function initializeTouchInteractions() {
    // Add touch feedback to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('touchstart', function() {
            this.classList.add('btn-touch-active');
        });
        
        button.addEventListener('touchend', function() {
            setTimeout(() => {
                this.classList.remove('btn-touch-active');
            }, 150);
        });
    });
    
    // Add touch feedback to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('touchstart', function() {
            this.classList.add('card-touch-active');
        });
        
        card.addEventListener('touchend', function() {
            setTimeout(() => {
                this.classList.remove('card-touch-active');
            }, 150);
        });
    });
}

// Form validation and enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showMobileError('Please fill in all required fields correctly.');
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
    });
}

// Form validation functions
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    let isValid = true;
    let errorMessage = '';
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required.';
    }
    
    // Type-specific validation
    if (value && type === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address.';
        }
    }
    
    if (value && type === 'number') {
        const num = parseFloat(value);
        if (isNaN(num) || num < 0) {
            isValid = false;
            errorMessage = 'Please enter a valid positive number.';
        }
    }
    
    if (value && field.hasAttribute('min')) {
        const min = parseFloat(field.getAttribute('min'));
        const num = parseFloat(value);
        if (num < min) {
            isValid = false;
            errorMessage = `Value must be at least ${min}.`;
        }
    }
    
    if (value && field.hasAttribute('max')) {
        const max = parseFloat(field.getAttribute('max'));
        const num = parseFloat(value);
        if (num > max) {
            isValid = false;
            errorMessage = `Value must be no more than ${max}.`;
        }
    }
    
    // Show/hide error
    if (!isValid) {
        showFieldError(field, errorMessage);
    } else {
        clearFieldError(field);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Mobile navigation
function initializeMobileNavigation() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navbarCollapse.contains(e.target) && !navbarToggler.contains(e.target)) {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            }
        });
        
        // Close mobile menu when clicking on a link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }
    
}


// Animations
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll('.card, .alert, .feature-icon');
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// Utility functions
function addTouchFriendlyClasses() {
    // Add touch-friendly classes to interactive elements
    const touchElements = document.querySelectorAll('button, .btn, .nav-link, .dropdown-item');
    touchElements.forEach(el => {
        el.classList.add('touch-friendly');
    });
}

function showMobileError(message) {
    // Create mobile-friendly error notification
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed';
    errorDiv.style.cssText = 'top: 20px; left: 20px; right: 20px; z-index: 9999; border-radius: 1rem;';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(errorDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

function showMobileSuccess(message) {
    // Create mobile-friendly success notification
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
    successDiv.style.cssText = 'top: 20px; left: 20px; right: 20px; z-index: 9999; border-radius: 1rem;';
    successDiv.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(successDiv);
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        if (successDiv.parentNode) {
            successDiv.remove();
        }
    }, 3000);
}

// Global utility functions for all pages
function formatNumber(value) {
    if (typeof value === 'number') {
        if (value >= 1000000) {
            return '€' + (value / 1000000).toFixed(1) + 'M';
        } else if (value >= 1000) {
            return '€' + (value / 1000).toFixed(1) + 'K';
        } else {
            return '€' + value.toFixed(2);
        }
    }
    return value;
}

// Add CSS for touch interactions
const style = document.createElement('style');
style.textContent = `
    .btn-touch-active {
        transform: scale(0.95);
        opacity: 0.8;
    }
    
    .card-touch-active {
        transform: scale(0.98);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .touch-friendly {
        min-height: 44px;
        min-width: 44px;
    }
    
    .invalid-feedback {
        display: block;
        font-size: 0.875rem;
        color: var(--danger-color);
        margin-top: 0.25rem;
    }
    
    .is-invalid {
        border-color: var(--danger-color);
    }
    
    .is-invalid:focus {
        border-color: var(--danger-color);
        box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
    }
`;
document.head.appendChild(style);
