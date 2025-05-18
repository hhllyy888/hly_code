"""
# Time  : 2025/3/3 21:56
# Author: Hou Ly
"""


import re
import time
import requests
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def extract_text(data):
    result = ""
    if isinstance(data, list):
        for item in data:
            result += extract_text(item)
    elif isinstance(data, dict):
        if data.get('type') == 'paragraph':
            result += '\n'
        elif data.get('type') == 'text':
            result += data.get('value', '')
        for value in data.values():
            result += extract_text(value)
    return result


def get_content(soup):
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if script_tag:
        json_data = script_tag.string
        try:
            # 解析 JSON 数据
            data = json.loads(json_data)
            # print("data is ",data)
            content = data["props"]["pageProps"]["story"]["body"]
            result = extract_text(content)
            return result

        except json.JSONDecodeError as e:
            print(f"解析 JSON 数据时出错: {e}")
            return ""
    else:
        print("未找到 id 为 __NEXT_DATA__ 的 script 标签。")
        return ""


def get_headline_author_pubtime(soup):
    script_tag = soup.find('script', id='gtm_analytics')
    try:
        if script_tag:
            # print("soup is ",soup)
            # print("script_tag is ",script_tag)
            # print("type script_tag is ",type(script_tag))
            script_content = script_tag.string
            start = script_content.find("{")
            end = script_content.find("}")
            script_json = json.loads(script_content[start:end + 1])
            author = script_json.get('author')
            headline = script_json.get('headline')
            published_at = script_json.get('publishedAt')

            # print("Author:", author)
            # print("Headline:", headline)
            # print("Published At:", published_at)
            return headline, author, published_at
        else:
            return "None","None","None"

    except json.JSONDecodeError:
        print("无法解析 JSON 数据")
        return "no headline", "no author", "no published_at"


def get_html_text(url):
    ua = UserAgent()
    # 随机生成 User-Agent
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.bloomberg.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    try:
        # time.sleep(5)
        response = requests.get(url,headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        print("请求成功")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        response = ""
    # print("res ",response)
    soup = BeautifulSoup(response.text, "html.parser")
    headline, author, published_at = get_headline_author_pubtime(soup)
    if headline == "None" and author == "None" and published_at == "None":
        return 0
    content = get_content(soup)
    # print("Author:", author)
    # print("Headline:", headline)
    # print("Published At:", published_at)
    # print("content is ",content)
    base_catalog = "./querydata/bloomberg/00/"
    invalid_chars = r'[\\/*?:"<>|]'
    clean_headline = re.sub(invalid_chars, '_', headline)
    filename = base_catalog + clean_headline +'.txt'
    with open(filename, 'w', encoding='utf-8') as Out:
        Out.write(f"Headline: {headline}\n")
        Out.write(f"Author: {author}\n")
        Out.write(f"Published At: {published_at}\n")
        Out.write(f"Url: {url}\n")
        Out.write(f"Content: {content}")
        print(f"已将内容写入{filename}中")
    url_file = "querydata_test/bloomberg/catalog/url.txt"
    with open(url_file, 'a', encoding='utf-8') as Out:
        Out.write(url)
        Out.write("\n")
        print(f"已将url写入{url_file}中")
    return 1


# url = "https://www.bloomberg.com/news/articles/2025-03-04/stock-market-today-dow-s-p-live-updates"
# get_html_text(url)
