from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

##  Static model  静态模型
model = ChatOpenAI(
    model="qwen3-max",
    temperature=0.1,
    # max_tokens=1000,            #OpenAI 于 2024 年 9 月弃用了 max_tokens ，转而使用 max_completion_tokens 。虽然为了向后兼容， max_tokens 仍然得到支持，但它在内部会自动转换为 max_completion_tokens 。
    max_completion_tokens=1000,
    timeout=30
    # ... (other params)
)

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)



