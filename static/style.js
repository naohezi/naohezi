function showNotification() {
    const notification = document.getElementById('notification');
    if (notification) {
        // Show notification
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Hide after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
}

// Run when page loads
document.addEventListener('DOMContentLoaded', showNotification);
