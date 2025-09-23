// Status configuration
// Decision configuration - Five-tier system
const DECISION_CONFIG = {
    'AUTHENTIC': {
        alertClass: 'alert-success',
        title: 'AUTHENTIC',
        text: 'High confidence authentic image.',
        statText: 'AUTHENTIC',
        statColor: 'text-success',
        iconPath: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
        badgeClass: 'badge-success'
    },
    'LIKELY_AUTHENTIC': {
        alertClass: 'alert-info',
        title: 'LIKELY AUTHENTIC',
        text: 'Moderate confidence authentic image.',
        statText: 'LIKELY AUTHENTIC',
        statColor: 'text-info',
        iconPath: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
        badgeClass: 'badge-info'
    },
    'INCONCLUSIVE': {
        alertClass: 'alert-warning',
        title: 'INCONCLUSIVE',
        text: 'Unable to determine authenticity with confidence.',
        statText: 'INCONCLUSIVE',
        statColor: 'text-warning',
        iconPath: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z',
        badgeClass: 'badge-warning'
    },
    'LIKELY_FORGED': {
        alertClass: 'alert-error',
        title: 'LIKELY FORGED',
        text: 'Moderate confidence forged image.',
        statText: 'LIKELY FORGED',
        statColor: 'text-error',
        iconPath: 'M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
        badgeClass: 'badge-error'
    },
    'FORGED': {
        alertClass: 'alert-error',
        title: 'FORGED',
        text: 'High confidence forged image.',
        statText: 'FORGED',
        statColor: 'text-error',
        iconPath: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
        badgeClass: 'badge-error'
    }
};

// Decision logic function
function determineDecision(integrity, evidenceReliability) {
    const integrityPercent = Math.round(integrity * 100);
    const reliabilityPercent = Math.round(evidenceReliability * 100);
    
    // Decision thresholds based on your requirements
    console.log(`Decision logic: integrity=${integrityPercent}%, reliability=${reliabilityPercent}%`);
    
    if (integrityPercent >= 70 && reliabilityPercent >= 40) {
        console.log('Decision: AUTHENTIC');
        return 'AUTHENTIC';
    } else if (integrityPercent >= 55 && integrityPercent < 70) {
        console.log('Decision: LIKELY_AUTHENTIC');
        return 'LIKELY_AUTHENTIC';
    } else if (integrityPercent >= 45 && integrityPercent < 55) {
        console.log('Decision: INCONCLUSIVE');
        return 'INCONCLUSIVE';
    } else if (integrityPercent >= 30 && integrityPercent < 45 && reliabilityPercent >= 40) {
        console.log('Decision: LIKELY_FORGED');
        return 'LIKELY_FORGED';
    } else if (integrityPercent < 30 && reliabilityPercent >= 50) {
        console.log('Decision: FORGED');
        return 'FORGED';
    } else {
        console.log('Decision: INCONCLUSIVE (default)');
        return 'INCONCLUSIVE'; // Default for edge cases
    }
}

// 🎨 UPDATED VERSION WITH SMOOTH COLORMAP - NO BLACK REGIONS! 🎨
console.log('🎨 JavaScript loaded: UI IMPROVEMENTS VERSION 2.0 - FIVE-TIER DECISION SYSTEM!');
console.log('🔧 DEBUG: New decision logic is active!');
console.log('🔧 DEBUG: Evidence Reliability calculation is active!');

// DOM elements are defined in HTML - using global elements object

// Check for missing elements
console.log('Checking DOM elements...');
for (const [name, element] of Object.entries(elements)) {
    if (!element) {
        console.error(`Missing DOM element: ${name}`);
    } else {
        console.log(`Found element: ${name}`);
    }
}

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
    console.log('File selected:', file.name, file.type, file.size);
    
    if (!validateFile(file)) {
        console.log('File validation failed');
        return;
    }
    
    console.log('File validation passed, starting detection...');
    
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
        console.log('Sending request to /detect...');
        const response = await fetch('/detect', {
            method: 'POST',
            body: formData
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const error = await response.json();
            console.error('API error:', error);
            throw new Error(error.detail || 'Detection failed');
        }
        
        const result = await response.json();
        console.log('Detection result:', result);
        displayResult(result);
        
    } catch (error) {
        console.error('Detection error:', error);
        showError(error.message || 'An error occurred during detection');
        resetUpload();
    }
}

// Display results
function displayResult(data) {
    console.log('🔧 DEBUG: displayResult called with data:', data);
    // Determine if this is TruFor response
    const isTruFor = data.model === 'TruFor';
    console.log('🔧 DEBUG: isTruFor:', isTruFor);
    
    // Update status based on TruFor response format
    let status, config;
    if (isTruFor) {
        // Calculate evidence reliability from confidence map
        let evidenceReliability = 0.5; // Default
        if (data.confidence_map) {
            const confData = data.confidence_map.flat();
            const avgConfidence = confData.reduce((sum, val) => sum + val, 0) / confData.length;
            evidenceReliability = avgConfidence;
            console.log(`Evidence Reliability calculated: ${avgConfidence} (${Math.round(avgConfidence * 100)}%)`);
        }
        
        // Determine decision using new five-tier system
        status = determineDecision(data.integrity, evidenceReliability);
        config = DECISION_CONFIG[status];
        console.log(`Decision: integrity=${data.integrity} (${Math.round(data.integrity * 100)}%), reliability=${evidenceReliability} (${Math.round(evidenceReliability * 100)}%) -> ${status}`);
        
        // Update status alert
        elements.statusAlert.className = `alert ${config.alertClass} shadow-lg`;
        elements.statusIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${config.iconPath}" />`;
        elements.statusTitle.textContent = config.title;
        elements.statusText.textContent = config.text;
        
        // Update statistics
        elements.resultStatus.textContent = config.statText;
        elements.resultStatus.className = `stat-value text-2xl ${config.statColor}`;
        elements.resultDesc.textContent = `Model: ${data.model} | Filename: ${data.filename}`;
        
        // Update evidence reliability
        if (data.confidence_map) {
            const confData = data.confidence_map.flat();
            const avgConfidence = confData.reduce((sum, val) => sum + val, 0) / confData.length;
            const reliabilityPercent = Math.round(avgConfidence * 100);
            console.log(`Evidence Reliability display: ${avgConfidence} -> ${reliabilityPercent}%`);
            elements.confidenceText.textContent = `${reliabilityPercent}%`;
            elements.confidenceBar.value = reliabilityPercent;
        } else {
            const confidence = Math.round(data.confidence * 100);
            console.log(`Using fallback confidence: ${confidence}%`);
            elements.confidenceBar.value = confidence;
            elements.confidenceText.textContent = `${confidence}%`;
        }
        
        // Show detection score for TruFor
        if (data.detection_score !== undefined) {
            elements.detectionScoreStat.style.display = 'block';
            const detectionScore = Math.round(data.detection_score * 100);
            elements.detectionScoreBar.value = detectionScore;
            elements.detectionScoreText.textContent = `${detectionScore}%`;
        }
        
        // Show TruFor visualization
        if (data.prediction_map) {
            elements.truforVisualization.classList.remove('hidden');
            elements.detectionScoreStat.style.display = 'block';
            elements.fakeLikelihoodStat.style.display = 'block';
            displayTruForVisualization(data);
            
            // Display portrait mode detection note
            if (data.portrait_note) {
                console.log('Portrait mode detected:', data.portrait_note);
                // Create or update portrait note element
                let portraitNoteElement = document.getElementById('portraitNote');
                if (!portraitNoteElement) {
                    portraitNoteElement = document.createElement('div');
                    portraitNoteElement.id = 'portraitNote';
                    portraitNoteElement.className = 'mt-4 p-3 bg-blue-100 border border-blue-300 rounded-lg text-sm text-blue-800';
                    elements.truforVisualization.querySelector('.card-body').appendChild(portraitNoteElement);
                }
                portraitNoteElement.textContent = data.portrait_note;
                portraitNoteElement.style.display = 'block';
            } else {
                // Hide portrait note if not detected
                const portraitNoteElement = document.getElementById('portraitNote');
                if (portraitNoteElement) {
                    portraitNoteElement.style.display = 'none';
                }
            }
        }
        
        // Update technical details
        const details = {
            model: data.model,
            is_fake: data.is_fake,
            confidence: data.confidence,
            detection_score: data.detection_score,
            image_size: data.image_size,
            has_confidence_map: data.has_confidence_map,
            has_noiseprint: data.has_noiseprint,
            prediction_map_size: data.prediction_map ? data.prediction_map.length : 0
        };
        elements.technicalDetails.textContent = JSON.stringify(details, null, 2);
        
    } else {
        // Legacy format for other models
        config = DECISION_CONFIG[data.status] || DECISION_CONFIG['INCONCLUSIVE'];
        
        // Update status alert
        elements.statusAlert.className = `alert ${config.alertClass} shadow-lg`;
        elements.statusIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${config.iconPath}" />`;
        elements.statusTitle.textContent = config.title;
        elements.statusText.textContent = config.text;
        
        // Update statistics
        elements.resultStatus.textContent = config.statText;
        elements.resultStatus.className = `stat-value text-2xl ${config.statColor}`;
        elements.resultDesc.textContent = `Request ID: ${data.request_id || 'N/A'}`;
        
        // Update confidence
        const confidence = Math.round((data.score || 0) * 100);
        elements.confidenceBar.value = confidence;
        elements.confidenceText.textContent = `${confidence}%`;
        
        // Hide TruFor-specific elements
        elements.truforVisualization.classList.add('hidden');
        elements.detectionScoreStat.style.display = 'none';
        
        // Update technical details
        const details = {
            ...data.vendor_raw,
            media_type: data.media_type,
            score_scale: data.score_scale
        };
        elements.technicalDetails.textContent = JSON.stringify(details, null, 2);
    }
    
    // Hide loading, show results
    elements.loadingState.classList.add('hidden');
    elements.resultPanel.classList.remove('hidden');
}

// Display TruFor visualization
function displayTruForVisualization(data) {
    // Store current image data for visualization
    window.currentImageData = data;
    
    // Display original image
    if (data.original_image_url) {
        elements.originalImage.src = data.original_image_url;
        elements.originalImage.onload = function() {
            // Set canvas size to match image size
            const imgWidth = elements.originalImage.naturalWidth;
            const imgHeight = elements.originalImage.naturalHeight;
            
            // Set canvas size to fixed 300x300 for consistent layout
            const canvasSize = 300;
            elements.predictionOverlay.width = canvasSize;
            elements.predictionOverlay.height = canvasSize;
            elements.predictionHeatmap.width = canvasSize;
            elements.predictionHeatmap.height = canvasSize;
            elements.confidenceMap.width = canvasSize;
            elements.confidenceMap.height = canvasSize;
            elements.noiseprintMap.width = canvasSize;
            elements.noiseprintMap.height = canvasSize;
            
            // Redraw visualizations with correct size
            if (data.prediction_map) {
                drawHeatmap(elements.predictionHeatmap, data.prediction_map, 'forgery');
                drawPredictionOverlay(elements.predictionOverlay, data.prediction_map);
            }
        };
    } else {
        // If no original image URL, we'll need to create one from the uploaded file
        // For now, we'll show a placeholder
        elements.originalImage.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjNmNGY2Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxOCIgZmlsbD0iIzk5YTNhZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIFByZXZpZXc8L3RleHQ+PC9zdmc+';
    }
    
    // Set canvas sizes to 300x300 for consistent layout
    const canvasSize = 300;
    elements.predictionHeatmap.width = canvasSize;
    elements.predictionHeatmap.height = canvasSize;
    elements.confidenceMap.width = canvasSize;
    elements.confidenceMap.height = canvasSize;
    elements.noiseprintMap.width = canvasSize;
    elements.noiseprintMap.height = canvasSize;
    
    // Draw prediction heatmap
    if (data.prediction_map) {
        drawHeatmap(elements.predictionHeatmap, data.prediction_map, 'forgery');
    }
    
    // Draw confidence map
    if (data.confidence_map) {
        drawHeatmap(elements.confidenceMap, data.confidence_map, 'confidence');
    }
    
    // Draw noiseprint map
    if (data.noiseprint_map) {
        drawHeatmap(elements.noiseprintMap, data.noiseprint_map, 'noiseprint');
    }
    
    // Draw prediction overlay on original image
    if (data.prediction_map) {
        drawPredictionOverlay(elements.predictionOverlay, data.prediction_map);
    }
    
    // Update Integrity Score and Fake Likelihood
    if (data.integrity !== undefined) {
        const integrityPercent = Math.round(data.integrity * 100);
        const fakeLikelihoodPercent = Math.round((1 - data.integrity) * 100);
        
        // Update integrity score
        elements.integrityScore.textContent = integrityPercent;
        
        // Update label and progress bar
        if (data.integrity > 0.5) {
            elements.integrityLabel.textContent = 'AUTHENTIC';
            elements.integrityBar.className = 'bg-green-600 h-3 rounded-full transition-all duration-500';
        } else {
            elements.integrityLabel.textContent = 'FAKE';
            elements.integrityBar.className = 'bg-red-600 h-3 rounded-full transition-all duration-500';
        }
        
        // Update progress bar width
        elements.integrityBar.style.width = `${integrityPercent}%`;
        
        // Update fake likelihood (if element exists)
        if (elements.fakeLikelihoodText) {
            elements.fakeLikelihoodText.textContent = fakeLikelihoodPercent;
            elements.fakeLikelihoodBar.style.width = `${fakeLikelihoodPercent}%`;
        }
        
        console.log(`Integrity Score updated: ${integrityPercent}% (${elements.integrityLabel.textContent})`);
        console.log(`Fake Likelihood: ${fakeLikelihoodPercent}%`);
    }
}

// Improved JET colormap function (blue to red) - smoother transitions
function jetColormap(value, channel) {
    // Clamp value to [0, 1]
    value = Math.max(0, Math.min(1, value));
    
    // Smoother JET colormap with better transitions
    if (channel === 0) { // Red
        if (value < 0.125) return 0;
        if (value < 0.375) return 4 * (value - 0.125);
        if (value < 0.625) return 1;
        if (value < 0.875) return 1 - 4 * (value - 0.625);
        return 0;
    } else if (channel === 1) { // Green
        if (value < 0.25) return 4 * value;
        if (value < 0.5) return 1;
        if (value < 0.75) return 1 - 4 * (value - 0.5);
        return 0;
    } else { // Blue
        if (value < 0.25) return 0.5 + 2 * value;
        if (value < 0.5) return 1 - 2 * (value - 0.25);
        return 0;
    }
}

// Simple and smooth colormap (blue to red) - no black regions
function smoothColormap(value) {
    // Clamp value to [0, 1]
    value = Math.max(0, Math.min(1, value));
    
    // Simple linear interpolation from blue to red
    // Blue (0,0,255) -> Cyan (0,255,255) -> Green (0,255,0) -> Yellow (255,255,0) -> Red (255,0,0)
    
    if (value < 0.25) {
        // Blue to Cyan: (0,0,255) to (0,255,255)
        const t = value * 4;
        return [0, t, 1];
    } else if (value < 0.5) {
        // Cyan to Green: (0,255,255) to (0,255,0)
        const t = (value - 0.25) * 4;
        return [0, 1, 1 - t];
    } else if (value < 0.75) {
        // Green to Yellow: (0,255,0) to (255,255,0)
        const t = (value - 0.5) * 4;
        return [t, 1, 0];
    } else {
        // Yellow to Red: (255,255,0) to (255,0,0)
        const t = (value - 0.75) * 4;
        return [1, 1 - t, 0];
    }
}

// Draw heatmap on canvas - UPDATED VERSION WITH SMOOTH COLORMAP
function drawHeatmap(canvas, data, type) {
    console.log(`🎨 NEW VERSION: Drawing ${type} heatmap with SMOOTH COLORMAP...`);
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    console.log(`Canvas size: ${width}x${height}`);
    console.log(`Data size: ${data.length}x${data[0].length}`);
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Create image data
    const imageData = ctx.createImageData(width, height);
    const pixels = imageData.data;
    
    // Debug data range
    let minVal = Infinity;
    let maxVal = -Infinity;
    for (let y = 0; y < data.length; y++) {
        for (let x = 0; x < data[y].length; x++) {
            const value = data[y][x];
            if (value < minVal) minVal = value;
            if (value > maxVal) maxVal = value;
        }
    }
    console.log(`${type} data range:`, minVal, 'to', maxVal);
    console.log(`🎨 USING SMOOTH COLORMAP for type: ${type}`);
    
    // Test smoothColormap function
    if (type === 'forgery') {
        console.log('🧪 Testing smoothColormap:');
        console.log('Value 0.0:', smoothColormap(0.0));
        console.log('Value 0.25:', smoothColormap(0.25));
        console.log('Value 0.5:', smoothColormap(0.5));
        console.log('Value 0.75:', smoothColormap(0.75));
        console.log('Value 1.0:', smoothColormap(1.0));
    }
    
    // Draw heatmap based on type
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const dataX = Math.floor((x / width) * data[0].length);
            const dataY = Math.floor((y / height) * data.length);
            const pixelIndex = (y * width + x) * 4;
            
            if (dataY < data.length && dataX < data[dataY].length) {
                const value = data[dataY][dataX];
                
                if (type === 'forgery') {
                    // Anomaly map: Smooth colormap (blue to red) - no black regions
                    const normalizedValue = Math.max(0, Math.min(1, value));
                    const [r, g, b] = smoothColormap(normalizedValue);
                    
                    // Debug: Check for black regions
                    if (r === 0 && g === 0 && b === 0) {
                        console.log(`Black pixel detected at (${x}, ${y}), value: ${value}, normalized: ${normalizedValue}`);
                    }
                    
                    pixels[pixelIndex] = Math.round(255 * r);     // Red
                    pixels[pixelIndex + 1] = Math.round(255 * g); // Green
                    pixels[pixelIndex + 2] = Math.round(255 * b); // Blue
                    pixels[pixelIndex + 3] = 255; // Alpha
                    
                } else if (type === 'confidence') {
                    // Confidence map: grayscale with slight contrast enhancement
                    const normalizedValue = Math.max(0, Math.min(1, value));
                    // Apply slight contrast enhancement: map [0.3, 0.9] to [0, 1]
                    const enhancedValue = Math.max(0, Math.min(1, (normalizedValue - 0.3) / 0.6));
                    const intensity = Math.round(255 * enhancedValue);
                    
                    pixels[pixelIndex] = intensity;     // Red
                    pixels[pixelIndex + 1] = intensity; // Green
                    pixels[pixelIndex + 2] = intensity; // Blue
                    pixels[pixelIndex + 3] = 255;       // Alpha
                    
                } else if (type === 'noiseprint') {
                    // Noiseprint++: grayscale
                    const normalizedValue = Math.max(0, Math.min(1, value));
                    const intensity = Math.round(255 * normalizedValue);
                    
                    pixels[pixelIndex] = intensity;     // Red
                    pixels[pixelIndex + 1] = intensity; // Green
                    pixels[pixelIndex + 2] = intensity; // Blue
                    pixels[pixelIndex + 3] = 255;       // Alpha
                }
            } else {
                // Fill out-of-bounds pixels with black
                pixels[pixelIndex] = 0;
                pixels[pixelIndex + 1] = 0;
                pixels[pixelIndex + 2] = 0;
                pixels[pixelIndex + 3] = 255;
            }
        }
    }
    
    ctx.putImageData(imageData, 0, 0);
    console.log(`✅ NEW VERSION: ${type} heatmap drawn successfully with SMOOTH COLORMAP!`);
}

// Draw prediction overlay on original image
function drawPredictionOverlay(canvas, data) {
    const ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;
    
    // Set canvas size to match display size
    canvas.width = width;
    canvas.height = height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Create image data
    const imageData = ctx.createImageData(width, height);
    const pixels = imageData.data;
    
    // Convert 2D array to 1D for processing
    const flatData = data.flat();
    const minVal = Math.min(...flatData);
    const maxVal = Math.max(...flatData);
    const range = maxVal - minVal;
    
    // Draw overlay
    for (let i = 0; i < pixels.length; i += 4) {
        const pixelIndex = Math.floor(i / 4);
        const x = pixelIndex % width;
        const y = Math.floor(pixelIndex / width);
        
        // Map 2D data to 1D pixel index
        const dataX = Math.floor((x / width) * data[0].length);
        const dataY = Math.floor((y / height) * data.length);
        
        if (dataY < data.length && dataX < data[dataY].length) {
            const value = data[dataY][dataX];
            const normalizedValue = range > 0 ? (value - minVal) / range : 0;
            
            // Only show overlay for high confidence predictions
            if (normalizedValue > 0.5) {
                const intensity = (normalizedValue - 0.5) * 2; // Scale from 0.5-1 to 0-1
                pixels[i] = 255;     // Red
                pixels[i + 1] = 0;   // Green
                pixels[i + 2] = 0;   // Blue
                pixels[i + 3] = Math.round(intensity * 128); // Alpha
            }
        }
    }
    
    ctx.putImageData(imageData, 0, 0);
}

// Reset upload
function resetUpload() {
    elements.uploadCard.classList.remove('hidden');
    elements.uploadZone.classList.remove('hidden');
    elements.loadingState.classList.add('hidden');
    elements.resultPanel.classList.add('hidden');
    elements.errorAlert.classList.add('hidden');
    elements.truforVisualization.classList.add('hidden');
    elements.detectionScoreStat.style.display = 'none';
    elements.fileInput.value = '';
    
    // Clear current image data
    window.currentImageData = null;
}

// Drag and drop events
if (elements.uploadZone) {
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
        
        console.log('File dropped');
        const files = e.dataTransfer.files;
        console.log('Files dropped:', files.length);
        if (files.length > 0) {
            console.log('Processing dropped file:', files[0].name);
            handleFile(files[0]);
        }
    });
} else {
    console.error('uploadZone element not found!');
}

// File selection event
if (elements.fileInput) {
    elements.fileInput.addEventListener('change', (e) => {
        console.log('File input changed');
        const files = e.target.files;
        console.log('Files selected:', files.length);
        if (files.length > 0) {
            console.log('Processing file:', files[0].name);
            handleFile(files[0]);
        }
    });
} else {
    console.error('fileInput element not found!');
}

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