# Test Video Analysis API
# This script tests the video analysis endpoint

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Testing Video Analysis API" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if service is running
Write-Host "1. Checking if service is running..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "   ✓ Service is running: $($health.service)" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Service is not running!" -ForegroundColor Red
    Write-Host "   Please start the service with: python scripts/start_trufor.py" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check for test video
Write-Host "2. Looking for test video..." -ForegroundColor Yellow

$testVideo = $null
if (Test-Path "data\jobs") {
    Get-ChildItem "data\jobs" -Directory | ForEach-Object {
        $videoPath = Join-Path $_.FullName "input.mp4"
        if (Test-Path $videoPath) {
            $testVideo = $videoPath
            Write-Host "   ✓ Found test video: $videoPath" -ForegroundColor Green
            $size = (Get-Item $videoPath).Length / 1MB
            Write-Host "   Size: $([math]::Round($size, 2)) MB" -ForegroundColor Gray
        }
    }
}

if (-not $testVideo) {
    Write-Host "   ! No test video found in data/jobs/" -ForegroundColor Yellow
    Write-Host "   You need to upload a video through the web interface first" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Or create a test video:" -ForegroundColor Cyan
    Write-Host "   1. Open http://localhost:8000 in your browser" -ForegroundColor White
    Write-Host "   2. Upload a video file" -ForegroundColor White
    Write-Host "   3. Run this script again" -ForegroundColor White
    exit 0
}

Write-Host ""

# Test video analysis endpoint
Write-Host "3. Testing video analysis endpoint..." -ForegroundColor Yellow

# Create multipart form data
$filePath = $testVideo
$fileName = Split-Path $filePath -Leaf

Write-Host "   Uploading: $fileName" -ForegroundColor Gray

try {
    # Read file
    $fileBytes = [System.IO.File]::ReadAllBytes($filePath)
    
    # Create boundary
    $boundary = [System.Guid]::NewGuid().ToString()
    
    # Create form data
    $LF = "`r`n"
    $bodyLines = (
        "--$boundary",
        "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`"",
        "Content-Type: video/mp4$LF",
        [System.Text.Encoding]::GetEncoding("iso-8859-1").GetString($fileBytes),
        "--$boundary--$LF"
    ) -join $LF
    
    # Send request
    $response = Invoke-RestMethod -Uri "http://localhost:8000/video/analyze" `
        -Method Post `
        -ContentType "multipart/form-data; boundary=$boundary" `
        -Body $bodyLines
    
    $jobId = $response.job_id
    Write-Host "   ✓ Video uploaded successfully!" -ForegroundColor Green
    Write-Host "   Job ID: $jobId" -ForegroundColor Cyan
    
} catch {
    Write-Host "   ✗ Upload failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Poll for results
Write-Host "4. Monitoring analysis progress..." -ForegroundColor Yellow
Write-Host ""

$maxAttempts = 60  # Wait up to 60 seconds
$attempt = 0

while ($attempt -lt $maxAttempts) {
    try {
        $status = Invoke-RestMethod -Uri "http://localhost:8000/video/jobs/$jobId/status" -Method Get
        
        $stage = $status.stage
        $progress = $status.progress
        $message = $status.message
        $jobStatus = $status.status
        
        Write-Host "   [$attempt/$maxAttempts] Status: $jobStatus | Progress: $progress% | $message" -ForegroundColor Gray
        
        if ($jobStatus -eq "completed") {
            Write-Host ""
            Write-Host "   ✓ Analysis completed!" -ForegroundColor Green
            
            # Get results
            $result = Invoke-RestMethod -Uri "http://localhost:8000/video/jobs/$jobId/result" -Method Get
            
            Write-Host ""
            Write-Host "   Results:" -ForegroundColor Cyan
            Write-Host "   - Video duration: $($result.video_duration)s" -ForegroundColor White
            Write-Host "   - Total clips analyzed: $($result.total_clips)" -ForegroundColor White
            Write-Host "   - Threshold: $([math]::Round($result.threshold, 4))" -ForegroundColor White
            Write-Host "   - Suspicious segments found: $($result.segments.Count)" -ForegroundColor White
            
            if ($result.segments.Count -gt 0) {
                Write-Host ""
                Write-Host "   Segments:" -ForegroundColor Yellow
                foreach ($seg in $result.segments) {
                    Write-Host "   - Segment $($seg.segment_id): $([math]::Round($seg.start_time, 1))s - $([math]::Round($seg.end_time, 1))s (score: $([math]::Round($seg.peak_score, 3)))" -ForegroundColor White
                }
            }
            
            break
        }
        
        if ($jobStatus -eq "error") {
            Write-Host ""
            Write-Host "   ✗ Analysis failed: $message" -ForegroundColor Red
            break
        }
        
        $attempt++
        Start-Sleep -Seconds 1
        
    } catch {
        Write-Host "   ✗ Error checking status: $($_.Exception.Message)" -ForegroundColor Red
        break
    }
}

if ($attempt -ge $maxAttempts) {
    Write-Host ""
    Write-Host "   ! Timeout waiting for analysis" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Test Complete" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

