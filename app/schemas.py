from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #default value
    
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    published: bool

class PostResponseBase(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse

    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    Post: PostResponseBase
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
class LoginResponse(Token):
    user_id: int
    first_name: str
    last_name: str
class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    vote_dir: conint(le=1, ge=0) # less than or equal 1, greater than or equal to 0 (constrained to 0 and 1)
