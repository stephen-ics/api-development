from fastapi import FastAPI, Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #default value
    rating: Optional[int] = None

my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1}, {'title': 'favourite foods', 'content': 'I like pizza', 'id':2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get('/')
def root():
    return {"message": "Hello World"}

@app.get('/posts')
def get_posts():
    return {"data" : my_posts}

@app.post('/posts', status_code=201)
def create_posts(post: Post): # Store all data in body as python dictionary named payLoad
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {'data': post_dict}  

@app.get('/posts/latest') # Move it up because {variable} matches latest but latest will never match an id
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {'detail': post}

@app.get('/posts/{id}') 
def  get_post(id: int, response: Response): # automatically convert to integer if possible
    post = find_post(id) # IDs are returned as a string, needs to be converted to int
    if not post: # If post = none/null
        raise HTTPException(status_code=404, 
                            detail=f'post with id: {id} was not found')
    return {'post_detail': post}

@app.delete('/posts/{id}', status_code=204)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=404, 
                            detail=f"post with id: {id} does not exist")
    
    my_posts.pop(index)
    return Response(status_code=204)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=404,
                            detail=f'post with id: {id} does not exist')
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}


def hello():
    print("tesitng git push")