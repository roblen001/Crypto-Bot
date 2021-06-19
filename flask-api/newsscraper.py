import requests
from csv import writer
import json
# import pandas as pd
import csv
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from datetime import datetime
import nltk

# TODO:
# -Add this to a helper function file
# -Clean this page
# -This will run forever if the csv files are empty: wont be to go up to the most recent article
# -Get selenium to not open up a webdriver ui
# -Get selenium to stop when it is done (the terminal keeps running for no reason)
# -Opens up two different webdrivers for some reason


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def newsscraper(type):
    print('scraper online:', type)
    # will scrape the top or latest news and store values in different datasets (top or latest)
    #  FOR TOP NEWS ====================================================================
    if type == 'top':
        URL = 'https://cryptonews.net/en/news/top/'

        driver = webdriver.Chrome('/usr/bin/chromedriver')
        driver.get(URL)

        time.sleep(3)
        previous_height = driver.execute_script(
            'return document.body.scrollHeight')

        i = 0
        #  change the i value to get more data
        #  TODO: this loop will run till it reaches the point to which it already has in the data base

        df = pd.read_csv('../topNews.csv')
        df_firstn = df.tail(1)
        uptodate = False
        while uptodate == False:
            while i < 1:
                i += 1
                driver.execute_script(
                    'window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(3)
                new_height = driver.execute_script(
                    'return document.body.scrollHeight')
                if new_height == previous_height:
                    break
                previous_height = new_height

            #  WEB SCRAPING
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

            page = requests.get(URL, headers=headers)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            titleList = []
            linkList = []
            dateList = []
            for element in soup.find_all("div", {"class": "row news-item start-xs"}):
                titleList.append(element['data-title'])
                linkList.append(element['data-link'])
                for date in element.find_all("span", {"class": "datetime flex middle-xs"}):
                    #  if date is h then it is the current date
                    if "h" in date.getText():
                        timestamp = datetime.today().strftime('%d-%m')
                        dateList.append(timestamp)
                    else:
                        partitioned_date = date.getText().strip().partition('.')
                        day = partitioned_date[0]
                        partitioned_monthAndTime = partitioned_date[2].partition(
                            ',')
                        month = partitioned_monthAndTime[0]
                        timestamp = day + "-" + month
                        dateList.append(timestamp)

            # Scraping individual articles for the text it contains
            #  Should I be scraping list elements too
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

            textList = []
            for url in linkList:
                page = requests.get(url, headers=headers)

                soup = BeautifulSoup(page.content, 'html.parser')

                article = ""
                for p in soup.find_all("p"):
                    article += p.getText()
                textList.append(article)

            #  creating the dataframe
            df = pd.DataFrame(list(zip(titleList, linkList, dateList, textList)),
                              columns=['title', 'link', 'date', 'article'])

            # check if title has already been scraped if not then continue to scrape
            for idx in range(len(df['title'])):
                if df['title'][idx] == df_firstn.iloc[0]['title']:
                    uptodate = True
                    new_df = df.head(idx)
                    reversed_df = new_df.iloc[::-1]
                    reversed_df.to_csv(
                        '../topNews.csv', mode='a', header=False, index=False)
                    driver.quit()

    # FOR LATEST NEWS ============================================
    elif type == 'latest':
        URL = 'https://cryptonews.net/en/'

        driver = webdriver.Chrome('/usr/bin/chromedriver')
        driver.get(URL)

        time.sleep(3)
        previous_height = driver.execute_script(
            'return document.body.scrollHeight')

        i = 0
        #  change the i value to get more data
        #  TODO: this loop will run till it reaches the point to which it already has in the data base
        # with open('../topNews.csv', newline='') as f:
        #     reader = csv.reader(f)
        #     first_row = next(reader)
        #     print(first_row)
        df = pd.read_csv('../allNews.csv')
        df_firstn = df.tail(1)

        #  TODO: this loop will run till it reaches the point to which it already has in the data base
        uptodate = False
        while uptodate == False:
            while i < 1:
                i += 1
                driver.execute_script(
                    'window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(3)
                new_height = driver.execute_script(
                    'return document.body.scrollHeight')
                if new_height == previous_height:
                    break
                previous_height = new_height

            #  WEB SCRAPING
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

            page = requests.get(URL, headers=headers)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            titleList = []
            linkList = []
            dateList = []
            for element in soup.find_all("div", {"class": "row news-item start-xs"}):
                titleList.append(element['data-title'])
                linkList.append(element['data-link'])
                for date in element.find_all("span", {"class": "datetime flex middle-xs"}):
                    #  if date is h then it is the current date
                    if "h" in date.getText():
                        timestamp = datetime.today().strftime('%d-%m')
                        dateList.append(timestamp)
                    else:
                        partitioned_date = date.getText().strip().partition('.')
                        day = partitioned_date[0]
                        partitioned_monthAndTime = partitioned_date[2].partition(
                            ',')
                        month = partitioned_monthAndTime[0]
                        timestamp = day + "-" + month
                        dateList.append(timestamp)

            # Scraping individual articles for the text it contains
            #  Should I be scraping list elements too
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

            textList = []
            for url in linkList:
                page = requests.get(url, headers=headers)

                soup = BeautifulSoup(page.content, 'html.parser')

                article = ""
                for p in soup.find_all("p"):
                    article += p.getText()
                textList.append(article)

            #  creating the dataframe
            df = pd.DataFrame(list(zip(titleList, linkList, dateList, textList)),
                              columns=['title', 'link', 'date', 'article'])

            # check if title has already been scraped if not then continue to scrape
            for idx in range(len(df['title'])):
                if df['title'][idx] == df_firstn.iloc[0]['title']:
                    uptodate = True
                    new_df = df.head(idx)
                    reversed_df = new_df.iloc[::-1]
                    reversed_df.to_csv(
                        '../allNews.csv', mode='a', header=False, index=False)
                    driver.quit()

    return print('scraping up to date')
