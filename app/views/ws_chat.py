from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket
from app.static.web_html import html
# 基于类的视图模式来处理HTTP方法和WebSocket会话。
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.responses import HTMLResponse
# 路由
from starlette.routing import Route, WebSocketRoute
from app.intercept import get_current_user



ws_router = APIRouter()


# class Echo(WebSocketEndpoint):
#     encoding = "text"
#
#     # 连接
#     async def on_connect(self, websocket):
#         print('客户端连接：{}'.format(websocket.client.host))
#         await websocket.accept()
#
#     # 收发
#     async def on_receive(self, websocket, data):
#         print('收到消息：{}'.format(data))
#         await websocket.send_text(f"Message text was: {data}")
#
#     # 断开
#     async def on_disconnect(self, websocket, close_code):
#         print('断开连接：{}'.format(websocket.client.host))
#         pass


# @app.get("/")告诉FastAPI如何去处理请求
# 路径 /
# 使用get操作
@ws_router.get("/")
async def get():
    # 返回表单信息
    return HTMLResponse(html)

clients = []


class MsgMode(object):
    def __init__(self, user_id, to_id, msg):
        self.user_id = user_id
        self.to_id = to_id
        self.msg = msg


@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_json(mode='text')
        for c in clients:
            await c.send_text(f" {data['msg']}")
