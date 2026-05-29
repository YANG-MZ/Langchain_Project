from langchain_openai import ChatOpenAI


# =======================================================================================================
#    批次调用,先等所有任务完成,把所有结果收集成 list，一次性得到所有的响应结果
# =======================================================================================================
model = ChatOpenAI(model="qwen3-max")
responses = model.batch([
    "你好",
    "1+1等于几？"
])
print(responses)

# output：
# [AIMessage(content='你好！有什么我可以帮你的吗？😊', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 9, 'prompt_tokens': 9, 'total_tokens': 18, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'qwen3-max', 'system_fingerprint': None, 'id': 'chatcmpl-54e98f39-5447-9a48-b3fb-9a740a99e77f', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019e743e-f9cc-76e2-80a7-9f67e1cc5f22-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 9, 'output_tokens': 9, 'total_tokens': 18, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}), 
#  AIMessage(content='1 + 1 等于 2。', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 11, 'prompt_tokens': 14, 'total_tokens': 25, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'qwen3-max', 'system_fingerprint': None, 'id': 'chatcmpl-96b7f56b-6688-9dfd-92b9-6babf96d428e', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019e743e-f9cc-76e2-80a7-9f7c088881d2-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 14, 'output_tokens': 11, 'total_tokens': 25, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}})]



# =======================================================================================================
#    批次调用,边完成边返回,而不是等全部结束再返回，可能是乱序，但每个结果都包含用于匹配的输入索引
# =======================================================================================================
model = ChatOpenAI(model="qwen3-max")
responses = model.batch_as_completed([
    "你好",
    "1+1等于几？"
])

for response in responses:
    print(response)

# output：
# (1, AIMessage(content='1 + 1 等于 2。', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 11, 'prompt_tokens': 14, 'total_tokens': 25, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'qwen3-max', 'system_fingerprint': None, 'id': 'chatcmpl-6c076f4c-0292-938c-9bcf-d7205d5e871a', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019e7435-718c-7f40-897a-2ca1323a364e-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 14, 'output_tokens': 11, 'total_tokens': 25, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}))
# (0, AIMessage(content='你好！很高兴见到你，有什么我可以帮忙的吗？😊', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 13, 'prompt_tokens': 9, 'total_tokens': 22, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'qwen3-max', 'system_fingerprint': None, 'id': 'chatcmpl-ed5cf239-72a4-9739-a4f5-24c9891ad559', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019e7435-718c-7f40-897a-2c9100a99ed7-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 9, 'output_tokens': 13, 'total_tokens': 22, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}))