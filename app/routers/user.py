from fastapi import FastAPI, Response, HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', status_code=201, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hask the password - user.password

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
    
@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {id} does not exist")

    return user

@router.put('/password-reset')
def reset_user_password(user_credentials: schemas.UserPasswordReset, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {id} does not exist")

    if not utils.verify(user_credentials.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    if user_credentials.new_password == user_credentials.old_password:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'New password must be different from old password')
    
    new_hashed_password = utils.hash(user_credentials.new_password)
    updated_password = {"password": new_hashed_password}

    user_query.update(updated_password, synchronize_session=False)
    db.commit()

    return {'message': 'password successfully changed!'}


