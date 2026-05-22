"""
    要使用动态模型，请使用 @wrap_model_call 装饰器创建中间件，该装饰器会在请求中修改模型
"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


basic_model = ChatOpenAI(model="qwen3-max")
advanced_model = ChatOpenAI(model="qwen3.6-plus")

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])

    if message_count > 10:
        # Use an advanced model for longer conversations
        model = advanced_model
    else:
        model = basic_model

    return handler(request.override(model=model))

agent = create_agent(
    model=basic_model,  # Default model
    tools=[get_weather],
    middleware=[dynamic_model_selection]
)




"""
Pre-bound models (models with bind_tools already called) are not supported when using structured output. If you need dynamic model selection with structured output, ensure the models passed to the middleware are not pre-bound.

"""