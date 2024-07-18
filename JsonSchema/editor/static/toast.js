let toastDismiss = null;

document.addEventListener('DOMContentLoaded', function() {
    const toast = document.getElementById('toast-default');
    const closeButton = toast.querySelector('button[data-dismiss-target]');

    console.log('Toast element:', toast);
    console.log('Close button:', closeButton);


    if (toast && closeButton) {
        const dismissOptions = {
            triggerEl: closeButton,
            targetEl: toast,
            transition: 'transition-opacity',
            duration: 300,
            timing: 'ease-out',
            onHide: () => {
                toast.classList.add('hidden');
            }
        };
        try {
            // Initialize the Dismiss instance
            toastDismiss = new Dismiss(toast, closeButton, dismissOptions);
            console.log("Dismiss object instantiated:", toastDismiss);
        } catch (error) {
            console.error("Error instantiating Dismiss object:", error);
        }
    }
    else{
        console.log("Toast or close button not found");
    }
});

function showToast(message, iconClass, duration = 3000) {
    const toast = document.getElementById('toast-default');
    const iconElement = document.getElementById('toast-icon');
    const messageElement = document.getElementById('toast-message');

    if (!toast || !iconElement || !messageElement) {
        console.error('Toast elements not found');
        return;
    }

    messageElement.textContent = message;
    iconElement.className = `inline-flex items-center justify-center flex-shrink-0 w-8 h-8 ${iconClass} bg-blue-100 rounded-lg`;

    toast.classList.remove('hidden');
    toast.classList.add('flex');
    toast.classList.remove('opacity-0');
    toast.classList.add('opacity-1');

    if (duration) {
        setTimeout(() => {
            toastDismiss.hide();
        }, duration);
    }
}

function hideToast() {
    if (toastDismiss) {
        toastDismiss.hide();
    }
}

function updateToast(message, iconClass) {
    const messageElement = document.getElementById('toast-message');
    const iconElement = document.getElementById('toast-icon');

    if (messageElement && iconElement) {
        messageElement.textContent = message;
        iconElement.className = `inline-flex items-center justify-center flex-shrink-0 w-8 h-8 ${iconClass} bg-blue-100 rounded-lg`;
    }
}

export { showToast, hideToast, updateToast };