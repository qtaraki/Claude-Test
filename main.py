from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello_world():
    return {"message": "Hello World"}


@app.get("/{path:path}")
def catch_all(path: str):
    return {"message": path}
