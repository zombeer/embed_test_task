from config import ENABLE_CORS, REMOTE_URL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.utils import create_tables

from server.endpoints.auth import auth_router
from server.endpoints.posts import router as posts_router
from server.endpoints.subscriptions import router as subscriptions_router
from server.endpoints.user import router as user_router
from server.endpoints.users import router as users_router

create_tables()

app = FastAPI(
    title="Embed.xyz test API",
    description="Some basic user-post CRUD API example...",
    contact={"email": "zombeer@gmail.com"},
    version="0.1.0",
    servers=[{"url": REMOTE_URL}],
)

if ENABLE_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_headers=["*"],
        allow_methods=["*"],
        allow_credentials=True,
    )

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(user_router)
app.include_router(posts_router)
app.include_router(subscriptions_router)
