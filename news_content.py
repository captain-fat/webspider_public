import random
import time
import urllib.request
from bs4 import BeautifulSoup as bs
import re
import jieba
import pandas as pd
import numpy as np
import requests
import os


# read existed csv file
def read_news_detail_df(name):
    news_detail_df = pd.read_csv(name)
    news_detail_df_link = news_detail_df['link'].values.tolist()
    return news_detail_df, news_detail_df_link


# read existed news link
def read_existed_news_link(name):
    df_news_ = pd.read_csv(name)
    links_exist = df_news_['link'].values.tolist()
    return links_exist


# function to return html data according to url link
def return_html_content(num):
    url = "http://10.201.112.8" + num
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
    request = urllib.request.Request(url=url, headers=head)
    resp = urllib.request.urlopen(request)
    html_data = resp.read().decode('utf-8')
    return html_data


# function to parse html to dataframe
def parse_html_content(html, node_num):
    news_title = []
    news_publisher = []
    news_writer = []
    news_contents = []
    news_date = []
    news_category = []
    soup = bs(html, 'html.parser')
    news_title_ = soup.find_all('a', rel='bookmark')
    news_title.append(news_title_[0].text.strip())
    news_info_ = soup.find_all('div', class_='article-create-date')
    news_date_ = news_info_[0]
    news_date_ = news_date_.find_all('span')[1]
    for i in news_date_:
        news_date.append(i.text)
    news_publisher_ = news_info_[1].text.strip()
    news_publisher_ = re.sub('\xa0', '', news_publisher_)
    news_publisher.append(news_publisher_)
    news_writer_ = news_info_[2].text.strip()
    news_writer_ = re.sub('\xa0', '', news_writer_)
    news_writer.append(news_writer_)
    news_category_ = news_info_[3].text.strip()
    news_category_ = re.sub('\xa0', '', news_category_)
    news_category.append(news_category_)
    news_content_ = soup.find_all('p')
    for i in news_content_:
        string_ = i.text
        string_ = re.sub('\xa0', '', string_)
        news_contents.append(string_)
        news_content = ''.join(news_contents)
    news_detail_dict = {'title': news_title, 'date': news_date, 'publisher': news_publisher,
                        'writer': news_writer, 'category': news_category, 'content': news_content,
                        'link': node_num}
    news_df = pd.DataFrame(news_detail_dict)
    return news_df
    # return news_detail_dict


# function to download web images
def get_img(html, node_num):
    soup = bs(html, 'html.parser')
    all_links = soup.find_all('img')
    for i in range(2, len(all_links)):
        url = 'http://10.201.112.8' + all_links[i]['src']
        name = str(i - 1)
        path = "D:/download_image" + node_num + "/"
        if not os.path.exists(path):
            os.makedirs(path)
        urllib.request.urlretrieve(url, path + name + ".jpg")
        print("-----downloading-----" + node_num)
    print("----------done--------------")


# main program


def save_news_detail_df(news_detail_df):
    news_detail_df.to_csv('result_detail.csv', encoding='utf_8_sig', index=0)
