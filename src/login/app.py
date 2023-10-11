from fastapi import FastAPI, Request, HTTPException, Response, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from models import Base, User
import jwt
import logging
import time
from config import DATABASE_URL, SECRET_KEY, JWT_EXPIRATION_SECONDS

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post('/login')
def login(request: LoginRequest):
    username = request.username
    password = request.password
    user_id = authenticate_user(username, password)

    if user_id:
        token = generate_jwt(user_id)
        return JSONResponse(content={"jwt_token": token}, status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def authenticate_user(username, password):
    session = DBSession()
    user = session.query(User).filter_by(username=username, password=password).first()
    logger.info(f"user")
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
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)

