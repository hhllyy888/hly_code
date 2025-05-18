"""
# Time  : 2025/3/10 21:37
# Author: Hou Ly
"""

# import pickle
#
# # 使用 with 语句打开 .pkl 文件
# with open('080001.pkl', 'rb') as file:
#     # 反序列化数据
#     data = pickle.load(file)
#
# # 打印读取的数据
# print(data)


# Finnhub (Yahoo Finance, Reuters, SeekingAlpha, CNBC...)
from finnlp.data_sources.news.finnhub_date_range import Finnhub_Date_Range

start_date = "2023-01-01"
end_date = "2023-01-03"
config = {
    "use_proxy": "us_free",    # use proxies to prvent ip blocking
    "max_retry": 5,
    "proxy_pages": 5,
    "token": "cv9c9v9r01qjq627ufsgcv9c9v9r01qjq627uft0"  # Available at https://finnhub.io/dashboard
}

news_downloader = Finnhub_Date_Range(config)                      # init
news_downloader.download_date_range_stock(start_date,end_date)    # Download headers
news_downloader.gather_content()                                  # Download contents
df = news_downloader.dataframe
selected_columns = ["headline", "content"]
df[selected_columns].head(10)
