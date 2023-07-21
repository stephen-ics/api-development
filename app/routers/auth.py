from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.LoginResponse)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    
    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id, "first_name": user.first_name, "last_name": user.last_name}
    # Change bearer 1 back to bearer after test


@router.get('/login')
def check_login(current_user: int = Depends(oauth2.get_current_user)):
    return {'message': 'successfully logged in'}

