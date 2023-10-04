from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User

app = Flask(__name__)

# PostgreSQL database configuration
DATABASE_URL = 'postgresql://antonv:password@localhost/exampleapp'
engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    if user:
        return jsonify(user.to_json()), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

