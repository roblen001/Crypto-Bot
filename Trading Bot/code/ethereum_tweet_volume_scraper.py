import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def parse_strlist(sl):
    clean = re.sub("[\[\],\s]", "", sl)
    splitted = re.split("[\'\"]", clean)
    values_only = [s for s in splitted if s != '']
    return values_only


url = 'https://bitinfocharts.com/comparison/tweets-eth.html#alltime'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

scripts = soup.find_all('script')
for script in scripts:
    if 'd = new Dygraph(document.getElementById("container")' in str(script):
        StrList = str(script)
        StrList = '[[' + StrList.split('[[')[-1]
        StrList = StrList.split(']]')[0] + ']]'
        StrList = StrList.replace("new Date(", '').replace(')', '')
        dataList = parse_strlist(StrList)

date = []
tweet = []
for each in dataList:
    if (dataList.index(each) % 2) == 0:
        date.append(each)
    else:
        tweet.append(each)

df = pd.DataFrame(list(zip(date, tweet)), columns=["Date", "Decred - Tweets"])
df.to_csv(
    'E:/TweetVolume.csv', mode='a', header=False, index=False)
