import subprocess
import os
from pathlib import Path

def assemble_market_short(video_output, chart_image, audio_path, script_text):
    """
    Assembles the final video using FFmpeg with professional overlays.
    """
    # Background: Solid dark blue/black gradient or static image
    # For now, using a generated black background if no video provided
    
    # FFmpeg command for vertical shorts:
    # 1. Take a 9:16 background
    # 2. Overlay the chart image
    # 3. Add text overlays for support/resistance
    # 4. Sync with audio
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(chart_image),
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
        "-vf", (
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "drawtext=text='DAILY MARKET UPDATE':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=150:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf,"
            "drawtext=text='NIFTY 50':fontcolor='#00ff9d':fontsize=120:x=(w-text_w)/2:y=400:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        ),
        "-c:v", "libx264", "-t", "10", "-pix_fmt", "yuv420p", "-shortest",
        str(video_output)
    ]
    
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    BASE = Path("/home/devone/.openclaw/workspace/market-shorts-automation")
    assemble_market_short(
        BASE / "output/videos/market_test.mp4",
        BASE / "output/charts/test_chart.png",
        # Mock audio for testing if real one fails
        "/usr/share/sounds/alsa/Front_Center.wav", 
        "Nifty is looking bullish today."
    )
