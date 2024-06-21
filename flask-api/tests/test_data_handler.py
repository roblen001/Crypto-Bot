"""Test cases for the data handler

Might be fun to connect this to some new crypto site
"""
import pytest
from unittest.mock import patch, Mock
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from src.data_handler.crypto_news_scraper import CryptoNewsScraper

import pytest
from unittest.mock import patch, Mock
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from src.data_handler.crypto_news_scraper import CryptoNewsScraper

# Mock for selenium.webdriver.Chrome
class MockWebDriver:
    def __init__(self, *args, **kwargs):
        self.page_source = ''
    
    def get(self, url):
        if url == 'https://cryptonews.net/en/news/top/':
            self.page_source = """
            <html>
                <head>
                    <title>Mock News</title>
                </head>

                <body>
                    <div class="row news-item start-xs" data-article-id="1" data-link="https://example.com/news1">
                        <div class="title">News Title 1</div>
                        <span class="datetime flex middle-xs">12.06.2021, 14:00</span>
                    </div>
                </body>
            </html>
            """ 
    
    def execute_script(self, script):
        return 1000  # Mock page height

    def quit(self):
        pass

    def find_element_by_id(self, id):
        class MockElement:
            def click(self):
                pass
        return MockElement()

@pytest.fixture
def setup_env(tmpdir):
    tmpdir.mkdir('data')
    temp_data_dir = tmpdir.join('data')
    with open(temp_data_dir.join('topNews.csv'), 'w') as f:
        f.write('title,link,date,article\n')

    yield temp_data_dir

def test_append_list_as_row(setup_env):
    temp_data_dir = setup_env
    row = ['title', 'link', 'date', 'article']
    CryptoNewsScraper.append_list_as_row(temp_data_dir.join('topNews.csv'), row)
    df = pd.read_csv(temp_data_dir.join('topNews.csv'))
    assert len(df) == 1
    assert df.iloc[0]['title'] == 'title'

def test_remove_emojis():
    assert CryptoNewsScraper.remove_emojis('Hello 😊') == 'Hello '

def test_strip_whitespace():
    assert CryptoNewsScraper.strip_whitespace('  Hello  ') == 'Hello'

def test_clean_text():
    assert CryptoNewsScraper.clean_text('  Hello 😊  ') == 'Hello'

@patch('selenium.webdriver.Chrome', return_value=MockWebDriver())
def test_get_crypto_news(mock_get, setup_env):
    temp_data_dir = setup_env
    scraper = CryptoNewsScraper(webdriver_path='chromedriver')
    scraper.get_crypto_news('top', csv_file_path=temp_data_dir.join('topNews.csv'), time_limit=0.1)
    df = pd.read_csv(temp_data_dir.join('topNews.csv'))
    assert len(df) > 0  # Ensure data has been scraped

def test_extract_news_data():
    html_content = """
    <div class="row news-item start-xs" data-article-id="1" data-link="https://example.com/news1">
        <div class="title">News Title 1</div>
        <span class="datetime flex middle-xs">12.06.2021, 14:00</span>
    </div>
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    scraper = CryptoNewsScraper()
    title_list, link_list, date_list, text_list = scraper._extract_news_data(soup)

    assert len(title_list) == 1
    assert title_list[0] == "News Title 1"
    assert link_list[0] == "https://example.com/news1"
    assert date_list[0] == "12-06.2021"

@patch('selenium.webdriver.Chrome', return_value=MockWebDriver())
def test_initialize_driver(mock_webdriver):
    scraper = CryptoNewsScraper(webdriver_path='chromedriver')
    driver = scraper.initialize_driver()
    assert driver is not None


def test_live_usecase_news_scraper(setup_env):
    """Mocking is for the weak...
    """
    temp_data_dir = setup_env
    scraper = CryptoNewsScraper(webdriver_path='../chromedriver-win64/chromedriver')
    scraper.get_crypto_news('top', time_limit=0.05, csv_file_path=temp_data_dir.join('topNews.csv'))
    post_len = len(pd.read_csv(temp_data_dir.join('topNews.csv')))

    assert post_len > 0

    
