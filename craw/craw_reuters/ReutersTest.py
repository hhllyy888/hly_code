"""
# Time  : 2025/4/1 00:19
# Author: Hou Ly
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 初始化浏览器驱动
driver = webdriver.Chrome()

try:
    # 打开网页
    driver.get('https://www.reuters.com/business/finance/')

    # 等待页面加载，可根据实际情况调整等待时间
    time.sleep(3)

    # 通过多个 class 名定位按钮元素，类名之间用点号连接
    button = driver.find_element(By.CSS_SELECTOR,
                                 'button.button__button__2Ecqi.button__secondary__18moI.button__round__1nYLA.button__w_auto__6WYRo.text-button__container__3q3zX')
    button.click()

    # 等待一段时间，让页面加载
    time.sleep(5)
    print("点击成功")

except Exception as e:
    print(f"点击按钮时出错: {e}")

finally:
    # 关闭浏览器
    driver.quit()


#
#
# #点击加载更多
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
#
# # 初始化浏览器驱动
# driver = webdriver.Chrome()
# # 打开网页
# driver.get('https://www.reuters.com/business/finance/')
# try:
#     # 通过单个 class 名定位按钮元素
#     button = driver.find_element(By.CSS_SELECTOR, 'button.button__button__2Ecqi button__secondary__18moI button__round__1nYLA button__w_auto__6WYRo text-button__container__3q3zX')
#     button.click()
#     # 等待一段时间，让页面加载
#     time.sleep(5)
#     print("点击成功")
# except Exception as e:
#     print(f"点击按钮时出错: {e}")
# finally:
#     # 关闭浏览器
#     driver.quit()
