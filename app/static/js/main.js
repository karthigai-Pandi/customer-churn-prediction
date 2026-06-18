/* Main JavaScript File */

// Utility function to show toast notifications
function showToast(message, type = 'info') {
    const toastHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    const container = document.querySelector('.container-fluid') || document.body;
    const div = document.createElement('div');
    div.innerHTML = toastHTML;
    container.insertBefore(div.firstElementChild, container.firstChild);
}

// Format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

// Format percentage
function formatPercentage(value) {
    return (value * 100).toFixed(2) + '%';
}

// API call wrapper
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'An error occurred');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(element => {
        new bootstrap.Tooltip(element);
    });

    // Bootstrap popovers
    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    popovers.forEach(element => {
        new bootstrap.Popover(element);
    });
});

// Logout confirmation
function confirmLogout() {
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = '/auth/logout';
    }
}

// Date formatting
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Export functionality
async function exportToPDF() {
    try {
        const response = await fetch('/api/export/predictions?format=pdf', {
            headers: {
                'X-API-Key': 'demo-key-12345'
            }
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'predictions.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            showToast('PDF exported successfully!', 'success');
        } else {
            showToast('Failed to export PDF', 'danger');
        }
    } catch (error) {
        showToast('Error exporting PDF: ' + error.message, 'danger');
    }
}

async function exportToCSV() {
    try {
        const response = await fetch('/api/export/predictions?format=csv', {
            headers: {
                'X-API-Key': 'demo-key-12345'
            }
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'predictions.csv';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            showToast('CSV exported successfully!', 'success');
        } else {
            showToast('Failed to export CSV', 'danger');
        }
    } catch (error) {
        showToast('Error exporting CSV: ' + error.message, 'danger');
    }
}

// Real-time form validation
function setupFormValidation(formId) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function(e) {
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.classList.add('was-validated');
    });
}

// Search functionality
function setupSearch(searchInputId, searchFunction) {
    const searchInput = document.getElementById(searchInputId);
    if (!searchInput) return;

    let timeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            searchFunction(this.value);
        }, 500);
    });
}

// Pagination
function setupPagination(pageLinks) {
    pageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = this.href;
        });
    });
}

// Loading spinner
function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border';
    spinner.id = 'loading-spinner';
    document.body.appendChild(spinner);
}

function hideLoading() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) spinner.remove();
}

// Chart configuration
const chartColors = {
    primary: 'rgba(102, 126, 234, 1)',
    secondary: 'rgba(118, 75, 162, 1)',
    success: 'rgba(40, 167, 69, 1)',
    danger: 'rgba(220, 53, 69, 1)',
    warning: 'rgba(255, 193, 7, 1)',
    info: 'rgba(23, 162, 184, 1)'
};

// Initialize charts
function initializeCharts() {
    Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
    Chart.defaults.plugins.legend.labels.padding = 15;
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initializeCharts);
