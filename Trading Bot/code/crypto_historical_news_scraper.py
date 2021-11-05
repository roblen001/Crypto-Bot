from os import link
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
# import pandas as pd
import csv
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from datetime import datetime
import nltk
from newspaper import Article
import time

driver = webdriver.Chrome(ChromeDriverManager().install())

#  WEB SCRAPING
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

# changes url to get to the next page


def nextPage(iter):
    if iter == 1:
        URL = 'https://cryptonews.net/en/'
    else:
        URL = 'https://cryptonews.net/en/' + 'page-' + str(iter)
    return URL

# get the data from a page


def getData(url, headers, driver):
    driver.get(url)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

# organize data from the page


def organizeData(soup):
    titleList = []
    linkList = []
    dateList = []
    for element in soup.find_all("div", {"class": "row news-item start-xs"}):
        titleList.append(element['data-title'])
        linkList.append(element['data-link'])
        for date in element.find_all("span", {"class": "datetime flex middle-xs"}):
            #  if date is h then it is the current date
            if "h" in date.getText() and "March" not in date.getText():
                timestamp = datetime.today().strftime('%m-%d')
                dateList.append(timestamp)
            else:
                partitioned_date = date.getText().strip().partition('.')
                day = partitioned_date[0]
                partitioned_monthAndTime = partitioned_date[2].partition(',')
                month = partitioned_monthAndTime[0]
                timestamp = day + "-" + month
                dateList.append(timestamp)
    return titleList, linkList, dateList,


# get data from individual articles


def getArticleData(linkList, headers):
    textList = []
    for url in linkList:
        # check if link is broken prior to attempting to access it
        try:
            statusCode = requests.get(
                url, headers=headers, allow_redirects=False).status_code
        except requests.exceptions.ConnectionError:
            print('here ==============')
            statusCode = "Connection refused"
        print(url)
        print(statusCode)
        if statusCode == 200 and statusCode != "Connection refused":
            # if status code not 200 then go to next item (write broken for text?)
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')

            article = ""
            for p in soup.find_all("p"):
                article += p.getText()
            textList.append(article)
        else:
            textList.append('Broken Link')
    return textList


i = 1337
# increase the value of i to scrape more pages
while i != 1512:
    # after every 10 pages sleep for a minute
    time.sleep(10)
    if i % 10 == 0:
        # Try closing and reopening the page and continuing where you had left off
        driver.quit()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        print(i)
        URL = nextPage(i)
        soup = getData(URL, headers, driver)
        titleList, linkList, dateList, = organizeData(soup)
        textList = getArticleData(linkList, headers)
        df = pd.DataFrame(list(zip(titleList, linkList, dateList, textList)),
                          columns=['title', 'link', 'date', 'article'])
        df.to_csv(
            'E:/MissingNews.csv', mode='a', header=False, index=False)
        i += 1
    else:
        print(i)
        URL = nextPage(i)
        soup = getData(URL, headers, driver)
        titleList, linkList, dateList, = organizeData(soup)
        textList = getArticleData(linkList, headers)
        df = pd.DataFrame(list(zip(titleList, linkList, dateList, textList)),
                          columns=['title', 'link', 'date', 'article'])
        df.to_csv(
            'E:/MissingNews.csv', mode='a', header=False, index=False)
        i += 1
# i need to see if itll keep adding to the df or if I need to
# add it to the csv as we go or if that can just be done at the end
