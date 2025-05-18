"""
# Time  : 2025/4/4 15:40
# Author: Hou Ly
"""

#由query生成关键词列表

import time
from utile.DeepseekApi import deepseek_chat_api,deepseek_r1_api
from utile.GptApi import gpt_api


def get_system_prompt():
    system_prompt = """
    你现在是一个查询领域的专家，你需要根据输入的query，从中提取出有效、有意义、最小单位的词。
    1、有效指的是提取出来的词语，符合query内容，可以是专业名词的简写，但需要确保不是凭空捏造的。
    2、有意义指的是这个词能够作为一个单独的词进行查询操作，比如语气词、代词就不是有效的词。
    3、最小单位指的是这个词以最短的长度表明最清晰的意思。比如新闻、近期、政策指代的太模糊，它们作为关键词会搜索出大量无关信息，它们不是最小单位的词。但关税、苹果公司、美联储等就是最小单位词语，它们以最短的长度表达着最清楚的意义，
    比如，用户输入：近期美联储降息的原因
    分析过程：针对这一个输入，关键的实词为 美联储降息、美联储、降息，对于“美联储”、“降息”这些词都可以作为一个关键信息的词出现，因为它们指定的范围非常具体；而“近期”、“原因”等词语，范围太大，不足成为为查询的关键词。
    输出：{"query_list":["Federal Reserve","cut interest rates","Federal Reserve cuts interest rates"]}
    再比如，用户输入：美国关税政策现在怎么样了，近期有什么新闻
    分析过程：针对这一个输入，美国关税、关税可以作为一个最小单位出现，而对于“政策”、“现在”、“怎么样”、“近期”、“新闻”一词，指定的范围太大，没有携带关键信息，不足以成为一个关键词
    输出：{"query_list":["U.S. tariffs","tariff"]}
    你需要处理的query如下，最终只需要输出查询关键词列表：
    """
    return system_prompt


def rewrite_query_dp_r1(query):
    system_prompt = get_system_prompt()
    requery = deepseek_r1_api(system_prompt,query)
    requery = requery["query_list"]
    return requery

def rewrite_query_dp_chat(query):
    system_prompt = get_system_prompt()
    requery = deepseek_chat_api(system_prompt,query)
    requery = requery["query_list"]
    return requery

def rewrite_query_gpt(query):
    system_prompt = get_system_prompt()
    requery = gpt_api(system_prompt,query)
    print("requery is ",requery)
    requery = requery["query_list"]
    return requery


# query = "中国近期有什么重大政策"
# s1 = time.time()
# print(rewrite_query_dp_r1(query))
# s2 = time.time()
# print(f"耗时为{s2-s1:.2f}s")
#
# print(rewrite_query_dp_chat(query))
# s3 = time.time()
# print(f"耗时为{s3-s2:.2f}s")
# res = rewrite_query_gpt(query)
# print(type(res)) #<class 'list'>
# print(res)
# s4 = time.time()
# print(f"耗时为{s4-s3:.2f}s")
