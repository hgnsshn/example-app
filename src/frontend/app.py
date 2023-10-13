from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import logging
import jwt
import os

USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL')
PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL')
ORDER_SERVICE_URL = os.environ.get('ORDER_SERVICE_URL')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_user_id_from_jwt(jwt_token):
    try:
        decoded_token = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/home")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/products")
def products(request: Request, token: str = None):
    headers = {'Authorization': f"Bearer {token}"} if token else {}
    response = requests.get(PRODUCT_SERVICE_URL, headers=headers)

    if response.status_code == 200:
        products_data = response.json()
        return templates.TemplateResponse("products.html", {"request": request, "products": products_data})
    else:
        return f"Failed to fetch products. Error: {response.status_code}, {response.headers}, {response.text}"

@app.get("/user/info")
def user_info(request: Request, token: str = None):
    headers = {'Authorization': f"Bearer {token}"} if token else {}
    user_id = extract_user_id_from_jwt(token)

    user_response = requests.get(f"{USER_SERVICE_URL}/{user_id}", headers=headers)

    if user_response.status_code == 200:
        user_data = user_response.json()
        return templates.TemplateResponse("user_info.html", {"request": request, "user": user_data})
    else:
        return f"Failed to fetch user information. Error: {user_response.status_code}"

@app.get("/user/orders")
def user_info(request: Request, token: str = None):
    headers = {'Authorization': f"Bearer {token}"} if token else {}
    user_id = extract_user_id_from_jwt(token)

    order_response = requests.get(ORDER_SERVICE_URL, headers=headers)

    if order_response.status_code == 200:
        orders_data = order_response.json()
        return templates.TemplateResponse("orders.html", {"request": request, "orders": orders_data})
    else:
        return f"Failed to fetch orders. Error: {order_response.status_code}, {order_response.text}"
