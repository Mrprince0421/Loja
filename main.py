from fastapi import FastAPI

from http import HTTPStatus
from schemas import Message
from  routers import users,auth

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


