"""
# Time  : 2025/4/2 22:21
# Author: Hou Ly
"""


import re
import os
import time
import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from web_news_details.bloom_detail.BloomInflationDetail import get_news_detail

def query_bloom(save_dir,headers,proxy,params):
    search_url = "https://www.bloomberg.com/search"

    # 先获取url，然后get detail，然后保存
    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        # print("Bloomberg 请求成功！")
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select('a.thumbnailWrapper__23c201ad78')  # 选择<a class="thumbnailWrapper__23c201ad78" 中的href
        article_links = []
        for article in articles:
            link = article.get('href')
            if link:
                article_links.append(link)
        # bloom_search_result = {}
        for url in article_links:
            # print("url is ",url)
            article_data = get_news_detail(url, headers, proxy)
            yield article_data
            # invalid_chars = r'[\\/*?:"<>|]'
            # clean_title = re.sub(invalid_chars, '_', article_data["headline"])
            # 保存到文件
            # with open(f"{save_dir}/{clean_title}.txt", "w", encoding="utf-8") as f:
            #     json_str = json.dumps(article_data, ensure_ascii=False, indent=4)
            #     f.write(json_str)
            # print(f"{article_url}已保存")
            # with open(index_file, "a", encoding="utf-8") as file:
            #     file.write(article_url + "\n")
            # bloom_search_result[number] = article_data
            # number += 1
        # print(f"共搜集到了{len(article_links)}个相关网页，共爬取了{number}个网页内容")
        # print("Bloomberg Inflation 搜索完成！")


    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {"error": "bloom search failed"}

# save_dir = "query_bloom_data"
# os.makedirs(save_dir, exist_ok=True)
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
# # 构造Bloomberg搜索页面URL（按时间排序）
# params = {
#     "query": "tariff" #,
#     # "sort": "time:desc"  # 按时间降序排序
# }
# query_bloom(save_dir,headers,proxy,params)