"""Scrape the all news. Seperate file to run as a subprocess
"""

import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root / 'src'))

from data_handler.crypto_news_scraper import CryptoNewsScraper
import time

def run_all_news_scraper():
    """Scrapes latest news every 15 minutes."""
    scraper = CryptoNewsScraper()
    while True:
        try:
            scraper.get_crypto_news('latest')
            time.sleep(900)
        except:
            raise RuntimeError('failed to start news scraper for latest news')

if __name__ == "__main__":
    run_all_news_scraper()
