#!/usr/bin/env python3
import os
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime

# Setup
BASE_DIR = Path("/home/devone/.openclaw/workspace/market-shorts-automation")
SCRIPTS_DIR = BASE_DIR / "scripts"
OUTPUT_DIR = BASE_DIR / "output"
(OUTPUT_DIR / "temp").mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / "videos").mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MarketOrchestrator")

def run_step(command, description):
    logger.info(f"🚀 Starting: {description}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"❌ Failed: {description}\nError: {result.stderr}")
        return False
    logger.info(f"✅ Completed: {description}")
    return True

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Fetch Data
    import data_fetcher
    snapshot = data_fetcher.get_latest_market_snapshot()
    if not snapshot:
        logger.error("Failed to fetch market snapshot")
        return

    # 2. Generate Chart Visuals
    if not run_step(f"python3 {SCRIPTS_DIR}/chart_renderer.py", "Rendering dynamic charts"):
        return

    # 3. (Future) Generate Audio via ElevenLabs
    # run_step(f"python3 {BASE_DIR}/../youtube-shorts-automation/scripts/generate_voiceover_elevenlabs.py ...")

    # 3. Audio & Voiceover
    script_content = {
        "script": f"Nifty closed at {snapshot['indices']['NIFTY 50']['price']}. The trend is {snapshot['sentiment']}."
    }
    script_path = OUTPUT_DIR / "temp" / "script.json"
    with open(script_path, "w") as f:
        json.dump(script_content, f)

    audio_out = OUTPUT_DIR / "temp" / "voiceover.mp3"
    voice_script = BASE_DIR / "../youtube-shorts-automation/scripts/generate_voiceover_elevenlabs.py"
    
    if os.path.exists(voice_script):
        run_step(f"python3 {voice_script} --script-json {script_path} --output {audio_out}", "Generating ElevenLabs Voiceover")
    
    # 4. Motion Rendering
    if not run_step(f"python3 {SCRIPTS_DIR}/motion_renderer.py", "Rendering motion graphics"):
        return

    video_raw = OUTPUT_DIR / "videos" / "render_test.mp4"
    video_final = OUTPUT_DIR / "videos" / f"market_short_{timestamp}.mp4"
    
    # 5. Final FFmpeg Merge (Video + Audio)
    if os.path.exists(audio_out):
        ffmpeg_cmd = f"ffmpeg -y -i {video_raw} -i {audio_out} -c:v copy -c:a aac -shortest {video_final}"
    else:
        ffmpeg_cmd = f"cp {video_raw} {video_final}"
    
    run_step(ffmpeg_cmd, "Merging final short")
    
    logger.info(f"✅ Workflow complete: {video_final}")

if __name__ == "__main__":
    main()
