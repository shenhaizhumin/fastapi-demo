from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/helloServer")
def hello(req: Request):
    return {
        'name': 'hello',
        'content': 'world'
        # 'remote_host':req.remote
    }


import uvicorn

uvicorn.run(app)
