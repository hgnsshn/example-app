
from fastapi import FastAPI, Request, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
import jwt
import logging
from config import DATABASE_URL, SECRET_KEY

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
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        logger.info("JWT Token Decoded Successfully")
        logger.info(f"Payload: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

@app.get('/users/{user_id}')
def get_user(user_id: int, authorization: str = Header(None)):
    jwt_token = extract_token(authorization)
    payload = verify_jwt(jwt_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    if int(payload['user_id']) != user_id:
        raise HTTPException(status_code=403, detail="Token user ID does not match requested user ID")

    session = DBSession()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()

    if user:
        return user.to_json()
    else:
        raise HTTPException(status_code=404, detail="User not found")

