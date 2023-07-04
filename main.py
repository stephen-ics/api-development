from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #default value
    rating: Optional[int] = None

@app.get('/')
def root():
    return {"message": "Hello World"}

@app.get('/posts')
def get_posts():
    return {"data" : "This is your post"}

@app.post('/createposts')
def create_posts(new_post: Post): # Store all data in body as python dictionary named payLoad
    print(new_post.rating)
    return {'data': 'new post'}

# title string, content string
 