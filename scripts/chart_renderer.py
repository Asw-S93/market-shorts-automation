import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import os
from datetime import datetime

def generate_market_chart(symbol, data_points, output_path):
    """
    Generates a high-quality dark-themed candlestick/line chart for Shorts.
    1080x1920 (9:16) aspect ratio.
    """
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100)
    
    # Mock data for visualization
    df = pd.DataFrame(data_points)
    
    # Smooth line with glow effect
    ax.plot(df['time'], df['price'], color='#00ff9d', linewidth=6, alpha=0.9, zorder=3)
    ax.fill_between(df['time'], df['price'], color='#00ff9d', alpha=0.15)
    
    # Levels (Support/Resistance)
    ax.axhline(y=22300, color='#ff4444', linestyle='--', linewidth=2, label='Support')
    ax.axhline(y=22600, color='#44ff44', linestyle='--', linewidth=2, label='Resistance')

    # Styling
    ax.set_title(f"{symbol} ANALYSIS", fontsize=50, pad=60, color='white', fontweight='black')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#333333')
    ax.spines['bottom'].set_color('#333333')
    
    ax.tick_params(axis='both', which='major', labelsize=20, colors='#888888')
    
    plt.grid(color='#222222', linestyle='-', alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', facecolor='black')
    plt.close()

if __name__ == "__main__":
    # Test generation
    mock_data = {
        'time': range(20),
        'price': np.random.randint(22000, 22600, 20)
    }
    os.makedirs("/home/devone/.openclaw/workspace/market-shorts-automation/output/charts", exist_ok=True)
    generate_market_chart("NIFTY 50", mock_data, "/home/devone/.openclaw/workspace/market-shorts-automation/output/charts/test_chart.png")
