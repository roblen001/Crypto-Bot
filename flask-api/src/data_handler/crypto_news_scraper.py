"""Functions to scrape crypto news site. Requires chromedriver to run.
"""

import requests
from csv import writer
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime
import emoji
from datetime import datetime, timedelta
import time 

class CryptoNewsScraper:
    def __init__(self, webdriver_path: str = "../../chromedriver-win64/chromedriver"):
        self.webdriver_path = webdriver_path

    @staticmethod
    def append_list_as_row(file_name, list_of_elem):
        """
        Append a list as a row to a CSV file.
        
        Args:
            file_name (str): The name of the file to append to.
            list_of_elem (list): The list of elements to append.
        """
        with open(file_name, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(list_of_elem)

    @staticmethod
    def remove_emojis(text):
        """
        Remove all emojis from the input text.

        Args:
            text (str): The input text that may contain emojis.

        Returns:
            str: The text with all emojis removed.
        """
        return emoji.replace_emoji(text, replace='')

    @staticmethod
    def strip_whitespace(text):
        """
        Remove leading and trailing whitespace from the input text.

        Args:
            text (str): The input text that may contain leading or trailing whitespace.

        Returns:
            str: The text with leading and trailing whitespace removed.
        """
        return text.strip()

    @staticmethod
    def clean_text(text):
        """
        Clean the input text by removing emojis and stripping leading and trailing whitespace.

        Args:
            text (str): The input text to be cleaned.

        Returns:
            str: The cleaned text.
        """
        text_no_emojis = CryptoNewsScraper.remove_emojis(text)
        cleaned_text = CryptoNewsScraper.strip_whitespace(text_no_emojis)
        return cleaned_text

    def get_crypto_news(self, news_type, csv_file_path=None, time_limit=30):
        """
        Scrape news articles and store them in CSV files based on type (top or latest).

        Args:
            news_type (str): The type of news to scrape ('top' or 'latest').
            csv_file_path: if used then it overwrites the standard data storage paths
            time_limit: the max amount of time to scrape for news
        """
        print('scraper online:', news_type)

        if news_type == 'top':
            url = 'https://cryptonews.net/en/news/top/'
            csv_file = 'output_data/topNews.csv'
        elif news_type == 'latest':
            url = 'https://cryptonews.net/en/'
            csv_file = 'output_data/allNews.csv'
        else:
            raise ValueError("Invalid type specified. Must be 'top' or 'latest")
        
        if csv_file_path is not None:
            csv_file = csv_file_path

        driver = self.initialize_driver()
        driver.get(url)

        df = pd.read_csv(csv_file)
        df_firstn = df.tail(1)

        self._scrape_news(driver, df, df_firstn, csv_file, time_limit)

        driver.quit()
        print('scraping completed')

    def initialize_driver(self):
        """
        Initialize the WebDriver.

        Returns:
            webdriver.Chrome: The initialized WebDriver.
        """
        try:
            driver = webdriver.Chrome(self.webdriver_path)
            return driver
        except Exception as e:
            raise FileNotFoundError(f"Make sure you installed chrome webdriver and you are pointing to the correct path. "
                                    f"newsscraper is currently looking at {self.webdriver_path} for the webdriver")

    def _scrape_news(self, driver, df, df_firstn, csv_file, time_limit):
        """
        Scrape the news articles from the webpage.

        Args:
            driver (webdriver.Chrome): The WebDriver instance.
            df (DataFrame): The existing news data.
            df_firstn (DataFrame): The first row of the existing news data.
            csv_file (str): The path to the CSV file to save the news data.
            time_limit: the max amount of time to scrape for news
        """
        end_time = datetime.now() + timedelta(minutes=time_limit)

        future = datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
        while now < future:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(3)
                        
            try:
                show_more_button = driver.find_element_by_id("show-more")
                show_more_button.click()
            except Exception as e:
                print("No 'Show more' button found or unable to click:", e)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            title_list, link_list, date_list, text_list = self._extract_news_data(soup)

            df = pd.DataFrame(list(zip(title_list, link_list, date_list, text_list)),
                              columns=['title', 'link', 'date', 'article'])

            for idx in range(len(df['title'])):
                if len(df_firstn) > 0:
                    if self.clean_text(df['title'][idx]) == self.clean_text(df_firstn.iloc[0]['title']):
                        new_df = df.head(idx+1)
                        reversed_df = new_df.iloc[::-1]
                        reversed_df.to_csv(csv_file, mode='a', header=False, index=False)
                        return
                else:
                    df_firstn = df

        # if the time limit is reached then stop and save
        reversed_df = df.iloc[::-1]
        reversed_df.to_csv(csv_file, mode='a', header=False, index=False)

    def _extract_news_data(self, soup):
        """
        Extract news data from the BeautifulSoup object.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the webpage content.

        Returns:
            list: Lists of news titles, links, dates, and articles.
        """
        title_list = []
        link_list = []
        date_list = []
        text_list = []

        for element in soup.find_all("div", {"class": "row news-item start-xs"}):
            if not element.has_attr('data-article-id'):
                continue
            title_list.append(element.find(class_='title').get_text())
            link_list.append(element['data-link'])

            for date in element.find_all("span", {"class": "datetime flex middle-xs"}):
                if "h" in date.getText():
                    timestamp = datetime.today().strftime('%d-%m')
                    date_list.append(timestamp)
                else:
                    partitioned_date = date.getText().strip().partition('.')
                    day = partitioned_date[0]
                    partitioned_month_and_time = partitioned_date[2].partition(',')
                    month = partitioned_month_and_time[0]
                    timestamp = day + "-" + month
                    date_list.append(timestamp)

        headers = {}
        for url in link_list:
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            article = ""
            for p in soup.find_all("p"):
                article += p.getText()
            text_list.append(article)

        return title_list, link_list, date_list, text_list
