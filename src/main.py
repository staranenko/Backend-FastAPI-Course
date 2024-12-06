from fastapi import FastAPI
import uvicorn

from src.hotels import router as router_hotels

app = FastAPI(docs_url=None)

app.include_router(router_hotels)


@app.get("/")
def func():
    return "Hello World!"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
