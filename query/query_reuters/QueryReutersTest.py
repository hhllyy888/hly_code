"""
# Time  : 2025/4/4 15:16
# Author: Hou Ly
"""


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlencode
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random

# 设置搜索 URL 和参数
search_url = "https://www.reuters.com/site-search"
params = {
    "query": "tariff"
}

# 常见的 User-Agent 列表
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
]

# 随机选择一个 User-Agent
random_user_agent = random.choice(user_agents)

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument(f"user-agent={random_user_agent}")  # 设置随机 User-Agent
# chrome_options.add_argument('--headless')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 执行 JavaScript 代码修改 navigator.webdriver 属性
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })

    query_string = urlencode(params)
    full_url = f"{search_url}?{query_string}"
    driver.get(full_url)

    # 模拟随机的鼠标移动
    actions = ActionChains(driver)
    for _ in range(random.randint(3, 6)):
        x = random.randint(100, 500)
        y = random.randint(100, 500)
        actions.move_by_offset(x, y).perform()
        actions.move_by_offset(-x, -y).perform()

    # 模拟随机的页面滚动
    for _ in range(random.randint(2, 5)):
        scroll_distance = random.randint(200, 500)
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        driver.implicitly_wait(random.randint(1, 3))

    # 等待页面加载完成
    driver.implicitly_wait(100)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    print("soup is ", soup)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # 关闭浏览器
    driver.quit()