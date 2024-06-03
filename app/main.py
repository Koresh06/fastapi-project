from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.api_v1.user.views import router as user_router
from api.api_v1.auth.views import router as auth_router
from core.config import settings
from core.models import db_helper
from core.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    #shutdown
    await db_helper.dispose()



main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

main_app.include_router(
    user_router,
    prefix=settings.api.v1.users,
    )

main_app.include_router(
    auth_router,
    prefix=settings.api.v1.auth,
    )


@main_app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", 
        host=settings.run.host,
        port=settings.run.port,
    )