import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.config import settings


app = FastAPI()

app.include_router(
    api_router,
    prefix=settings.api.prefix,
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app")