"""
基于 LangChain + LangGraph 的天气智能体
具备：时间查询、天气查询、持久化记忆、日志、城市ID缓存、流式输出
"""

import asyncio
import datetime
import logging
import os
from typing import Annotated, Literal, TypedDict, Optional, AsyncGenerator
from functools import lru_cache

import requests
from dotenv import load_dotenv

from langchain_core.messages import ToolMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableConfig

# ========== 日志配置 ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
# ========== 加载环境变量 ==========
load_dotenv()

# ========== 配置 ==========
QWEN_API_KEY = os.getenv("DASHSCOPE_API_KEY")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
QWEN_MODEL_NAME = os.getenv("QWEN_MODEL_NAME", "qwen-turbo")

HEFENG_API_KEY = os.getenv("HEFENG_API_KEY")
HEFENG_HOST = os.getenv("HEFENG_HOST")

if HEFENG_HOST:
    HEFENG_HOST = HEFENG_HOST.rstrip('/')
    HEFENG_GEO_URL = f"{HEFENG_HOST}/geo/v2/city/lookup"
    HEFENG_WEATHER_URL = f"{HEFENG_HOST}/v7/weather/now"
else:
    HEFENG_GEO_URL = "https://geoapi.qweather.com/v2/city/lookup"
    HEFENG_WEATHER_URL = "https://devapi.qweather.com/v7/weather/now"

# 验证必要配置
if not QWEN_API_KEY:
    raise ValueError("请在 .env 中设置 DASHSCOPE_API_KEY")
if not HEFENG_API_KEY:
    raise ValueError("请在 .env 中设置 HEFENG_API_KEY")

# ========== 工具定义 ==========

@tool
def get_current_time() -> str:
    """获取当前真实时间。当用户询问现在几点、今天几号、当前时间时调用此工具。"""
    return datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")


@lru_cache(maxsize=128)
def get_city_id(city_name: str) -> tuple[Optional[str], Optional[str]]:
    """
    将城市名转换为和风天气 Location ID（带缓存）
    返回 (location_id, standard_name)
    """
    try:
        response = requests.get(
            HEFENG_GEO_URL,
            params={"key": HEFENG_API_KEY, "location": city_name.strip(), "number": 1},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if data.get("code") == "200" and data.get("location"):
            loc = data["location"][0]
            return loc.get("id"), loc.get("name")
        else:
            logger.warning(f"城市搜索失败: {city_name}, code={data.get('code')}")
            return None, None
    except requests.exceptions.Timeout:
        logger.warning(f"城市搜索超时: {city_name}")
        return None, None
    except requests.exceptions.ConnectionError:
        logger.warning(f"城市搜索网络错误: {city_name}")
        return None, None
    except Exception as e:
        logger.warning(f"城市搜索未知错误: {city_name}, {e}")
        return None, None

@tool
def get_weather(city: str) -> str:
    """
    获取指定城市的实时天气。
    当用户询问天气、气温、下雨、带伞等问题时调用此工具。

    Args:
        city: 城市名称，如"北京"、"上海"
    """
    city_id, standard_name = get_city_id(city)
    if not city_id:
        return f"未找到城市「{city}」，请检查城市名称是否正确"

    try:
        response = requests.get(
            HEFENG_WEATHER_URL,
            params={"key": HEFENG_API_KEY, "location": city_id, "unit": "m"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if data.get("code") == "200":
            now = data.get("now", {})
            return (f"{standard_name or city}天气：{now.get('text', '未知')}，"
                    f"{now.get('temp', '未知')}°C，体感{now.get('feelsLike', '未知')}°C")
        else:
            logger.warning(f"天气查询失败: {city}, code={data.get('code')}")
            return f"查询{city}天气失败：{data.get('code', '未知错误')}"
    except requests.exceptions.Timeout:
        logger.warning(f"天气查询超时: {city}")
        return f"查询{city}天气超时，请稍后重试"
    except requests.exceptions.ConnectionError:
        logger.warning(f"天气查询网络错误: {city}")
        return f"无法连接天气服务，请检查网络"
    except Exception as e:
        logger.error(f"天气查询异常: {city}, {e}")
        return f"天气查询出错：{str(e)}"


tools = [get_current_time, get_weather]
tools_by_name = {tool.name: tool for tool in tools}

# ========== LangGraph 状态定义 ==========

class AgentState(TypedDict):
    """智能体状态"""
    messages: Annotated[list, add_messages]
    next_action: Literal["use_tools", "end"]


# ========== 创建 LangGraph 智能体 ==========

def create_weather_agent():
    """创建天气智能体"""

    # 初始化 LLM（开启流式）
    llm = ChatOpenAI(
        model=QWEN_MODEL_NAME,
        base_url=QWEN_BASE_URL,
        temperature=0.3,
        streaming=True  # 关键：开启流式
    )
    llm_with_tools = llm.bind_tools(tools)

    system_prompt = SystemMessage(content="""你是一个智能助手，可以调用工具来获取实时信息。

可用工具：
- get_current_time：获取当前真实时间
- get_weather：获取指定城市的实时天气

规则：
- 如果用户需要实时数据，调用对应的工具
- 如果不需要工具，直接回答问题
- 绝对不要编造时间和天气信息""")

    # 节点1：决策 + 回复生成
    def call_model(state: AgentState):
        messages = [system_prompt] + state["messages"]
        response = llm_with_tools.invoke(messages)
        if hasattr(response, "tool_calls") and response.tool_calls:
            next_action = "use_tools"
        else:
            next_action = "end"
        return {"messages": [response], "next_action": next_action}

    # 节点2：执行工具
    def call_tools(state: AgentState):
        last_message = state["messages"][-1]
        tool_messages = []

        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            logger.info(f"调用工具: {tool_name}({tool_args})")

            if tool_name in tools_by_name:
                result = tools_by_name[tool_name].invoke(tool_args)
            else:
                result = f"错误：未找到工具 {tool_name}"

            tool_messages.append(
                ToolMessage(
                    content=result,
                    tool_call_id=tool_call["id"]
                )
            )

        return {"messages": tool_messages}

    # 构建图
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tools)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        lambda state: state["next_action"],
        {
            "use_tools": "tools",
            "end": END
        }
    )

    workflow.add_edge("tools", "agent")

    app = workflow.compile(checkpointer=MemorySaver())
    return app


# ========== 主程序包装类 ==========

class WeatherAgent:
    """天气智能体包装类（支持流式输出）"""

    def __init__(self):
        self.app = create_weather_agent()
        self.config: RunnableConfig = {"configurable": {"thread_id": "weather_agent_session"}}
        self.message_count = 0

    def clear_memory(self):
        """清空对话记忆（重置 thread_id 和消息计数）"""
        import uuid
        self.app = create_weather_agent()
        self.config = {"configurable": {"thread_id": f"weather_agent_session_{uuid.uuid4().hex[:8]}"}}
        self.message_count = 0

    async def astream_chat(self, user_input: str) -> AsyncGenerator[str, None]:
        self.message_count += 1
        input_state = {"messages": [HumanMessage(content=user_input)]}

        async for event in self.app.astream_events(input_state, config=self.config, version="v2"):
            if event["event"] == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                # 防御性提取 content
                content = None
                if hasattr(chunk, "content"):
                    content = chunk.content
                elif isinstance(chunk, dict):
                    content = chunk.get("content")
                # 只输出有内容且不是工具调用的部分
                if content and not getattr(chunk, "tool_calls", None):
                    yield str(content)

    # ---------- 命令行交互（异步） ----------
    async def run(self):
        """异步命令行交互（支持流式输出）"""
        print("=" * 60)
        print("🤖 智能体已启动（LangGraph + 通义千问 + 流式输出）")
        print("功能：查询时间、查询天气")
        print("输入 'exit' 退出，输入 '/clear' 清空对话记忆")
        print("=" * 60)

        while True:
            user_input = input("\n👤 你: ").strip()
            if user_input.lower() == 'exit':
                print("👋 再见！")
                break
            elif user_input.lower() == '/clear':
                self.clear_memory()
                print("🗑️ 对话记忆已清空")
                continue

            try:
                # 流式输出
                print("🤖 助手: ", end="", flush=True)
                async for chunk in self.astream_chat(user_input):
                    print(chunk, end="", flush=True)
                print()  # 换行
            except Exception as e:
                logger.error(f"对话处理失败: {e}")
                print(f"\n🤖 助手: 抱歉，处理您的请求时出现了问题：{e}")


if __name__ == "__main__":
    agent = WeatherAgent()
    asyncio.run(agent.run())