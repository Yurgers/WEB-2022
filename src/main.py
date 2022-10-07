import string
import time
import random

from fastapi import FastAPI, Request

from .pages import user
from .pages import auth

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"status": "OK"}
