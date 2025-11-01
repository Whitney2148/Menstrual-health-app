// Authentication helper functions
class AuthHelper {
    static getToken() {
        return localStorage.getItem('access_token');
    }
    
    static setToken(token) {
        localStorage.setItem('access_token', token);
    }
    
    static removeToken() {
        localStorage.removeItem('access_token');
    }
    
    static isAuthenticated() {
        return !!this.getToken();
    }
    
    static redirectToLogin() {
        window.location.href = '/login';
    }
    
    static async checkAuth() {
        const token = this.getToken();
        if (!token) {
            this.redirectToLogin();
            return false;
        }
        return true;
    }
}

// Form handling utilities
class FormHelper {
    static showLoading(button) {
        const originalText = button.innerHTML;
        button.disabled = true;
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    }
    
    static hideLoading(button) {
        const originalText = button.getAttribute('data-original-text');
        button.disabled = false;
        button.innerHTML = originalText;
    }
    
    static showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Add to top of page
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Check authentication on page load for protected pages
document.addEventListener('DOMContentLoaded', function() {
    const protectedPages = ['/dashboard', '/analysis', '/history'];
    const currentPath = window.location.pathname;
    
    if (protectedPages.includes(currentPath)) {
        AuthHelper.checkAuth();
    }
});