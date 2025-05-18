"""
# Time  : 2025/3/26 12:57
# Author: Hou Ly
"""

import requests
from fake_useragent import UserAgent

# 创建会话对象
session = requests.Session()

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
    "query": "tariff"
    # "sort": "time:desc"  # 按时间降序排序
}
# 获取搜索结果页
try:
    # 使用会话对象发送请求
    response = session.get(search_url, params=params, headers=headers, timeout=10)
    response.raise_for_status()  # 检查HTTP错误
    print("请求成功")
    print(response.text)
except requests.exceptions.RequestException as e:
    response = ""
    print(f"请求失败: {e}")
