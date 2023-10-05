from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
import jwt
import logging
import time
from config import DATABASE_URL, SECRET_KEY, JWT_EXPIRATION_SECONDS

app = Flask(__name__)
CORS(app)

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/login', methods=['POST'])
def login():

    username = request.json.get('username')
    password = request.json.get('password')
    user_id = authenticate_user(username, password)

    if user_id:
        token = generate_jwt(user_id)
        return jsonify({"jwt_token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

def authenticate_user(username, password):
    
    session = DBSession()
    user = session.query(User).filter_by(username=username, password=password).first()
    session.close()

    if user:
        return user.id
    else:
        return None


def generate_jwt(user_id, expiration_seconds=JWT_EXPIRATION_SECONDS):

    current_time = time.time()
    expiration_time = current_time + expiration_seconds

    payload = {
        "user_id": user_id,
        "exp": expiration_time
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

