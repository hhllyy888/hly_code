"""
# Time  : 2025/4/5 15:16
# Author: Hou Ly
"""

'''
下面把搜索引擎结合大模型
'''
from pprint import pprint
from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.generators import OpenAIGenerator
from haystack.components.websearch import SerperDevWebSearch
from haystack.components.generators import HuggingFaceLocalGenerator
from haystack.utils import Secret

web_search = SerperDevWebSearch(api_key=Secret.from_token("sk-PCNfCls6bdsOhug9j8QxkiopIU5FmfwTHkHBPQgoRTlsepum"), top_k=2)
link_content = LinkContentFetcher()
html_converter = HTMLToDocument()

template = """Given the information below: \n
            {% for document in documents %}
                {{ document.content }}
            {% endfor %}
            Answer question: {{ query }}. \n Answer:"""

prompt_builder = PromptBuilder(template=template)
pipe = Pipeline()
pipe.add_component("search", web_search)
pipe.add_component("fetcher", link_content)
pipe.add_component("converter", html_converter)
pipe.add_component("prompt_builder", prompt_builder)
pipe.add_component("llm", HuggingFaceLocalGenerator(model="Qwen/Qwen2.5-0.5B",
                                                    huggingface_pipeline_kwargs={"device_map": "auto",
                                                                                 "torch_dtype": "auto"},
                                                    generation_kwargs={
                                                        "max_new_tokens": 512,
                                                    }))

pipe.connect("search.links", "fetcher.urls")
pipe.connect("fetcher.streams", "converter.sources")
pipe.connect("converter.documents", "prompt_builder.documents")
pipe.connect("prompt_builder.prompt", "llm.prompt")

query = "英伟达50系列显卡上市时间"

result = pipe.run(data={"search": {"query": query}, "prompt_builder": {"query": query}})

pprint(result)