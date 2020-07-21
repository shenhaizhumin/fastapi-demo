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
from pydantic import BaseModel
from app.models.user_info import UserInfo

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


class MsgMode(BaseModel):
    user_id: int
    friend_id: int
    content: str

    class Config:
        orm_mode = True


@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, current_user: UserInfo = Depends(get_current_user)):
    await websocket.accept()
    clients.append({current_user.id: websocket})
    while True:
        data = await websocket.receive_json(mode='text')
        user_id = data['user_id']  # 发送者
        friend_id = data['friend_id']  # 接收者
        content = data['content']  # 发送内容
        for c in clients:
            '''
            chatMsg.content = msg
                chatMsg.friend_id = friendId
                chatMsg.user_id = userId
                chatMsg.ismineChat = 0
                chatMsg.post_date = Date()
            '''
            client = c[friend_id]  # 找到接收者的客户端
            if client:
                await client.send_text(MsgMode.from_orm(**data))  # 下发消息
