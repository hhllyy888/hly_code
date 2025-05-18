"""
# Time  : 2025/4/3 22:15
# Author: Hou Ly
"""

#先获取url，然后根据url获取新闻详情页，最后保存


import re
import os
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlencode
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from web_news_details.CNBC_detail.CNBCFinanceDetail import get_news_detail

def query_cnbc(save_dir,headers,proxy,params):
    search_url = "https://www.cnbc.com/search"
    # 先获取url，然后get detail，然后保存
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        query_string = urlencode(params)
        full_url = f"{search_url}?{query_string}"
        driver.get(full_url)
        #隐式等待，这里不太行，还没加载完就退出了
        # driver.implicitly_wait(100)
        #显示等待
        wait = WebDriverWait(driver, 60)
        search = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#searchcontainer > *')))
        page_source = driver.page_source
        #解码
        decoded_html = page_source.encode().decode('unicode_escape')
        soup = BeautifulSoup(decoded_html, "html.parser")
        search_container = soup.find('div', id='searchcontainer')
        #获取url
        article_links = []
        all_article_links = search_container.find_all('div',class_="SearchResult-searchResultTitle")
        for sub_div in all_article_links:
            a_element = sub_div.find('a')
            link = a_element.get('href')
            if link:
                article_links.append(link)
        driver.quit() #获取到信息后，关闭浏览器

        # print("article_links len is ",len(article_links),article_links)
        #保存新闻详情信息
        for url in article_links:
            article_data = get_news_detail(url, headers, proxy)

            # invalid_chars = r'[\\/*?:"<>|]'
            # clean_title = re.sub(invalid_chars, '_', article_data["headline"])
            # 保存到文件
            # with open(f"{save_dir}/{clean_title}.txt", "w", encoding="utf-8") as f:
            #     json_str = json.dumps(article_data, ensure_ascii=False, indent=4)
            #     f.write(json_str)
            # print(f"{article_url}已保存")
            # with open(index_file, "a", encoding="utf-8") as file:
            #     file.write(article_url + "\n")
            yield article_data

        # print(f"共搜集到了{len(article_links)}个相关网页，共爬取了{number}个网页内容")
        # print("CNBC Finance 搜索完成！")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {"error":"cnbc search failed"}

# save_dir1 = "query_CNBC_data"
# os.makedirs(save_dir1, exist_ok=True)
# ua = UserAgent()
# headers1 = {
#     "User-Agent": ua.random,
#     "Accept-Language": "en-US,en;q=0.9",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
# }
# proxy1 = {
#         'http': 'http://127.0.0.1:7897',
#         'https': 'http://127.0.0.1:7897'
#     }
# # 构造CNBC搜索页面URL（按时间排序）
# params1 = {
#     "query": "tariff",
#     "qsearchterm": "tariff"  # 添加这个参数以匹配你的目标URL
# #   "sort": "time:desc"  # 按时间降序排序
# }
# query_cnbc(save_dir1,headers1,proxy1,params1)