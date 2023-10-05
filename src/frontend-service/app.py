from flask import Flask, render_template, redirect, url_for, jsonify, request
import requests
from config import PRODUCT_SERVICE_URL, USER_SERVICE_URL, ORDER_SERVICE_URL, SECRET_KEY
import logging
import jwt
app = Flask(__name__)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_user_id_from_jwt(jwt_token):
    try:
        decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/products')
def products():

    jwt_token = request.args.get('token')

    logger.info(f"Token: {jwt_token}")

    if jwt_token:
        headers = {
            'Authorization': f"Bearer {jwt_token}"
        }

    logger.info(f"Headers: {headers}")

    response = requests.get(PRODUCT_SERVICE_URL, headers=headers)
    if response.status_code == 200:
        products_data = response.json()
        return render_template('products.html', products=products_data)
    else:
        return f"Failed to fetch products. Error: {response.status_code}, {response.headers}, {response.text}"

@app.route('/user/info')
def user_info():

    jwt_token = request.args.get('token')

    if jwt_token:
        headers = {
            'Authorization': f"Bearer {jwt_token}"
        }

    user_id = extract_user_id_from_jwt(jwt_token)

    user_response = requests.get(f"{USER_SERVICE_URL}/{user_id}", headers=headers)
    if user_response.status_code == 200:
        user_data = user_response.json()
        logger.info(f"{user_data}")

        # Fetch user orders from the Order Service
        order_response = requests.get(ORDER_SERVICE_URL, headers=headers)
        if order_response.status_code == 200:
            orders_data = order_response.json()
            logger.info(f"{orders_data}")
            return render_template('user_info.html', user=user_data, orders=orders_data)
        else:
            return f"Failed to fetch orders. Error: {order_response.status_code}"
    else:
        return f"Failed to fetch user information. Error: {user_response.status_code}, {user_response.headers}, {user_response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)

