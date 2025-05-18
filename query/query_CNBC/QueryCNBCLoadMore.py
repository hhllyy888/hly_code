"""
# Time  : 2025/4/4 14:34
# Author: Hou Ly
"""

#没有验证过，目前是取直接加载出来的前10个

import requests
from bs4 import BeautifulSoup

# 假设这是搜索结果页面的基础 URL
base_url = "https://example.com/search"
# 每次请求获取的结果数量
results_per_page = 9
# 总共需要的结果数量
total_results = 20

all_results = []
page = 1

while len(all_results) < total_results:
    # 构建请求 URL，这里假设通过 page 参数进行分页
    url = f"{base_url}?page={page}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # 假设搜索结果的 HTML 元素有一个特定的类名 'search-result'
        results = soup.find_all(class_='search-result')
        all_results.extend(results)
        page += 1
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        break

# 截取前20个结果
final_results = all_results[:total_results]

# 打印结果
for result in final_results:
    print(result.text.strip())
