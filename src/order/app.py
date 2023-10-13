from fastapi import FastAPI, Request, Header, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Order
import requests
import jwt
import logging
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL')
PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL')

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

@app.get('/orders')
def get_all_orders(authorization: str = Header(None)):
    jwt_token = extract_token(authorization)
    payload = verify_jwt(jwt_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    session = DBSession()
    orders = session.query(Order).options(joinedload(Order.product)).all()

    orders_json = [{
        "id": order.id,
        "product_name": order.product.name if order.product else None,
        "quantity": order.quantity
    } for order in orders]

    session.close()

    return orders_json

@app.get('/orders/{order_id}')
def get_order(order_id: int, authorization: str = Header(None)):
    jwt_token = extract_token(authorization)
    payload = verify_jwt(jwt_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    session = DBSession()
    order = session.query(Order).filter_by(id=order_id).first()
    session.close()
    if order:
        headers = {"Authorization": f"Bearer {jwt_token}"}

        # Fetch user details from User Service
        user_response = requests.get(f'{USER_SERVICE_URL}/{order.user_id}', headers=headers)
        user_response.raise_for_status()
        user_details = user_response.json()

        if int(payload['user_id']) != order.user_id:
            raise HTTPException(status_code=403, detail="Token user ID does not match requested user ID")

        # Fetch product details from Product Service
        product_response = requests.get(f'{PRODUCT_SERVICE_URL}/{order.product_id}', headers=headers)
        product_response.raise_for_status()
        product_details = product_response.json()

        # Combine order data with user and product details
        order_data = {
            "id": order.id,
            "product_name": product_details.get('name'),
            "user": user_details,
            "quantity": order.quantity
        }

        return order_data

    else:
        raise HTTPException(status_code=404, detail="Order not found")
