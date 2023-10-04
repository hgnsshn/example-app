from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product

app = Flask(__name__)

# PostgreSQL database configuration
DATABASE_URL = 'postgresql://antonv:password@localhost/exampleapp'
engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    session = DBSession()
    product = session.query(Product).filter_by(id=product_id).first()
    session.close()
    if product:
        return jsonify(product.to_json()), 200
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

