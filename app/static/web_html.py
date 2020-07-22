

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off" placeholder="" />
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            document.getElementById("messageText").placeholder="第一次输入内容为昵称";
        
            var ws = new WebSocket("ws://39.107.77.70:8888/ws");
            
            // 接收
            ws.onmessage = function(event) {
                // 获取id为messages的ul标签内
                var messages = document.getElementById('messages')
                // 创建li标签
                var message = document.createElement('li')
                // 创建内容
                var content = document.createTextNode(event.data)
                // 内容添加到li标签内
                message.appendChild(content)
                // li标签添加到ul标签内
                messages.appendChild(message)
            };
            
            var name = 0;
            // 发送
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
                
                if (name == 0){
                    document.getElementById("messageText").placeholder="";
                    name = 1;
                }
            }
        </script>
    </body>
</html>
"""