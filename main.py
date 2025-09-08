# loja/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from http import HTTPStatus
from routers import users, auth, products, sales
from schemas import Message

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(sales.router)

@app.get('/', status_code=HTTPStatus.OK)
def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

@app.get('/login', status_code=HTTPStatus.OK)
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@app.get('/register', status_code=HTTPStatus.OK)
def register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})

# A rota abaixo foi alterada de '/products' para '/products-page'
@app.get('/products-page', status_code=HTTPStatus.OK)
def products_page(request: Request):
    return templates.TemplateResponse('products.html', {'request': request})

@app.get('/create-product-page', status_code=HTTPStatus.OK)
def create_product_page(request: Request):
    return templates.TemplateResponse('create_product.html', {'request': request})

@app.get('/update-product-page', status_code=HTTPStatus.OK)
def update_product_page(request: Request):
    return templates.TemplateResponse('update_product.html', {'request': request})

@app.get('/delete-product-page', status_code=HTTPStatus.OK)
def delete_product_page(request: Request):
    return templates.TemplateResponse('delete_product.html', {'request': request})

@app.get('/sales', status_code=HTTPStatus.OK)
def sales_page(request: Request):
    return templates.TemplateResponse('sales.html', {'request': request})

@app.get('/accounting', status_code=HTTPStatus.OK)
def accounting_page(request: Request):
    return templates.TemplateResponse('accounting.html', {'request': request})