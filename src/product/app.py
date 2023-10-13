from fastapi import FastAPI, Request, HTTPException, Header
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product
import jwt
import logging
import os

DATABASE_URL = os.environ.get('DATABASE_URL').strip('"')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY').strip('"')

app = FastAPI()

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_token(authorization: str = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        return authorization[len("Bearer "):]
    return None

def verify_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        logger.info("JWT Token Decoded Successfully")
        logger.info(f"Payload: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

@app.get('/products')
def get_all_products(authorization: str = Header(None)):
    jwt_token = extract_token(authorization)
    payload = verify_jwt(jwt_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    session = DBSession()
    products = session.query(Product).all()
    session.close()

    products_json = [product.to_json() for product in products]
    return products_json

@app.get('/products/{product_id}')
def get_product(product_id: int, authorization: str = Header(None)):
    jwt_token = extract_token(authorization)
    payload = verify_jwt(jwt_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    session = DBSession()
    product = session.query(Product).filter_by(id=product_id).first()
    session.close()

    if product:
        return product.to_json()
    else:
        raise HTTPException(status_code=404, detail="Product not found")

