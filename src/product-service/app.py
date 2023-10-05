from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product
import jwt
import logging
import time
from config import DATABASE_URL, SECRET_KEY

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

@app.route('/products', methods=['GET'])
def get_all_products():

    session = DBSession()
    products = session.query(Product).all()
    session.close()

    products_json = [product.to_json() for product in products]
    return jsonify(products_json), 200

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):

    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return jsonify({"error": "Authorization header missing"}), 401

    jwt_token = extract_token(authorization_header)

    payload = verify_jwt(jwt_token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401

    session = DBSession()
    product = session.query(Product).filter_by(id=product_id).first()
    session.close()

    if product:
        return jsonify(product.to_json()), 200
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

