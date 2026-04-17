import cv2
import numpy as np
import pandas as pd
from pathlib import Path

class MarketRenderer:
    def __init__(self, width=1080, height=1920):
        self.width = width
        self.height = height
        self.fps = 30
        self.bg_color = (15, 15, 15)  # Darker gray

    def create_frame(self, data, frame_idx, total_frames):
        frame = np.full((self.height, self.width, 3), self.bg_color, dtype=np.uint8)
        
        # 1. Header (Motion)
        cv2.putText(frame, "DAILY MARKET UPDATE", (100, 150), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4, cv2.LINE_AA)
        
        # 2. Main Chart Area (Animated Line)
        chart_top, chart_bottom = 400, 1200
        chart_left, chart_right = 100, 980
        
        # Draw axes
        cv2.line(frame, (chart_left, chart_bottom), (chart_right, chart_bottom), (50, 50, 50), 2)
        
        prices = data['prices']
        n_points = len(prices)
        current_points = int((frame_idx / total_frames) * n_points)
        if current_points < 2: current_points = 2
        
        # Normalize prices
        min_p, max_p = min(prices), max(prices)
        def scale_y(p):
            return int(chart_bottom - (p - min_p) / (max_p - min_p) * (chart_bottom - chart_top))
        
        def scale_x(i):
            return int(chart_left + (i / (n_points - 1)) * (chart_right - chart_left))

        # Draw Glow Line
        pts = []
        for i in range(current_points):
            pts.append([scale_x(i), scale_y(prices[i])])
        
        pts = np.array(pts, np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], False, (157, 255, 0), 6, cv2.LINE_AA) # Neon Green
        
        # 3. Floating Stats with shadow for readability
        shadow_color = (0, 0, 0)
        text_color = (157, 255, 0)
        cv2.putText(frame, f"NIFTY: {data['current_price']}", (104, 304), 
                    cv2.FONT_HERSHEY_SIMPLEX, 3, shadow_color, 6, cv2.LINE_AA)
        cv2.putText(frame, f"NIFTY: {data['current_price']}", (100, 300), 
                    cv2.FONT_HERSHEY_SIMPLEX, 3, text_color, 6, cv2.LINE_AA)
        
        return frame

    def render_video(self, data, output_path):
        # Using H.264 via ffmpeg command for better compatibility
        temp_avi = str(output_path).replace('.mp4', '_temp.avi')
        
        # First write as AVI (uncompressed/raw)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(temp_avi, fourcc, self.fps, (self.width, self.height))
        
        total_frames = 150  # 5 seconds
        for i in range(total_frames):
            frame = self.create_frame(data, i, total_frames)
            out.write(frame)
        
        out.release()
        
        # Convert to H.264 MP4 using ffmpeg
        import subprocess
        ffmpeg_cmd = [
            'ffmpeg', '-y', '-i', temp_avi,
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-pix_fmt', 'yuv420p',  # Required for browser compatibility
            str(output_path)
        ]
        subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
        
        # Cleanup temp file
        import os
        os.remove(temp_avi)

if __name__ == "__main__":
    renderer = MarketRenderer()
    mock_data = {
        'prices': np.random.randint(22000, 22600, 50).tolist(),
        'current_price': "22,453"
    }
    renderer.render_video(mock_data, "/home/devone/.openclaw/workspace/market-shorts-automation/output/videos/render_test.mp4")
