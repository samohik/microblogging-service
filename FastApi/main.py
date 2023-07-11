import uvicorn
from fastapi import FastAPI
from routers import tweet
from database import Base, engine


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


app.include_router(
    tweet.router
)
# app.include_router(
#     user.router
# )
# app.include_router(
#     like.router
# )
# app.include_router(
#     media.router
# )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
