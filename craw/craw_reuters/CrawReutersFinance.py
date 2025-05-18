"""
# Time  : 2025/3/26 21:06
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


def get_published_time(time_element):
    # published_time
    if time_element:
        published_time = time_element.get('datetime')
    else:
        published_time = "None"
    return published_time


def get_author(author_links):
    # author
    author_name = ""
    if author_links:
        # 为Reuters
        author_span = author_links.find("span",class_='text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__tag_label__6ajML')
        if author_span:
            author_name += author_span.get_text(strip=True)
            author_name += ", "
        else:
            author_a_list = author_links.find_all('a', rel='author')
            for link in author_a_list:
                author_name += link.get_text()
                author_name += ", "
    else:
        author_name += "None"
        author_name += ", "
    author_name = author_name[:-2]
    return author_name


def get_content(article_soup):
    #if summary li
    #text__text__1FZLe text__dark-grey__3Ml43 text__regular__2N1Xr text__small__1kGq2 body__base__22dCE body__small_body__2vQyf summary__point__NO-2F
    summary_content = ""
    li_tags = article_soup.find_all('li',class_='text__text__1FZLe text__dark-grey__3Ml43 text__regular__2N1Xr text__small__1kGq2 body__base__22dCE body__small_body__2vQyf summary__point__NO-2F')
    if li_tags:
        summary_content +=  " article summary \n"
        for li in li_tags:
            summary_content += li.get_text() + '\n'
            # print(li.get_text())

    article_content = ""
    article_body_div = article_soup.find_all('div', class_='text__text__1FZLe text__dark-grey__3Ml43 text__regular__2N1Xr text__small__1kGq2 body__full_width__ekUdw body__small_body__2vQyf article-body__paragraph__2-BtD')
    if article_body_div:
        for paragraph in article_body_div:
                article_content += paragraph.get_text().strip() + '\n'
                # print(p.get_text())

    # 去除最后一个多余的换行符
    article_content = article_content.rstrip()
    content = summary_content + article_content
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
    title_tag = article_soup.find('h1', class_='text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_article__3WgTF heading__base__2T28j heading__heading_article__2uc0a headline__headline__3kky1')
    title = get_title(title_tag)
    # published_time
    time_element = article_soup.find('time', class_='text__text__1FZLe text__dark-grey__3Ml43 text__regular__2N1Xr text__extra_small__1Mw6v body__base__22dCE body__extra_small_body__3QTYe')
    published_time = get_published_time(time_element)
    chinese_publish_time = get_chinese_time(published_time)
    # author
    author_links = article_soup.find('div', class_='text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__tag_label__6ajML')
    author_name = get_author(author_links)
    # content
    content = get_content(article_soup)
    article_data = {
        'headline': title,
        'published_time': published_time,
        'chinese_publish_time': chinese_publish_time,
        'author': author_name,
        'url': article_url,
        'source': "Reuters",
        'content': content
    }
    load_craw_data(title, save_dir, article_data, index_file, article_url)
    return article_data


def get_article_url(index_file,headers,proxy):
    url = 'https://www.reuters.com/business/finance/'
    response = requests.get(url, headers=headers, proxies=proxy)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_links_tag = soup.find_all('div', class_='media-story-card__body__3tRWy')
    url_list = read_index(index_file)
    print("reuters url_index is ", url_list)
    article_links_list = []
    #get topic news url
    for link_tag in article_links_tag:
        h3 = link_tag.find('h3')
        if h3:
            link = h3.find('a')
            href = "https://www.reuters.com"+link.get('href')
            if href in url_list:
                print(f"reuters {href} 已存在")
                continue
            article_links_list.append(href)
    #get common news url
    for link_tag in article_links_tag:
        link = link_tag.find('a', class_="text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_6__1qUJ5 heading__base__2T28j heading__heading_6__RtD9P media-story-card__headline__tFMEu")
        if link:
            href = "https://www.reuters.com"+link.get('href')
            if href in url_list:
                print(f"reuters {href} 已存在")
                continue
            article_links_list.append(href)

    return article_links_list


def craw_reuters_finance():
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    proxy = {
            'http': 'http://127.0.0.1:7897',
            'https': 'http://127.0.0.1:7897'
        }
    index_file = "G:/biyesheji/financial_RAG/craw/craw_reuters/reuters_finance_milvus_index.txt"
    save_dir = "G:/biyesheji/financial_RAG/craw/craw_reuters/reuters_finance2"
    article_links_list = get_article_url(index_file,headers,proxy)
    # print("reuters article_links_list is ",article_links_list)
    # print("article_links_list ",len(article_links_list),article_links_list)
    number = 1
    # reuters_all_data = []
    for article_url in article_links_list:
        article_data = get_article_detail(article_url,save_dir,headers,proxy,index_file)
        # reuters_all_data.append(article_data)
        # print(f"Reuters 已保存第 {number} 篇文章: {article_url}")
        number += 1
        yield article_data
    # print("Reuters 爬取成功！")
    # return reuters_all_data


# craw_reuters_finance()


# <ul>  class="story-collection__one_hero_and_one_column__XqWrc story-collection__list__2M49i story-collection__with-hero__3pzaT"
#
# div  class ="media-story-card__body__3tRWy" 下面，data-testid="Heading"的<h3>,下面data-testid="Link"的<a>,取其中的href

#作者 div的text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__tag_label__6ajML下面，可能是span，也可能是a
#找class为它的span 或者


