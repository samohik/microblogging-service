import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi_users import FastAPIUsers
from starlette.responses import JSONResponse

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserRead, UserCreate
from database import Base, engine
from routers import tweet, user
from fastapi import Request
from routers.user import fastapi_users


app = FastAPI(title="My FastApi", description="FastApi")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/protected-route", tags=['authorization'])
def protected_route(user: User = Depends(fastapi_users.current_user())):
    return f"Hello, {user.name}"


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


app.include_router(tweet.router)
app.include_router(user.router)
# app.include_router(
#     media.router
# )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
