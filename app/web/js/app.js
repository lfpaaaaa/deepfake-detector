// Status configuration
const STATUS_CONFIG = {
    'AUTHENTIC': {
        alertClass: 'alert-success',
        title: 'Detection Result: Authentic',
        text: 'No deepfake detected',
        statText: 'Authentic',
        statColor: 'text-success',
        iconPath: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
    },
    'FAKE': {
        alertClass: 'alert-error',
        title: 'Detection Result: Fake',
        text: 'Deepfake features detected',
        statText: 'Fake',
        statColor: 'text-error',
        iconPath: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z'
    },
    'UNCERTAIN': {
        alertClass: 'alert-warning',
        title: 'Detection Result: Uncertain',
        text: 'Unable to determine authenticity',
        statText: 'Uncertain',
        statColor: 'text-warning',
        iconPath: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'
    }
};

// DOM elements
const elements = {
    uploadCard: document.getElementById('uploadCard'),
    uploadZone: document.getElementById('uploadZone'),
    fileInput: document.getElementById('fileInput'),
    loadingState: document.getElementById('loadingState'),
    errorAlert: document.getElementById('errorAlert'),
    errorText: document.getElementById('errorText'),
    resultPanel: document.getElementById('resultPanel'),
    statusAlert: document.getElementById('statusAlert'),
    statusIcon: document.getElementById('statusIcon'),
    statusTitle: document.getElementById('statusTitle'),
    statusText: document.getElementById('statusText'),
    resultStatus: document.getElementById('resultStatus'),
    resultDesc: document.getElementById('resultDesc'),
    confidenceBar: document.getElementById('confidenceBar'),
    confidenceText: document.getElementById('confidenceText'),
    technicalDetails: document.getElementById('technicalDetails'),
    themeToggle: document.getElementById('themeToggle')
};

// File validation
function validateFile(file) {
    const allowedTypes = ['image/jpeg', 'image/png', 'video/mp4', 'video/quicktime'];
    const maxImageSize = 10 * 1024 * 1024; // 10MB
    const maxVideoSize = 50 * 1024 * 1024; // 50MB
    
    if (!allowedTypes.includes(file.type)) {
        showError('Unsupported file type. Please upload JPG, PNG, MP4 or MOV files.');
        return false;
    }
    
    const isVideo = file.type.startsWith('video/');
    const maxSize = isVideo ? maxVideoSize : maxImageSize;
    
    if (file.size > maxSize) {
        const maxSizeMB = maxSize / (1024 * 1024);
        showError(`File too large. Maximum size: ${maxSizeMB}MB.`);
        return false;
    }
    
    return true;
}

// Show error
function showError(message) {
    elements.errorText.textContent = message;
    elements.errorAlert.classList.remove('hidden');
    setTimeout(() => {
        elements.errorAlert.classList.add('hidden');
    }, 5000);
}

// Handle file
async function handleFile(file) {
    if (!validateFile(file)) {
        return;
    }
    
    // Hide errors and results
    elements.errorAlert.classList.add('hidden');
    elements.resultPanel.classList.add('hidden');
    
    // Hide upload card and show loading state
    elements.uploadCard.classList.add('hidden');
    elements.loadingState.classList.remove('hidden');
    
    // Create FormData
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/detect', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Detection failed');
        }
        
        const result = await response.json();
        displayResult(result);
        
    } catch (error) {
        showError(error.message || 'An error occurred during detection');
        resetUpload();
    }
}

// Display results
function displayResult(data) {
    const config = STATUS_CONFIG[data.status] || STATUS_CONFIG['UNCERTAIN'];
    
    // Update status alert
    elements.statusAlert.className = `alert ${config.alertClass} shadow-lg`;
    elements.statusIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${config.iconPath}" />`;
    elements.statusTitle.textContent = config.title;
    elements.statusText.textContent = config.text;
    
    // Update statistics
    elements.resultStatus.textContent = config.statText;
    elements.resultStatus.className = `stat-value text-2xl ${config.statColor}`;
    elements.resultDesc.textContent = `Request ID: ${data.request_id}`;
    
    // Update confidence
    const confidence = Math.round(data.score * 100);
    elements.confidenceBar.value = confidence;
    elements.confidenceText.textContent = `${confidence}%`;
    
    // Update technical details
    const details = {
        ...data.vendor_raw,
        media_type: data.media_type,
        score_scale: data.score_scale
    };
    elements.technicalDetails.textContent = JSON.stringify(details, null, 2);
    
    // Hide loading, show results
    elements.loadingState.classList.add('hidden');
    elements.resultPanel.classList.remove('hidden');
}

// Reset upload
function resetUpload() {
    elements.uploadCard.classList.remove('hidden');
    elements.uploadZone.classList.remove('hidden');
    elements.loadingState.classList.add('hidden');
    elements.resultPanel.classList.add('hidden');
    elements.errorAlert.classList.add('hidden');
    elements.fileInput.value = '';
}

// Drag and drop events
elements.uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    elements.uploadZone.classList.add('border-primary', 'bg-base-200');
});

elements.uploadZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    elements.uploadZone.classList.remove('border-primary', 'bg-base-200');
});

elements.uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    elements.uploadZone.classList.remove('border-primary', 'bg-base-200');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// File selection event
elements.fileInput.addEventListener('change', (e) => {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// Theme toggle
elements.themeToggle.addEventListener('change', (e) => {
    const theme = e.target.checked ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
});

// Initialize theme
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    elements.themeToggle.checked = savedTheme === 'dark';
});