"""
# Time  : 2025/3/24 00:50
# Author: Hou Ly
"""

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from fake_useragent import UserAgent
from utile.GetChineseTime import get_chinese_time


def read_index(index_file):
    url_list = []
    with open(index_file, "a+", encoding="utf-8") as file:
        file.seek(0)
        for line in file:
            url = line.strip()
            if url:
                url_list.append(url)
    return url_list


def write_index(index_file, new_url):
    with open(index_file, "a", encoding="utf-8") as file:
        for url in new_url:
            file.write(url + "\n")


def get_title(title_tag):
    # title
    if title_tag:
        title = title_tag.get_text()
        # print(title)
    else:
        title = "None"
    return title


def get_published_time(time_div):
    # published_time
    if time_div:
        time_element = time_div.find('time')
        if time_element:
            published_time = time_element.get('datetime')[:-5]
            published_time += "Z"
        else:
            published_time = "None"
    else:
        published_time = "None"
    return published_time


def get_author(author_links):
    # author
    author_name = ""
    if author_links:
        for each_author in author_links:
            author_name += each_author.get_text(strip=True)
            author_name += ", "
    else:
        author_name+= "None"
        author_name += ", "
    author_name = author_name[:-2]
    return author_name


def get_content(article_soup):
    #if key
    key_content = ""
    key_div = article_soup.find('div', class_='RenderKeyPoints-list')
    if key_div:
        key_content += "key point \n"
        li_tags = key_div.find_all('li')
        for li in li_tags:
            key_content += li.get_text() + '\n'
            # print(li.get_text())

    article_content = ""
    article_body_div = article_soup.find('div', class_='ArticleBody-articleBody')
    if article_body_div:
        group_div = article_body_div.find('div', class_='group')
        if group_div:
            p_tags = group_div.find_all('p')
            for p in p_tags:
                article_content += p.get_text().strip() + '\n'
                # print(p.get_text())

    # 去除最后一个多余的换行符
    article_content = article_content.rstrip()
    content = key_content + article_content
    # print("key_content is",key_content)
    # print("article_content is", article_content)
    return content


def load_craw_data(title,save_dir,article_data,index_file,article_url):
    invalid_chars = r'[\\/*?:"<>|]'
    clean_title = re.sub(invalid_chars, '_', title)
    # 保存到文件
    with open(f"{save_dir}/{clean_title}.txt", "w", encoding="utf-8") as f:
        json_str = json.dumps(article_data, ensure_ascii=False, indent=4)
        f.write(json_str)
    with open(index_file, "a", encoding="utf-8") as file:
        file.write(article_url + "\n")


# 爬取每篇文章并存储到txt中
def get_article_detail(article_url,save_dir,headers,proxy,index_file):
    # print("article_url is ",article_url)
    # # 获取每篇文章的详细信息

    article_response = requests.get(article_url, headers=headers, proxies=proxy)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')
    # print(article_soup)
    # title
    title_tag = article_soup.find('h1', class_='ArticleHeader-headline')
    title = get_title(title_tag)
    # published_time
    time_div = article_soup.find('div', class_='ArticleHeader-timeHidden')
    published_time = get_published_time(time_div)
    chinese_publish_time = get_chinese_time(published_time)
    # author
    author_links = article_soup.find_all('a', class_='Author-authorName')
    author_name = get_author(author_links)
    # content
    content = get_content(article_soup)
    article_data = {
        'headline': title,
        'published_time': published_time,
        'chinese_publish_time': chinese_publish_time,
        'author': author_name,
        'url': article_url,
        'source': "CNBC",
        'content': content
    }
    load_craw_data(title, save_dir, article_data, index_file, article_url)
    return article_data

def get_article_url(index_file,headers,proxy):
    url = 'https://www.cnbc.com/finance/'
    # url = "https://www.cnbc.com/finance/?page=2"
    # print(url)
    response = requests.get(url, headers=headers, proxies=proxy)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_links = soup.find_all('a', class_='Card-title')
    article_links_list = []

    url_list = read_index(index_file)
    # print("CNBC Finance url_index is ",url_list)
    for link in article_links:
        href = link.get('href')
        if href in url_list:
            print(f"CNBC Finance {href} 已存在")
            continue
        article_links_list.append(href)
    return article_links_list


def craw_CNBC_finance():
    ua = UserAgent()
    # 随机生成 User-Agent
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    proxy = {
            'http': 'http://127.0.0.1:7897',
            'https': 'http://127.0.0.1:7897'
        }
    save_dir = "G:/biyesheji/financial_RAG/craw/craw_CNBC/CNBC_finance_data2"
    index_file = "G:/biyesheji/financial_RAG/craw/craw_CNBC/CNBC_finance_milvus_index.txt"
    article_links_list = get_article_url(index_file,headers,proxy)
    # print("CNBC Finance article_links_tag is ", article_links_list)
    number = 1
    # cnbc_all_data = []
    for article_url in article_links_list:
        article_data = get_article_detail(article_url,save_dir,headers,proxy,index_file)
        # cnbc_all_data.append(article_data)
        # print(f"CNBC finance已保存第 {number} 篇文章: {article_url}")
        number += 1
        yield article_data
    # print("CNBC 爬取成功！")
    # return cnbc_all_data

# craw_CNBC_finance()
#
# ua = UserAgent()
# headers = {
#     "User-Agent": ua.random,
#     "Accept-Language": "en-US,en;q=0.9",
#     "Referer": "https://www.bloomberg.com/",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
# }
# proxy = {
#         'http': 'http://127.0.0.1:7897',
#         'https': 'http://127.0.0.1:7897'
#     }
# index_file = "G:/biyesheji/financial_RAG/craw/craw_CNBC/CNBC_finance_title_index2.txt"
# article_url = 'https://www.cnbc.com/2025/04/08/elon-musk-steps-up-attacks-on-navarro-as-tesla-shares-slump-fourth-day.html'
# get_article_detail(article_url,headers,proxy,index_file)