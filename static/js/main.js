document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
        });
    }
    
    // Auto-dismiss messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    if (messages.length > 0) {
        setTimeout(function() {
            messages.forEach(function(message) {
                message.style.opacity = '0';
                setTimeout(function() {
                    message.style.display = 'none';
                }, 300);
            });
        }, 5000);
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Create error message if it doesn't exist
                    let errorMessage = field.nextElementSibling;
                    if (!errorMessage || !errorMessage.classList.contains('form-error')) {
                        errorMessage = document.createElement('div');
                        errorMessage.classList.add('form-error');
                        errorMessage.textContent = 'This field is required';
                        field.parentNode.insertBefore(errorMessage, field.nextSibling);
                    }
                } else {
                    field.classList.remove('is-invalid');
                    
                    // Remove error message if it exists
                    const errorMessage = field.nextElementSibling;
                    if (errorMessage && errorMessage.classList.contains('form-error')) {
                        errorMessage.remove();
                    }
                }
            });
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    });
    
    // Blood request search filters
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        const filterInputs = filterForm.querySelectorAll('select, input');
        filterInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }
    
    // Real-time notifications with WebSockets (if available)
    setupNotifications();
});

function setupNotifications() {
    // Check if the browser supports WebSockets and if the user is authenticated
    if ('WebSocket' in window && document.body.dataset.userId) {
        const userId = document.body.dataset.userId;
        const notificationCount = document.getElementById('notification-count');
        
        // Connect to WebSocket server
        const ws = new WebSocket(`ws://${window.location.host}/ws/notifications/${userId}/`);
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            
            // Update notification count
            if (notificationCount) {
                notificationCount.textContent = data.unread_count;
                if (data.unread_count > 0) {
                    notificationCount.classList.add('has-notifications');
                } else {
                    notificationCount.classList.remove('has-notifications');
                }
            }
            
            // Show notification toast
            if (data.notification) {
                showNotificationToast(data.notification);
            }
        };
        
        ws.onclose = function() {
            console.log('Notification WebSocket closed. Reconnecting...');
            setTimeout(setupNotifications, 5000);
        };
    }
}

function showNotificationToast(notification) {
    // Create toast element
    const toast = document.createElement('div');
    toast.classList.add('notification-toast');
    
    toast.innerHTML = `
        <div class="notification-toast-header">
            <strong>${notification.title}</strong>
            <button type="button" class="toast-close">&times;</button>
        </div>
        <div class="notification-toast-body">
            ${notification.message}
        </div>
    `;
    
    // Add to document
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.classList.add('toast-container');
        document.body.appendChild(container);
        container.appendChild(toast);
    } else {
        toastContainer.appendChild(toast);
    }
    
    // Add close button functionality
    const closeButton = toast.querySelector('.toast-close');
    closeButton.addEventListener('click', function() {
        toast.classList.add('hiding');
        setTimeout(function() {
            toast.remove();
        }, 300);
    });
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        toast.classList.add('hiding');
        setTimeout(function() {
            toast.remove();
        }, 300);
    }, 5000);
}

// Donation verification
const verifyButtons = document.querySelectorAll('.verify-donation-btn');
if (verifyButtons.length > 0) {
    verifyButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to verify this donation?')) {
                event.preventDefault();
            }
        });
    });
}

// Blood request status update
const statusUpdateForm = document.getElementById('status-update-form');
if (statusUpdateForm) {
    const statusSelect = statusUpdateForm.querySelector('select[name="status"]');
    statusSelect.addEventListener('change', function() {
        if (confirm('Are you sure you want to update the status?')) {
            statusUpdateForm.submit();
        } else {
            statusSelect.value = statusSelect.dataset.originalValue;
        }
    });
}

// Donor availability toggle
const availabilityToggle = document.getElementById('availability-toggle');
if (availabilityToggle) {
    availabilityToggle.addEventListener('change', function() {
        const form = this.closest('form');
        form.submit();
    });
}


document.addEventListener('DOMContentLoaded', function() {
    const userDropdown = document.getElementById('userDropdown');
    const dropdownMenu = document.getElementById('dropdownMenu');

    if (userDropdown && dropdownMenu) {
        userDropdown.addEventListener('click', function(event) {
            event.preventDefault();
            dropdownMenu.classList.toggle('show');
        });

        // Hide dropdown when clicking outside
        document.addEventListener('click', function(event) {
            if (!userDropdown.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.remove('show');
            }
        });
    }
});
