from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Order
import requests
import jwt
import logging
from config import SECRET_KEY, DATABASE_URL, USER_SERVICE_URL, PRODUCT_SERVICE_URL
app = Flask(__name__)

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_token(authorization_header):
    if authorization_header and authorization_header.startswith("Bearer "):
        return authorization_header[len("Bearer "):]
    return None


def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        logger.info("JWT Token Decoded Successfully")
        logger.info(f"Payload: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

@app.route('/orders', methods=['GET'])
def get_all_orders():

    session = DBSession()
    orders = session.query(Order).options(joinedload(Order.product)).all()

    orders_json = [{
        "id": order.id,
        "product_name": order.product.name if order.product else None,
        "quantity": order.quantity
    } for order in orders]

    session.close()

    return jsonify(orders_json), 200

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):

    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return jsonify({"error": "Authorization header missing"}), 401

    jwt_token = extract_token(authorization_header)

    payload = verify_jwt(jwt_token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401

    session = DBSession()
    order = session.query(Order).filter_by(id=order_id).first()
    session.close()
    if order:
        # Fetch user details from User Service
        headers = {"Authorization": f"Bearer {jwt_token}"}
        user_response = requests.get(f'{USER_SERVICE_URL}/{order.user_id}', headers=headers)

        if int(payload['user_id']) != order.user_id:
            return jsonify({"error": "Token user ID does not match requested user ID"}), 403

        user_details = user_response.json()

        # Fetch product details from Product Service
        headers = {"Authorization": f"Bearer {jwt_token}"}
        product_response = requests.get(f'{PRODUCT_SERVICE_URL}/{order.product_id}', headers=headers)
        product_details = product_response.json()

        # Combine order data with user and product details
        order_data = order.to_json()
        order_data["user"] = user_details
        order_data["product"] = product_details

        return jsonify(order_data), 200
    else:
        return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

