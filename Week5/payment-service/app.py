from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

def get_redis_connection():
    return redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0)

@app.route('/payments', methods=['POST'])
def process_payment():
    data = request.get_json()
    order_id = data['order_id']
    amount = data['amount']

    payment_status = "Success"
    
    redis_conn = get_redis_connection()
    redis_conn.set(f"payment:{order_id}", payment_status)
    
    return jsonify({"message": "Payment processed", "status": payment_status}), 201

@app.route('/payments/<order_id>', methods=['GET'])
def get_payment_status(order_id):
    redis_conn = get_redis_connection()
    payment_status = redis_conn.get(f"payment:{order_id}")
    
    if payment_status:
        return jsonify({"order_id": order_id, "payment_status": payment_status.decode('utf-8')})
    else:
        return jsonify({"message": "Payment not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
