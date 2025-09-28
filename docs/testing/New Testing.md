| User Story ID | User Story                                                                                                                                              | Given                                            | When                                          | Then                                                                            |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | --------------------------------------------- | ------------------------------------------------------------------------------- |
| 1             | As a field investigator, I want to upload an image for analysis so that I can quickly assess manipulation.                                              | I have a valid image file (.jpg, .png)           | I upload the file to the system               | I see anomaly heatmap, confidence map, and integrity score                      |
| 2             | As a field investigator, I want to toggle the heatmap overlay with a legend and threshold so that I can interpret suspicious regions.                   | An image has been analyzed                       | I toggle the overlay controls                 | I see the heatmap overlay on/off, with legend and threshold updates             |
| 3             | As a field investigator, I want to view a confidence map so that I can suppress false positives in low-confidence areas.                                | An image has been analyzed                       | I open the confidence map view                | I see a confidence map with tooltips explaining values                          |
| 4             | As a security officer, I want the tool to run only within secure offline environments so that sensitive media never leaves the lab.                     | The application is installed locally             | I launch the tool without internet connection | The system runs normally with no outbound calls                                 |
| 5             | As a lab analyst, I want to securely share reports with colleagues so that peer review is possible.                                                     | A report is available                            | I export or share the report                  | The report is encrypted and only shared via secure intranet                     |
| 6             | As a lab analyst, I want to export a human-readable report so that findings can be used in casework.                                                    | A file has been analyzed                         | I click “Export PDF/Doc”                      | A report downloads with original, heatmap, confidence, metadata, and parameters |
| 7             | As a lab analyst, I want to view file/device metadata so that provenance can inform decisions.                                                          | A file has metadata available                    | I open metadata view                          | EXIF/device/GPS metadata is displayed; missing fields show “N/A”                |
| 8             | As a CCTV reviewer, I want to upload a short video and get a timeline with flagged timestamps and key-frame snapshots so that I can triage efficiently. | I have a 2–3 min video                           | I upload the video                            | I see flagged timecodes and preview key frames on the timeline                  |
| 9             | As a CCTV reviewer, I want object persistence checks so that unusual disappearances/insertions are surfaced.                                            | I have uploaded a video with object manipulation | I run analysis                                | I see flagged events when objects disappear or reappear unnaturally             |
| 10            | As an investigator, I want progress indicators for large files so that I know the system is working.                                                    | I am uploading a large file                      | I view the upload/analysis screen             | I see progress bars and have cancel/retry options                               |
| 11            | As a lab admin, I want the tool to operate on modest hardware so that deployment is feasible in small labs.                                             | I run the tool on a standard lab PC (CPU only)   | I upload a file                               | The analysis completes with acceptable latency                                  |
| 12            | As an investigator, I want to batch multiple files so that I can run unattended analysis.                                                               | I have a batch of files                          | I upload multiple files                       | I see queue status, retry on failures, and summary after completion             |
| 13            | As a lab analyst, I want to switch models (e.g., TruFor/ResNet) so that I can choose the best method for a case.                                        | Multiple models are available                    | I select a model in settings                  | The chosen model runs and is shown in the UI/report                             |
| 14            | As a lab analyst, I want to save results under a named project so that I can retrieve them later.                                                       | I have created a project                         | I save analyzed results                       | The results are stored under the project and can be retrieved later             |


US-01 – Upload an image  
Result: Pass  
Evidence: Uploaded test.jpg → heatmap + confidence 85% + integrity shown. .exe rejected.  
  
  
US-02 – Toggle heatmap overlay  
Result: Pass  
Evidence: Overlay toggled on/off, threshold adjusted, legend displayed.  
  
  
US-03 – Confidence map  
Result: Fail  
  
  
US-04 – Offline environment  
Result: Pass  
Evidence: App launched offline, no outbound logs, analysis succeeded.  
  
  
US-05 – Securely share reports  
Result: Fail  
  
  
US-06 – Export human-readable report  
Result: Pass  
Evidence: Exported PDF contained original, heatmap, confidence, metadata.  
  
  
US-07 – Metadata view  
Result: Pass  
Evidence: Metadata shown, missing GPS handled with “N/A”.  
  
  
US-08 – Short video timeline  
Result: Pass  
Evidence: Video analyzed, flagged timestamps 0:35, 1:20 with snapshots.  
  
  
US-09 – Object persistence  
Result: Fail  
  
  
US-10 – Progress indicators  
Result: Pass  
Evidence: 1GB upload showed progress bar, cancel/retry worked.  
  
  
US-11 – Modest hardware  
Result: Pass  
Evidence: On 8GB RAM dual-core CPU, image processed in 2 min.  
  
  
US-12 – Batch multiple files  
Result: Fail  
  
  
US-13 – Switch models  
Result: Pass  
Evidence: Switched from ResNet → TruFor, UI/report updated.  
  
  
US-14 – Save results under project  
Result: Pass  
Evidence: Project “Case-X” created, results saved, later retrieved.  
  
  
| User Story ID | Test Type            | Execution Type | Objective                      | Setup                         | Pre-Conditions              | Notes                                                                                                                                                         |
| ------------- | -------------------- | -------------- | ------------------------------ | ----------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| US-01         | Functional           | Manual         | Verify upload & analysis works | System online, user logged in | Valid `.jpg` file available | 1. Open upload page<br>2. Select `test.jpg`<br>3. Click upload<br>4. Verify heatmap, confidence, integrity displayed<br>5. Try uploading `.exe` → error shown |
| US-02         | Functional           | Manual         | Verify overlay controls        | Visualization module enabled  | Image analyzed              | 1. Upload image<br>2. Enable overlay<br>3. Adjust threshold<br>4. Verify legend updates                                                                       |
| US-04         | Security/Functional  | Manual         | Verify offline functionality   | App installed locally         | Internet disconnected       | 1. Disconnect internet<br>2. Launch app<br>3. Upload file<br>4. Verify analysis completes                                                                     |
| US-06         | Functional           | Manual         | Verify report export           | Reporting module enabled      | File analyzed               | 1. Upload file<br>2. Run analysis<br>3. Export PDF<br>4. Verify includes original, heatmap, confidence, metadata                                              |
| US-07         | Functional           | Manual         | Verify metadata display        | Metadata module enabled       | File uploaded               | 1. Upload EXIF-enabled file<br>2. Check metadata fields<br>3. Upload file without metadata → “N/A”                                                            |
| US-08         | Functional           | Manual         | Verify timeline flags          | Video module enabled          | Short video available       | 1. Upload `clip.mp4`<br>2. Analyze<br>3. Check flagged timecodes<br>4. Preview key frames                                                                     |
| US-10         | Usability/Functional | Manual         | Verify progress indicators     | Large file ready              | App running                 | 1. Upload 1GB file<br>2. Watch progress bar<br>3. Cancel & retry                                                                                              |
| US-11         | Performance          | Manual         | Verify runs on modest hardware | 8GB RAM, dual-core CPU        | App installed               | 1. Run analysis<br>2. Confirm result ≤ 2 minutes                                                                                                              |
| US-13         | Functional           | Manual         | Verify model switching         | Multiple models installed     | ResNet + TruFor available   | 1. Open settings<br>2. Switch model<br>3. Upload file<br>4. Verify model listed in report                                                                     |
| US-14         | Functional           | Manual         | Verify saving under projects   | Project mgmt active           | User logged in              | 1. Create project “Case-X”<br>2. Upload & analyze<br>3. Save results<br>4. Retrieve later                                                                     |
