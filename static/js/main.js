// SME Debt Management Tool - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Language switching
    const languageDropdown = document.getElementById('languageDropdown');
    if (languageDropdown) {
        languageDropdown.addEventListener('click', function(e) {
            e.preventDefault();
        });
    }

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Number formatting for inputs
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !isNaN(this.value)) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });

    // Auto-save form data to localStorage
    const formsToSave = document.querySelectorAll('form[id$="Form"]');
    formsToSave.forEach(form => {
        const formId = form.id;
        
        // Load saved data
        const savedData = localStorage.getItem(formId);
        if (savedData) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = data[key];
                }
            });
        }

        // Save data on input change
        form.addEventListener('input', function(e) {
            const formData = new FormData(form);
            const data = {};
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            localStorage.setItem(formId, JSON.stringify(data));
        });
    });

    // Smooth scrolling for anchor links
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

    // Loading state management
    function showLoading(element) {
        element.classList.add('loading');
        element.style.position = 'relative';
    }

    function hideLoading(element) {
        element.classList.remove('loading');
    }

    // Error handling
    function showError(message, element = null) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        if (element) {
            element.insertBefore(alertDiv, element.firstChild);
        } else {
            document.body.insertBefore(alertDiv, document.body.firstChild);
        }
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Success message
    function showSuccess(message, element = null) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-success alert-dismissible fade show';
        alertDiv.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        if (element) {
            element.insertBefore(alertDiv, element.firstChild);
        } else {
            document.body.insertBefore(alertDiv, document.body.firstChild);
        }
        
        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 3000);
    }

    // Currency formatting
    function formatCurrency(amount, currency = '€') {
        return currency + parseFloat(amount).toLocaleString('de-DE', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    // Percentage formatting
    function formatPercentage(value, decimals = 2) {
        return parseFloat(value).toFixed(decimals) + '%';
    }

    // Number formatting
    function formatNumber(value, decimals = 0) {
        return parseFloat(value).toLocaleString('de-DE', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }

    // API request helper
    async function makeApiRequest(url, data, method = 'POST') {
        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Form data collection helper
    function collectFormData(form) {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            // Handle array inputs
            if (key.endsWith('[]')) {
                const arrayKey = key.slice(0, -2);
                if (!data[arrayKey]) {
                    data[arrayKey] = [];
                }
                data[arrayKey].push(value);
            } else {
                data[key] = value;
            }
        }
        return data;
    }

    // Chart helper (if needed for future enhancements)
    function createSimpleChart(canvasId, data, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;

        const ctx = canvas.getContext('2d');
        
        // Default options
        const defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        };

        // Merge options
        const chartOptions = { ...defaultOptions, ...options };

        // This would integrate with Chart.js if needed
        // return new Chart(ctx, { type: 'bar', data, options: chartOptions });
    }

    // Export functions to global scope for use in templates
    window.SMEDebtTool = {
        showLoading,
        hideLoading,
        showError,
        showSuccess,
        formatCurrency,
        formatPercentage,
        formatNumber,
        makeApiRequest,
        collectFormData,
        createSimpleChart
    };

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeForm = document.querySelector('form:focus-within');
            if (activeForm) {
                const submitBtn = activeForm.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.click();
                }
            }
        }
        
        // Escape to close modals/alerts
        if (e.key === 'Escape') {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                const closeBtn = alert.querySelector('.btn-close');
                if (closeBtn) {
                    closeBtn.click();
                }
            });
        }
    });

    // Performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', function() {
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            console.log(`Page load time: ${loadTime}ms`);
        });
    }

    // Service Worker registration (for future PWA capabilities)
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/sw.js')
                .then(function(registration) {
                    console.log('ServiceWorker registration successful');
                })
                .catch(function(err) {
                    console.log('ServiceWorker registration failed');
                });
        });
    }
});
