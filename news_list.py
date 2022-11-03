# import necessary packages
import random
import time
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup as bs


# input page number and then return html data responded from the url link
def return_html(num):
    url = "http://10.201.112.8/list/xinwen?page=" + num
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}

    request = urllib.request.Request(url=url, headers=head)
    resp = urllib.request.urlopen(request)
    html_data = resp.read().decode('utf-8')
    return html_data


# according to the returned html data to generate one dataframe to store information such as news title,
# news content, news writer and ect. and then return the dataframe
# print(html_data)
def parse_df(html):
    soup = bs(html, 'html.parser')
    news_title = soup.find_all('div', class_='views-field-title')
    news_content = soup.find_all('div', class_='views-field-body')
    news_writer = soup.find_all('span', class_='release-info-dept')
    news_date = soup.find_all('span', 'release-info-created')
    news_titles = []
    news_writers = []
    news_date_ = []
    news_content_ = []
    news_links = []
    for i in news_title:
        news_titles.append(i.text)
    for i in news_writer:
        news_writers.append(i.text.strip())
    for i in news_date:
        news_date_.append(i.text.strip())
    for i in news_content:
        news_content_.append(i.text)
    for i in news_title:
        news_links.append(i.find('a').get('href'))
    news_dict = {'title': news_titles, 'writer': news_writers, 'content': news_content_,
                 'date': news_date_, 'link': news_links}
    news_df = pd.DataFrame(news_dict)
    return news_df


# format new dataframe
def format_df():
    news_df_ = pd.DataFrame(columns=['title', 'writer', 'content', 'date', 'link'])
    return news_df_


# read exist csv to create one dataframe that can be compared with the new one, avoid duplicated data
def read_news_link_exist(name):
    df_exist = pd.read_csv(name)
    news_link_exist = df_exist['link'].values.tolist()
    return news_link_exist, df_exist


# main program to cycle from 0 to 85 to get the news list with information mentioned before


# concatenate exist df with new df and save it to csv file
def save_csv_file(news_df_, df_exist):
    news_df_ = pd.concat([news_df_, df_exist], axis=0)

    news_df_.to_csv('result.csv', encoding='utf_8_sig', index=0)
