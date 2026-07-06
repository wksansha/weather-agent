"""
Web 服务器 - 为天气智能体提供聊天界面（静态 HTML 版本）
"""

import asyncio
import json
import os

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, StreamingResponse, PlainTextResponse
from weather_plus import WeatherAgent

app = FastAPI(title="天气智能体 Web 聊天")
agent = WeatherAgent()
agent_lock = asyncio.Lock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 脚本所在目录
DOCS_DIR = BASE_DIR  # 限定可访问的文档根目录


# ---------- 路由 ----------
@app.get("/")
async def get_chat_page():
    return FileResponse(os.path.join(BASE_DIR, "templates", "index.html"))


@app.post("/chat_stream")
async def chat_stream(request: Request):
    """流式对话接口（SSE）"""
    data = await request.json()
    user_message = data.get("message", "")

    async def event_generator():
        try:
            async for chunk in agent.astream_chat(user_message):
                if not isinstance(chunk, str):
                    chunk = str(chunk)
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/docs/{file_name}")
async def get_md_file(file_name: str):
    """返回指定 Markdown 文件的内容（纯文本）"""
    # 防止路径穿越：只取文件名部分
    safe_name = os.path.basename(file_name)
    file_path = os.path.join(DOCS_DIR, safe_name)

    # 二次确认解析后的路径在允许的目录内（commonpath 在 Windows 上不区分大小写）
    real_path = os.path.abspath(file_path)
    if os.path.commonpath([real_path, DOCS_DIR]) != os.path.abspath(DOCS_DIR):
        raise HTTPException(status_code=403, detail="禁止访问")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文档不存在")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except PermissionError:
        raise HTTPException(status_code=403, detail="无权读取该文件")
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"读取文件失败: {e}")

    return PlainTextResponse(content)


@app.post("/clear")
async def clear_memory():
    """清空对话记忆"""
    async with agent_lock:
        agent.clear_memory()
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
