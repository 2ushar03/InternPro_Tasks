from flask import Flask, jsonify
import pymongo
import os

app = Flask(__name__)

def get_db_connection():
    client = pymongo.MongoClient(os.getenv('DB_HOST', 'localhost'))
    db = client['product_db']
    return db

@app.route('/products', methods=['GET'])
def get_products():
    db = get_db_connection()
    products = db.products.find()
    
    product_list = []
    for product in products:
        product_list.append({"id": str(product['_id']), "name": product['name'], "price": product['price']})
    
    return jsonify(product_list)

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    db = get_db_connection()
    product = db.products.find_one({"_id": pymongo.ObjectId(product_id)})
    
    if product:
        return jsonify({"id": str(product['_id']), "name": product['name'], "price": product['price']})
    else:
        return jsonify({"message": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
