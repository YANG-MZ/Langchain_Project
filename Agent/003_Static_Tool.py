"""
@tool 装饰器不仅仅是“把函数变成工具”，它本质上还是一个 Tool Metadata 定义器。
它的作用是为函数提供元数据（metadata），这些元数据描述了函数的功能、输入参数、输出格式等信息。这些信息对于工具的使用者来说非常重要，因为它们可以帮助使用者理解工具的用途和如何正确地调用它。
因此，@tool 装饰器的作用不仅仅是将函数转换为工具，还包括为函数提供必要的元数据，使其成为一个完整的工具，可以被其他组件（如Agent）正确地识别和使用。

"""


from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="qwen3-max", temperature=0.1, max_completion_tokens=1000, timeout=30)

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(model, tools=[search, get_weather])        #如果提供的工具列表为空，则代理将由一个没有工具调用功能的 LLM 节点组成

