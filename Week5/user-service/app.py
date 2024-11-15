from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'user_db'),
        user=os.getenv('DB_USER', 'user'),
        password=os.getenv('DB_PASSWORD', 'password')
    )
    return conn

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO users (username, email) VALUES (%s, %s)', (username, email))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful", "user": user[1]}), 200
    else:
        return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
