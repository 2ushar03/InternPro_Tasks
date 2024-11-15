from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    user_data = request.get_json()
    response = requests.post('http://user-service:5001/register', json=user_data)
    return jsonify(response.json()), response.status_code

@app.route('/products', methods=['GET'])
def get_products():
    response = requests.get('http://product-service:5002/products')
    return jsonify(response.json()), response.status_code

@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.get_json()
    response = requests.post('http://order-service:5003/orders', json=order_data)
    return jsonify(response.json()), response.status_code

@app.route('/payments', methods=['POST'])
def process_payment():
    payment_data = request.get_json()
    response = requests.post('http://payment-service:5004/payments', json=payment_data)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
