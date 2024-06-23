"""Activate trading bot. In a seperate file to run as a subprocess.
"""

import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root / 'src'))

from trading_bot.trading_bot import bot

def run_trading_bot():
    """Runs the trading bot."""
    bot()

if __name__ == "__main__":
    run_trading_bot()
