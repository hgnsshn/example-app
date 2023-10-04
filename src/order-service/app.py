from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Order
import requests

app = Flask(__name__)

# PostgreSQL database configuration
DATABASE_URL = 'postgresql://antonv:password@localhost/exampleapp'
engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# URLs for User Service and Product Service
USER_SERVICE_URL = 'http://localhost:5000/users'
PRODUCT_SERVICE_URL = 'http://localhost:5001/products'

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    session = DBSession()
    order = session.query(Order).filter_by(id=order_id).first()
    session.close()
    if order:
        # Fetch user details from User Service
        user_response = requests.get(f'{USER_SERVICE_URL}/{order.user_id}')
        user_details = user_response.json()

        # Fetch product details from Product Service
        product_response = requests.get(f'{PRODUCT_SERVICE_URL}/{order.product_id}')
        product_details = product_response.json()

        # Combine order data with user and product details
        order_data = order.to_json()
        order_data["user"] = user_details
        order_data["product"] = product_details

        return jsonify(order_data), 200
    else:
        return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

