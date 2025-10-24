"""
ZIP Report Generator
Packages complete detection results into a ZIP archive
"""

import zipfile
import json
from pathlib import Path
from typing import List


class ZIPReportGenerator:
    """Generates ZIP archive of detection results"""

    def __init__(self, job_dir: Path):
        self.job_dir = Path(job_dir)

    def generate_report(self, include_video: bool = True) -> str:
        """
        Generate ZIP archive containing all job artifacts

        Args:
            include_video: Whether to include the original video (can be large)

        Returns:
            Path to generated ZIP file
        """
        output_path = self.job_dir / "report.zip"

        # Files to include
        files_to_zip = []

        # Always include metadata
        try:
            if (self.job_dir / "metadata.json").exists():
                files_to_zip.append(("metadata.json", self.job_dir / "metadata.json"))
        except Exception as e:
            print(f"Warning: Failed to add metadata.json: {e}")

        # Include timeline data
        try:
            if (self.job_dir / "timeline.json").exists():
                files_to_zip.append(("timeline.json", self.job_dir / "timeline.json"))
        except Exception as e:
            print(f"Warning: Failed to add timeline.json: {e}")

        # Include PDF report
        try:
            if (self.job_dir / "report.pdf").exists():
                files_to_zip.append(("report.pdf", self.job_dir / "report.pdf"))
        except Exception as e:
            print(f"Warning: Failed to add report.pdf: {e}")

        # Include progress log
        try:
            if (self.job_dir / "progress.json").exists():
                files_to_zip.append(("progress.json", self.job_dir / "progress.json"))
        except Exception as e:
            print(f"Warning: Failed to add progress.json: {e}")

        # Include original video if requested
        if include_video:
            try:
                video_files = list(self.job_dir.glob("input.*"))
                if video_files:
                    video_file = video_files[0]
                    files_to_zip.append((video_file.name, video_file))
            except Exception as e:
                print(f"Warning: Failed to add video file: {e}")

        # Include heatmaps (TruFor)
        try:
            heatmap_dir = self.job_dir / "heatmaps"
            if heatmap_dir.exists():
                for heatmap_file in heatmap_dir.glob("*.png"):
                    files_to_zip.append((f"heatmaps/{heatmap_file.name}", heatmap_file))
        except Exception as e:
            print(f"Warning: Failed to add heatmaps: {e}")

        # Include keyframes (DeepfakeBench)
        try:
            keyframe_dir = self.job_dir / "keyframes"
            if keyframe_dir.exists():
                keyframes = list(keyframe_dir.glob("*.jpg")) + list(keyframe_dir.glob("*.png"))
                for kf in keyframes[:5]:  # Limit to first 5 keyframes
                    files_to_zip.append((f"keyframes/{kf.name}", kf))
        except Exception as e:
            print(f"Warning: Failed to add keyframes: {e}")

        # Include generated charts
        try:
            for chart_file in ["timeline_chart.png", "score_distribution.png"]:
                chart_path = self.job_dir / chart_file
                if chart_path.exists():
                    files_to_zip.append((f"charts/{chart_file}", chart_path))
        except Exception as e:
            print(f"Warning: Failed to add charts: {e}")

        # Create ZIP archive
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for arcname, filepath in files_to_zip:
                try:
                    zipf.write(filepath, arcname=arcname)
                except Exception as e:
                    print(f"Warning: Failed to write {arcname} to ZIP: {e}")

            # Add a README
            try:
                readme_content = self._generate_readme()
                zipf.writestr("README.txt", readme_content)
            except Exception as e:
                print(f"Warning: Failed to add README: {e}")

        return str(output_path)

    def _generate_readme(self) -> str:
        """Generate README content for ZIP archive"""
        readme = """
Deepfake Detection Report Package
==================================

This archive contains the complete results of a deepfake detection analysis.

Contents:
---------
- metadata.json: Job information and detection results
- timeline.json: Frame-by-frame analysis timeline (DeepfakeBench)
- report.pdf: Comprehensive PDF report with visualizations
- input.*: Original video file (if included)
- heatmaps/: Forensic heatmap images (TruFor)
- keyframes/: Extracted keyframes from suspicious segments
- charts/: Generated visualization charts

File Descriptions:
------------------
metadata.json:
  Contains job ID, username, detection type, model used, timestamps,
  and overall detection verdict and score.

timeline.json:
  Contains frame-by-frame scores and suspicious segment information
  for video analysis using DeepfakeBench models.

report.pdf:
  Human-readable comprehensive report including:
  - Job information
  - Detection results summary
  - Timeline visualization
  - Score distribution
  - Segment details
  - Forensic heatmaps

For more information, visit:
https://github.com/your-repo/deepfake-detector

Generated by Deepfake Detection System
"""
        return readme.strip()


def generate_zip_report(job_dir: str, include_video: bool = True) -> str:
    """
    Convenience function to generate ZIP report

    Args:
        job_dir: Path to job directory
        include_video: Whether to include the original video

    Returns:
        Path to generated ZIP file
    """
    generator = ZIPReportGenerator(job_dir)
    return generator.generate_report(include_video=include_video)
