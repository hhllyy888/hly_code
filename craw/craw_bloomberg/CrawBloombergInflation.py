"""
# Time  : 2025/3/22 11:12
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


def get_content(article_soup):
    body_content_div = article_soup.find('div', class_='body-content')
    if body_content_div:
        p_contents = [p.get_text(strip=True) for p in body_content_div.find_all('p')]
        article_content = "\n".join(p_contents)
    else:
        article_content = "None"
    return article_content


def get_article_url(url,headers,proxy,index_file):
    response = requests.get(url, headers=headers, proxies=proxy)
    soup = BeautifulSoup(response.text, 'html.parser')
    href_headline_list = []
    url_list = read_index(index_file)
    # 获取头号新闻
    top_links = soup.find_all('a', class_='StoryBlock_storyLink__5nXw8')
    for link in top_links:
        href = link.get('href')
        href = 'https://www.bloomberg.com' + href
        if href in url_list:
            print(f"bloomberg {href} 已存在")
            continue
        span = link.find('span')
        if span:
            headline = span.get_text()
            result_dict = {"url": href, "headline": headline}
            href_headline_list.append(result_dict)

    # 获取其他新闻
    others_links = soup.find_all('a', class_='LineupContentArchive_storyLink__Umeq4')
    for link in others_links:
        href = link.get('href')
        href = 'https://www.bloomberg.com' + href
        if href in url_list:
            print(f"bloomberg {href} 已存在")
            continue
        span = link.find('span')
        if span:
            headline = span.get_text()
            result_dict = {"url": href, "headline": headline}
            href_headline_list.append(result_dict)
    return href_headline_list


def load_craw_data(save_dir,title,article_data,index_file,article_url):
    invalid_chars = r'[\\/*?:"<>|]'
    clean_title = re.sub(invalid_chars, '_', title)
    # 保存到文件
    with open(f"{save_dir}/{clean_title}.txt", "w", encoding="utf-8") as f:
        json_str = json.dumps(article_data, ensure_ascii=False, indent=4)
        f.write(json_str)
    # print(f"{article_url}已保存")
    with open(index_file, "a", encoding="utf-8") as file:
        file.write(article_url + "\n")


def get_article_detail(href_headline,save_dir,index_file,headers,proxy):
    title = href_headline["headline"]
    article_url = href_headline['url']
    # print("article_url is ",article_url)
    # # 获取每篇文章的详细信息
    article_response = requests.get(article_url, headers=headers, proxies=proxy)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')
    # print(article_soup)
    time_tag = article_soup.find('time')
    if time_tag:
        date_time = time_tag.get('datetime')
        if "." in date_time:
            tmp_time_split = date_time.split(".")
            date_time = tmp_time_split[0]+tmp_time_split[1][-1]
    else:
        date_time = "None"
    # print("date_time is ", date_time)
    chinese_publish_time = get_chinese_time(date_time)
    author_links = article_soup.find_all('a', rel="author")
    # print(author_links)
    author_name = ""
    if author_links:
        for each_aothor in author_links:
            author_name += each_aothor.get_text(strip=True)
            author_name += ", "
        # print(author_name)
    else:
        author_name += "None"
        author_name += ", "
    author_name = author_name[:-2]
    content = get_content(article_soup)
    # 将数据保存到列表
    article_data = {
        'headline': title,
        'published_time': date_time,
        'chinese_publish_time':chinese_publish_time,
        'author': author_name,
        'url': article_url,
        'source': "Bloomberg",
        'content': content
    }
    load_craw_data(save_dir, title, article_data, index_file, article_url)
    return article_data


def craw_bloom_inflation():
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.bloomberg.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    proxy = {
            'http': 'http://127.0.0.1:7897',
            'https': 'http://127.0.0.1:7897'
        }
    url = 'https://www.bloomberg.com/economics/inflation-and-prices'
    index_file = "G:/biyesheji/financial_RAG/craw/craw_bloomberg/bloomberg_inflation_milvus_index.txt"
    href_headline_list = get_article_url(url, headers, proxy, index_file)
    # print("Bloomberg href_headline_list is ", href_headline_list)
    # href_headline_list = [{'href': '/news/articles/2025-03-21/fed-s-goolsbee-sees-transitory-inflation-from-one-time-tariffs?srnd=phx-economics-inflation-and-prices', 'headline': 'Fed’s Goolsbee Sees Transitory Inflation From One-Time Tariffs'}, {'href': '/news/articles/2025-03-20/japan-s-inflation-slows-after-resumption-of-energy-subsidies?srnd=phx-economics-inflation-and-prices', 'headline': 'Japan’s Inflation Slows Less Than Expected, Backing BOJ Hikes'}, {'href': '/news/articles/2025-03-19/sweden-finance-minister-warns-inflation-will-miss-target-in-2025?srnd=phx-economics-inflation-and-prices', 'headline': 'Sweden Finance Chief Warns Inflation May Miss Target in 2025'}, {'href': '/news/articles/2025-03-19/south-african-inflation-steady-on-eve-of-expected-rate-pause?srnd=phx-economics-inflation-and-prices', 'headline': 'South African Inflation Steady on Eve of Expected Rate Pause'}, {'href': '/news/articles/2025-03-18/canada-inflation-quickens-to-2-6-on-end-of-sales-tax-break?srnd=phx-economics-inflation-and-prices', 'headline': 'Canada Inflation Quickens to 2.6% on End of Sales Tax Break'}, {'href': '/news/articles/2025-03-18/south-africa-s-power-cut-losses-plummet-83-as-supply-stabilizes?srnd=phx-economics-inflation-and-prices', 'headline': 'South Africa’s Power-Cut Losses Fall 83% as Supply Improves'}, {'href': '/news/articles/2025-03-17/nigerian-inflation-cools-again-amid-hope-prices-have-peaked?srnd=phx-economics-inflation-and-prices', 'headline': 'Nigerian Inflation Cools Again Giving Impetus for Rate Pause'}, {'href': '/news/articles/2025-03-14/ecb-s-villeroy-sees-victory-over-inflation-very-soon?srnd=phx-economics-inflation-and-prices', 'headline': 'ECB’s Villeroy Sees Victory Over Inflation ‘Very Soon’'}, {'href': '/news/articles/2025-03-14/german-inflation-revised-down-to-2-6-in-positive-sign-for-ecb?srnd=phx-economics-inflation-and-prices', 'headline': 'German Inflation Revised Down to 2.6% in Positive Sign for ECB'}, {'href': '/news/articles/2025-03-13/eu-egg-prices-soar-to-highest-in-over-a-decade-as-bird-flu-hits?srnd=phx-economics-inflation-and-prices', 'headline': 'EU Egg Prices Soar to Highest in Over a Decade as Bird Flu Hits'}, {'href': '/news/articles/2025-03-12/five-key-takeaways-from-the-us-cpi-report-for-february-toplive?srnd=phx-economics-inflation-and-prices', 'headline': 'Five Key Takeaways From the US CPI Report for February'}, {'href': '/news/articles/2025-03-12/us-inflation-comes-in-lower-than-forecast-offering-some-relief?srnd=phx-economics-inflation-and-prices', 'headline': 'US Inflation Eases, Offering Some Relief Ahead of Tariffs'}, {'href': '/news/articles/2025-03-12/india-inflation-eases-further-boosting-rate-cut-hopes?srnd=phx-economics-inflation-and-prices', 'headline': 'India’s Below-Target Inflation Boosts Case for Rate Cuts'}]
    # 存储新闻数据
    save_dir = "G:/biyesheji/financial_RAG/craw/craw_bloomberg/bloomberg_inflation2"
    number = 1
    # bloomberg_all_data = []
    for href_headline in href_headline_list:
        article_data = get_article_detail(href_headline,save_dir,index_file,headers,proxy)
        # bloomberg_all_data.append(article_data)
        # break
        # print(f"Bloomberg 已保存第 {number} 篇文章: {href_headline['url']}")
        number += 1
        yield article_data
    # print("Bloomberg 爬取成功！")

    # return bloomberg_all_data

# craw_bloom_inflation()

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
# index_file = "G:/biyesheji/financial_RAG/craw/craw_bloomberg/bloomberg_inflation_title_index.txt"
# save_dir = "G:/biyesheji/financial_RAG/craw/craw_bloomberg/bloomberg_inflation"
# href_headline = {'url': 'https://www.bloomberg.com/news/articles/2025-04-08/republicans-fracture-over-how-much-debt-to-run-up-for-tax-cuts?srnd=homepage-americas', 'headline': 'Test GOP Fractures Over How Much Debt to Run Up for Tax Cuts'}
# get_article_detail(href_headline,save_dir,index_file,headers,proxy)





