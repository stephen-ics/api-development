from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, LargeBinary
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    parent_id = Column(Integer, nullable=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    image = Column(String, nullable=True)  
    published = Column(Boolean, nullable=True, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    biography = Column(String, nullable=True)
    profile_photo = Column(String, nullable=True, server_default=text("'https://firebasestorage.googleapis.com/v0/b/connectx-22806.appspot.com/o/images%2FDefaultpfp4.jpeg?alt=media&token=0ec8e6d7-9967-45f7-a8a0-401f4ec50ad4'"))
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 

class Vote(Base):
    __tablename__ = 'votes'
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)

