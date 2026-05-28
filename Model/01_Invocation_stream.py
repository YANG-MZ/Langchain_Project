from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="qwen3-max")

"""
<class 'langchain_core.messages.ai.AIMessageChunk'>
chunk(AIMessageChunk)的内部部结构如下：
    content='鹦' 
    additional_kwargs={} 
    response_metadata={'model_provider': 'openai'} 
    id='lc_run--019e6efa-985d-7d23-9893-ec275528440c' 
    tool_calls=[] 
    invalid_tool_calls=[] 
    tool_call_chunks=[]
"""


# ------------------------------------------------------------------------------
#    流式调用的chunk,可以直接访问text属性,得到当前块的文本内容
# ------------------------------------------------------------------------------
# for chunk in model.stream("简要回答,为什么鹦鹉有彩色羽毛？"):
#     print(chunk.content, end="|", flush=True)



# ------------------------------------------------------------------------------
#    流式调用的chunk,可以根据块的类型进行不同的处理
# ------------------------------------------------------------------------------
# for chunk in model.stream("我在美国，现在的天空是什么颜色的?"):
#     for block in chunk.content_blocks:
#         if block["type"] == "reasoning" and (reasoning := block.get("reasoning")):
#             print(f"Reasoning: {reasoning}")
#         elif block["type"] == "tool_call_chunk":
#             print(f"Tool call chunk: {block}")
#         elif block["type"] == "text":
#             print(block["text"])
#         else:
#             print(f"Other block: {block}")




# ------------------------------------------------------------------------------
#    流式调用的chunk,可以简单地用+操作符进行拼接,得到完整的消息对象
# ------------------------------------------------------------------------------
# full = None  # None | AIMessageChunk
# for chunk in model.stream("为什么鹦鹉有彩色羽毛?"):
#     full = chunk if full is None else full + chunk
#     print(full.text) 

# # The
# # The sky
# # The sky is
# # The sky is typically
# # The sky is typically blue
# # ...

# print(full.content_blocks)
# # [{"type": "text", "text": "The sky is typically blue..."}]




