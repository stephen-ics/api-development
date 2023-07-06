from fastapi import FastAPI, Response, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #default value

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
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""
    #    SELECT *
    #    FROM posts
    # """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    return {'data': posts}  

@app.post('/posts', status_code=201)
def create_posts(post: Post, db: Session = Depends(get_db)): # Store all data in body as python dictionary named payLoad
    # cursor.execute("""
    #    INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) 
    #    RETURNING * 
    # """, (post.title, post.content, post.published)) # %s Represents variable
    
    # new_post = cursor.fetchone()
    # conn.commit()'

    new_post = models.Post(
        **post.dict()
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'data': new_post}  

@app.get('/posts/{id}') 
def  get_post(id: int, db: Session = Depends(get_db)): # automatically convert to integer if possible
    # cursor.execute("""
    #    SELECT * 
    #    FROM posts
    #    WHERE posts.id = %s
    # """, (id,))

    # one_post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=404, detail=f'post with id: {id} was not found')
    return {'post_detail': post}

@app.delete('/posts/{id}', status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""
    #    DELETE
    #    FROM posts
    #    WHERE posts.id = %s
    #    RETURNING *
    # """, (id,))

    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=404, 
                            detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=204)

@app.put('/posts/{id}')
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""
    #    UPDATE posts
    #    SET title = %s, content = %s, published = %s
    #    WHERE id = %s
    #    RETURNING *
    # """, (post.title, post.content, post.published, id))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404,
                            detail=f'post with id: {id} does not exist')
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return {'data': post_query.first()}

