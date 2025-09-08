from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
import DB, security, schemas, models
from security import get_current_user

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/token', response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(DB.get_session),
):
    user = session.scalar(
        select(models.User).where(models.User.username == form_data.username)
    )

    if not user or not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    access_token = security.create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=schemas.Token)
def refresh_access_token(user: Annotated[models.User, Depends(get_current_user)]):
    new_access_token = security.create_access_token(data={'sub': user.username})

    return {'access_token': new_access_token, 'token_type': 'bearer'}