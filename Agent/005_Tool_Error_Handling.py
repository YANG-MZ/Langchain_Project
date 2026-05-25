"""

Tool error handling  工具错误处理:
    -若要自定义工具错误的处理方式，请使用 @wrap_tool_call 装饰器来创建中间件

"""

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage


@wrap_tool_call
def handle_tool_errors(request, handler):
    """
    当工具报错时，拦截异常，并将其优雅地转化为一条 ToolMessage 塞回给大模型，
    让大模型知道“工具报错了，错误原因是什么”，从而给模型一次“自我纠错（Self-Correction）”的机会
    """
    try:
        return handler(request)
    except Exception as e:
        # 向模型返回自定义错误消息，包括错误信息
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )

agent = create_agent(
    model="gpt-5.4",
    tools=[search, get_weather],
    middleware=[handle_tool_errors]
)


"""
[用户]: "查一下那个叫 '布拉布拉拉' 的地方的天气"
   │
   ▼
[gpt-5.4]: 决定调用工具 -> get_weather(location="布拉布拉拉")
   │
   ▼
[进入中间件]: 触发 handle_tool_errors -> 开始执行 handler(request)
   │
   ▼
[工具崩溃]: get_weather 内部报错: "City not found"
   │
   ▼
[中间件拦截]: 捕获异常，阻断崩溃！
   │          生成 ToolMessage(content="Tool error: ... (City not found)", id="call_123")
   │
   ▼
[信息倒回]: Agent 将这条 ToolMessage 作为“观察结果（Observation）”喂回给 gpt-5.4
   │
   ▼
[gpt-5.4 纠错]: 看到报错信息后，理解了原因，对用户说：“抱歉，我没有找到名为‘布拉布拉拉’的城市，请问拼写是否正确？”
"""