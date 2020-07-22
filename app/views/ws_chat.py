from typing import Optional, Set, List
import datetime
import time

from fastapi import Cookie, Depends, APIRouter, Query, WebSocket, status
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket
from app.static.web_html import html
# 基于类的视图模式来处理HTTP方法和WebSocket会话。
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.responses import HTMLResponse
# 路由
from starlette.routing import Route, WebSocketRoute
from app.intercept import get_current_user
from pydantic import BaseModel, Field
from app.models.user_info import UserInfo
import json
from app.response import BaseError, BaseResponse

'''
chatMsg.content = msg
                chatMsg.friend_id = friendId
                chatMsg.user_id = userId
                chatMsg.ismineChat = 0 //发送者标记为自己
                chatMsg.post_date = Date()'''


class P2pMessage(BaseModel):
    user_id: int = Field(None)
    friend_id: int = Field(None)
    content: str = Field(None)
    post_date: int = Field(None)

    class Config:
        orm_mode = True


class WsEntity(object):
    def __init__(self, websocket, user_id):
        self.ws = websocket
        self.user_id = user_id

    def __eq__(self, other):
        if not isinstance(other, WsEntity):
            return False
        return self.user_id == other.user_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.ws) + hash(self.user_id)


clients = []


class Homepage(HTTPEndpoint):
    async def get(self, request):
        return HTMLResponse(html)


class Echo(WebSocketEndpoint):
    encoding = "text"

    # 修改socket
    async def alter_socket(self, websocket):
        socket_str = str(websocket)[1:-1]
        socket_list = socket_str.split(' ')
        socket_only = socket_list[3]
        return socket_only

    # 连接 存储
    async def on_connect(self, websocket):
        await websocket.accept()

        # 用户输入名称
        user_info = await websocket.receive_json()
        if not user_info or type(user_info) != dict:
            await websocket.send_json({'msg': '无法识别的用户连接'})
        else:
            print(user_info)
            # socket_only = await self.alter_socket(websocket)
            # 添加连接池 保存用户名
            user_id = user_info['user_id']
            ws_entity = WsEntity(websocket, user_id)
            if ws_entity in clients:
                for c in clients:
                    if c.user_id == user_id:
                        c.ws = websocket
            else:
                clients.append(ws_entity)

            # 先循环 告诉之前的用户有新用户加入了
            # for wbs in info:
            #     await info[wbs][1].send_text(f"{info[socket_only][0]}-加入了聊天室")

            print(clients)

    # 收发
    async def on_receive(self, websocket, data):
        # socket_only = await self.alter_socket(websocket)
        if len(clients) == 0:
            await websocket.send_text('invalid message')
        else:
            data = json.loads(data)
            if data and type(data) == dict:
                friend_id = data['friend_id']
                user_id = data['user_id']
                content = data['content']
                # send_ws = clients[user_id]  # 发送者
                for wsEntity in clients:
                    if wsEntity.user_id == friend_id:
                        # 拼接消息
                        msg = P2pMessage(user_id=user_id, friend_id=friend_id, content=content,
                                         post_date=int(time.time() * 1000))
                        receive_ws = wsEntity.ws  # 接收者
                        await receive_ws.send_text(msg.json().__str__())
            else:
                await websocket.send_text('无效的消息格式')

    # 断开 删除
    async def on_disconnect(self, websocket, close_code):
        # socket_only = await self.alter_socket(websocket)
        # 删除连接池
        for entity in clients:
            if entity.ws == websocket:
                clients.remove(entity)
                print("user_id:{} disconnected".format(entity.user_id))
        # clients.pop(socket_only)
        # print(info)
        pass


ws_router = APIRouter()
# @app.get("/")告诉FastAPI如何去处理请求
# 路径 /
# 使用get操作
# @ws_router.get("/")
# async def get():
#     # 返回表单信息
#     return HTMLResponse(html)


clients = []


async def get_cookie_or_token(
        websocket: WebSocket,
        session: Optional[str] = Cookie(None),
        token: Optional[str] = Query(None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, current_user: UserInfo = Depends(get_current_user)):
    await websocket.accept()
    # print(websocket.user)
    # clients.append({current_user.id: websocket})
    clients.append(websocket)
    while True:
        data = await websocket.receive_json(mode='text')
        # user_id = data['user_id']  # 发送者
        # friend_id = data['friend_id']  # 接收者
        # content = data['content']  # 发送内容
        for c in clients:
            '''
            chatMsg.content = msg
                chatMsg.friend_id = friendId
                chatMsg.user_id = userId
                chatMsg.ismineChat = 0
                chatMsg.post_date = Date()
            '''
            # client = c[friend_id]  # 找到接收者的客户端
            # if client:
            # await c.send_text(MsgMode.from_orm(**data))  # 下发消息
            await c.send_text(data['msg'])  # 下发消息
