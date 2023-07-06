from fastapi import FastAPI, Response, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from random import randrange
import psycopg
from .database import engine, get_db
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

try:
    conn = psycopg.connect("dbname=apis user=postgres password=password123")
    cursor = conn.cursor()
    print('Connected to database!')
except Exception as error:
    print('Connecting to database failed')
    print('Error', error)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {"message": "Hello World"}


