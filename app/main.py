from fastapi import FastAPI, Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg


app = FastAPI(debug=True)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #default value
    rating: Optional[int] = None

try:
    conn = psycopg.connect("dbname=apis user=postgres password=password123")
    cursor = conn.cursor()
    print('Connected to database!')
except Exception as error:
    print('Connecting to database failed')
    print('Error', error)

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
    cursor.execute("""
        SELECT *
        FROM posts
    """)
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}  

@app.post('/posts', status_code=201)
def create_posts(post: Post): # Store all data in body as python dictionary named payLoad
    cursor.execute("""
        INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) 
        RETURNING * 
    """, (post.title, post.content, post.published)) # %s Represents variable
    
    new_post = cursor.fetchone()
    conn.commit()

    return {'data': new_post}  

@app.get('/posts/{id}') 
def  get_post(id: int): # automatically convert to integer if possible
    cursor.execute("""
        SELECT * 
        FROM posts
        WHERE posts.id = %s
    """, (id,))

    one_post = cursor.fetchone()

    if one_post is None:
        raise HTTPException(status_code=404, detail=f'post with id: {id} was not found')
    return {'post_detail': one_post}

@app.delete('/posts/{id}', status_code=204)
def delete_post(id: int):
    cursor.execute("""
        DELETE
        FROM posts
        WHERE posts.id = %s
        RETURNING *
    """, (id,))

    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=404, 
                            detail=f"post with id: {id} does not exist")
    
    return Response(status_code=204)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("""
        UPDATE posts
        SET title = %s, content = %s, published = %s
        WHERE id = %s
        RETURNING *
    """, (post.title, post.content, post.published, id))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=404,
                            detail=f'post with id: {id} does not exist')
    
    return {'data': updated_post}

