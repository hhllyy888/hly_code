"""
# Time  : 2025/3/27 20:26
# Author: Hou Ly
"""

import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from craw.craw_bloomberg.CrawBloombergInflation import craw_bloom_inflation
from craw.craw_CNBC.CrawCNBCFinance import craw_CNBC_finance
from craw.craw_reuters.CrawReutersFinance import craw_reuters_finance
from datetime import datetime



def print_time(label):
    now = datetime.datetime.now()
    now_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{label}开始爬取的时间是 {now_time}")


# if __name__ == "__main__":
#     scheduler = BlockingScheduler()
#     now = datetime.datetime.now()
#     # 每隔 3 小时运行一次
#     # 获取当前日期和时间
#     print_time("craw_bloom_inflation")
#     scheduler.add_job(craw_bloom_inflation, 'interval', minutes=3, next_run_time=now) #后续需要将其改为间隔3h
#     print_time("craw_CNBC_finance")
#     scheduler.add_job(craw_CNBC_finance, 'interval', minutes=3, next_run_time=now)
#     print_time("craw_reuters_finance")
#     scheduler.add_job(craw_reuters_finance, 'interval', minutes=3,next_run_time=now)
#     try:
#         print('开始调度任务...')
#         scheduler.start()
#     except (KeyboardInterrupt, SystemExit):
#         print('任务调度已停止。')

# print("线上代码运行成功！")

#离线跑三轮
# n = 5
# for i in range(n):
#
# print(f"{n}轮爬取成功！")

# for i in range(5):
bloom_all_data = craw_bloom_inflation()
cnbc_all_data = craw_CNBC_finance()
reuters_all_data = craw_reuters_finance()
print("bloom_all_data is ",bloom_all_data)
print("cnbc_all_data is ",cnbc_all_data)
print("reuters_all_data is ",reuters_all_data)

current_time = datetime.now()
print("当前时间是 ",current_time)