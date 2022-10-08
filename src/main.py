import string
import time
import random

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from .pages import user
from .pages import auth
from .pages import wallets


app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(wallets.router)


# @app.options('/')
# @app.head('/')
@app.get("/")
async def root():
    return {"status": "OK"}


