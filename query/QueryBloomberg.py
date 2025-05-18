"""
# Time  : 2025/3/3 21:43
# Author: Hou Ly
"""

import requests
from bs4 import BeautifulSoup
import os
import time
from fake_useragent import UserAgent
from QueryBlooombergContent import get_html_text

save_dir = "querydata_test/bloomberg"
os.makedirs(save_dir, exist_ok=True)

ua = UserAgent()
# 随机生成 User-Agent
headers = {
    "User-Agent": ua.random,
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.bloomberg.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
# 构造Bloomberg搜索页面URL（按时间排序）
search_url = "https://www.bloomberg.com/search"
params = {
    "query": "tariff" #,
    # "sort": "time:desc"  # 按时间降序排序
}
# 获取搜索结果页
try:
    response = requests.get(search_url, params=params, headers=headers, timeout=10)
    response.raise_for_status()  # 检查HTTP错误
    print("请求成功")
except requests.exceptions.RequestException as e:
    response = ""
    print(f"请求失败: {e}")

# 解析搜索结果页
soup = BeautifulSoup(response.text, "html.parser")
# print("soup is ",soup)
articles = soup.select('a.thumbnailWrapper__23c201ad78') #选择<a class="thumbnailWrapper__23c201ad78" 中的href

# 提取 href 的 URL
article_links = []
for article in articles:
    link = article.get('href')
    if link:
        article_links.append(link)

number = 0
for url in article_links:
    # print("url is ",url)
    number += get_html_text(url)
print(f"共搜集到了{len(article_links)}个相关网页，共爬取了{number}个网页内容")


# 下载并保存文章内容
for idx, url in enumerate(article_links[:10], 1):
    try:
        article_resp = requests.get(url, headers=headers, timeout=10)
        article_resp.raise_for_status()
        # 保存到文件
        with open(f"{save_dir}/article_{idx}.html", "w", encoding="utf-8") as f:
            f.write(article_resp.text)
        print(f"已保存第 {idx} 篇文章: {url}")
        time.sleep(2)  # 避免频繁请求

    except Exception as e:
        print(f"下载失败 {url}: {e}")

print("爬取完成！")


