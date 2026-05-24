"""
情况一
Filtering pre-registered tools 筛选预注册工具:
    如果在代理创建时已知所有可能的工具，您可以预先注册它们，并根据状态、权限或上下文动态筛选哪些工具将对模型可见。

"""

#------------------------------------------------
'case1：仅在达到特定对话里程碑后启用高级工具'
#------------------------------------------------

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@wrap_model_call     #  自定义中间件
def state_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on conversation State."""
    # 从State中读取：检查用户是否已认证
    state = request.state
    is_authenticated = state.get("authenticated", False)
    message_count = len(state["messages"])

    # 根据认证状态和消息数量动态筛选工具
    if not is_authenticated:
        tools = [t for t in request.tools if t.name.startswith("public_")]
        request = request.override(tools=tools)
    elif message_count < 5:
        # 在对话的前几个回合中仅启用基本工具
        tools = [t for t in request.tools if t.name != "advanced_search"]
        request = request.override(tools=tools)

    return handler(request)

agent = create_agent(
    model="gpt-5.4",
    tools=[public_search, private_search, advanced_search],
    middleware=[state_based_tools]          #中间件
)



#------------------------------------------------
'case2：利用中间件（Middleware）和状态存储（Store）在运行时（Runtime）动态筛选 Agent 可用的工具'
#------------------------------------------------

from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:                      #它定义了单次运行（Per-run）必须传递的外部元数据契约（Schema）
    user_id: str

@wrap_model_call
def store_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on Store preferences."""
    # 1. 从运行时上下文中拿到当前发起请求的用户 ID
    user_id = request.runtime.context.user_id

    # Read from Store: get user's enabled features
    store = request.runtime.store
    # 2. 从全局存储中，通过命名空间 ("features",) 和 键 (user_id) 获取该用户的配置
    feature_flags = store.get(("features",), user_id)

    if feature_flags:
        # 3. 提取出该用户被允许使用的工具名称列表，例如：["search_tool", "export_tool"]
        enabled_features = feature_flags.value.get("enabled_tools", [])
        # 4. 关键过滤：遍历原本准备提交给模型的所有工具（request.tools），
        #    只保留其名字在 user_id 允许列表（enabled_features）中的工具。
        tools = [t for t in request.tools if t.name in enabled_features]
        # 5. 重写请求：使用 .override() 方法生成一个替换了工具列表的新 request 对象
        request = request.override(tools=tools)

    # 6. 放行：将修改后的 request 传递给下游。此时大模型只能看到过滤后的工具。
    return handler(request)

agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool, analysis_tool, export_tool],
    middleware=[store_based_tools],     # 挂载我们的拦截器
    context_schema=Context,             # 声明后台必须传入 Context 这个数据结构中定义的数据
    store=InMemoryStore()               # 注入存储
)

#------------------------------------------------
'case3： 基于运行时上下文（Runtime Context）和中间件（Middleware）对 Agent 进行动态权限控制和工具隔离'
#------------------------------------------------

from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@dataclass
class Context:              #它定义了单次运行（Per-run）必须传递的外部元数据契约（Schema）
    user_role: str

@wrap_model_call
def context_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on Runtime Context permissions."""
    # Read from Runtime Context: get user role
    if request.runtime is None or request.runtime.context is None:
        # 1. 容错处理：确保 runtime 和 context 存在。如果没传，默认给予最低的权限 "viewer"
        user_role = "viewer"
    else:
        user_role = request.runtime.context.user_role

    # 2. 根据角色动态过滤工具箱 (RBAC 核心)
    if user_role == "admin":
        # 管理员：不进行任何拦截，保留全部工具 (read_data, write_data, delete_data)
        pass
    elif user_role == "editor":
        # 编辑：不允许使用 delete_data 工具。
        # 遍历 request.tools 过滤掉名字为 "delete_data" 的工具。
        tools = [t for t in request.tools if t.name != "delete_data"]
        # 【关键点】使用 .override() 生成一个全新的、工具被修改后的 request 对象
        request = request.override(tools=tools)
    else:
        # 访客：只允许调用以 "read_" 开头的只读工具 (比如 read_data)
        tools = [t for t in request.tools if t.name.startswith("read_")]
        request = request.override(tools=tools)

    # 3. 将修改（或未修改）后的 request 对象放行传给下游
    return handler(request)

agent = create_agent(
    model="gpt-5.4",
    tools=[read_data, write_data, delete_data],
    middleware=[context_based_tools],
    context_schema=Context          #声明后台必须传入 Context 这个数据结构中定义的数据
)




"""
情况二
Runtime tool registration  运行时工具注册:
    如果在代理创建时已知所有可能的工具，您可以预先注册它们，并根据状态、权限或上下文动态筛选哪些工具将对模型可见。

"""