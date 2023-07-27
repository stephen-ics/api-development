from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

import redis.asyncio as aioredis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from .database import engine
from . import models
from .routers import post, user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

origins = ["*"] # Disables cors for all domains --> security issue will change later

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def initialize_rate_limiter(app: FastAPI, redis_url: str):
    @app.on_event('startup')
    async def startup():
        print('woop woop!')
        redis = await aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(redis)

initialize_rate_limiter(app, "redis://localhost:6379")

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {"message": "Hello World! 1333"}


