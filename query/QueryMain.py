"""
# Time  : 2025/4/4 16:43
# Author: Hou Ly
"""

import os
from fake_useragent import UserAgent
from QueryToList import rewrite_query_gpt
from query_bloom.QueryBloom import query_bloom
from query_CNBC.QueryCNBC import query_cnbc



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


bloom_save_dir = "query_bloom/query_bloom_main"
os.makedirs(bloom_save_dir, exist_ok=True)

cnbc_save_dir = "query_CNBC/query_CNBC_main"
os.makedirs(cnbc_save_dir, exist_ok=True)

query = "中国关税"
query_list = rewrite_query_gpt(query)
print("query_list is ",query_list)

search_results = {}
number = 1
for keyword in query_list:
    print(f"正在查询关键词 {keyword}...")
    bloom_params = { "query": keyword }
    cnbc_params = {
        "query": keyword,
        "qsearchterm": keyword
    }

    for each_article_data in query_bloom(bloom_save_dir, headers, proxy, bloom_params):
        search_results[number] = each_article_data
        number += 1
    for each_article_data in query_cnbc(cnbc_save_dir, headers, proxy, cnbc_params):
        search_results[number] = each_article_data
        number += 1
    print(f"关键词 {keyword} 查询完毕")
print("search data successfully!")
