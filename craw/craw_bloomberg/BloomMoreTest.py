"""
# Time  : 2025/4/2 20:58
# Author: Hou Ly
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# # 设置 Chrome 为无头模式
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# # 初始化浏览器驱动
# driver = webdriver.Chrome(options=chrome_options)
# try:
#     # 打开网页
#     driver.get('https://www.bloomberg.com/economics/inflation-and-prices')
#     # 等待页面加载
#     time.sleep(3)
#     # 通过 CSS 选择器定位按钮元素，注意类名之间用点号连接
#     button = driver.find_element(By.CSS_SELECTOR,
#                                  'button.media-ui-Button_button-phoenix-D1e3y3-dPnA-.media-ui-Button_default-1-Rsg7503aw-.media-ui-OutlinedButton_outlinedButton-phoenix-578zuGBVzuk-.media-ui-OutlinedButton_light-73gI9xYets4-.media-ui-OutlinedButton_default-WRnB2HeLXEE-.LineupContentArchive_loadMore__qFJho.outlined-button')
#     # 点击按钮
#     button.click()
#     # 等待一段时间，让页面加载
#     time.sleep(5)
#     print("点击成功")
#     # 获取当前网页的源代码
#     page_source = driver.page_source
#     # 这里可以对源代码进行处理，比如保存到文件
#     # 示例：将源代码保存到文件
#     print('page_source is :', page_source)
#
# except Exception as e:
#     print(f"点击按钮时出错: {e}")
#
# finally:
#     # 关闭浏览器
#     driver.quit()



# 测试网页源代码是否存在button class
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
response = requests.get(url, headers=headers, proxies=proxy)
soup = BeautifulSoup(response.text, 'html.parser')
print("soup is ",soup)
# button = soup.find_all('button', class_='media-ui-Button_button-phoenix-D1e3y3-dPnA-.media-ui-Button_default-1-Rsg7503aw-.media-ui-OutlinedButton_outlinedButton-phoenix-578zuGBVzuk-.media-ui-OutlinedButton_light-73gI9xYets4-.media-ui-OutlinedButton_default-WRnB2HeLXEE-.LineupContentArchive_loadMore__qFJho.outlined-button')
# print("button is ", button)

# #交互
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
#
# # 代理信息
# proxy_ip = '127.0.0.1'
# proxy_port = '7897'
# # 配置 Chrome 选项（避免被反爬检测和设置无头模式）
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # 设置为无头模式
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_argument(f'--proxy-server=http://{proxy_ip}:{proxy_port}')
#
# # 初始化浏览器驱动
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://www.bloomberg.com/your-page-url")  # 替换为实际页面URL
#
# try:
#     # 显式等待父级 div 元素加载（确保结构稳定）
#     print("before driver.page_source: ",driver.page_source)
#     wait = WebDriverWait(driver, 20)
#     pagination_div = wait.until(EC.presence_of_element_located(
#         (By.CSS_SELECTOR, "div.LineupContentArchive_paginationContainer__Nn23p")
#     ))
#
#     # 在父级 div 内部定位按钮（避免依赖按钮的复杂 class）
#     load_more_button = pagination_div.find_element(By.CSS_SELECTOR, "button")
#
#     # 通过 JavaScript 点击按钮（确保触发点击事件）
#     driver.execute_script("arguments[0].click();", load_more_button)
#
#     # 等待新内容加载（根据实际页面调整条件）
#     # 示例：等待新增内容区域出现（假设新增内容类名为 "news-item"）
#     wait.until(EC.presence_of_element_located(
#         (By.CSS_SELECTOR, ".news-item:nth-child(10)")  # 根据实际情况调整
#     ))
#
#     # 获取渲染后的完整页面源码
#     rendered_html = driver.page_source
#     print(rendered_html)  # 或保存到文件
#
# finally:
#     driver.quit()  # 确保退出浏览器