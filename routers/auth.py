# loja/routers/auth.py
from http import HTTPStatus

from typing import Annotated

from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas import Token
from security import verify_password,create_access_token,get_current_user
from DB import get_session
from models import User

from sqlalchemy import select
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/auth', tags=['auth']
)
CurrentUser = Annotated[User, Depends(get_current_user)]
@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(User.username == form_data.username) # <--- Linha corrigida para buscar por email
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'bearer'}

@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser):
    new_access_token = create_access_token(data={'sub': user.username})

    return {'access_token': new_access_token, 'token_type': 'bearer'}