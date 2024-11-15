from flask import Flask, request, jsonify
import mysql.connector
import os
import requests

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'password'),
        database=os.getenv('DB_NAME', 'order_db')
    )
    return conn

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']
    
    product_res = requests.get(f'http://product-service:5002/products/{product_id}')
    
    if product_res.status_code == 200:
        product_data = product_res.json()
        total_price = product_data['price'] * quantity
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO orders (product_id, quantity, total_price) VALUES (%s, %s, %s)', 
                       (product_id, quantity, total_price))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Order created", "total_price": total_price}), 201
    else:
        return jsonify({"message": "Product not found"}), 404

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_id = %s', (order_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if order:
        return jsonify({"order_id": order[0], "product_id": order[1], "quantity": order[2], "total_price": order[3]})
    else:
        return jsonify({"message": "Order not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
