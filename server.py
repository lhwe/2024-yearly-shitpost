from flask import Flask, request, jsonify
import json
import bcrypt

app = Flask(__name__)

with open('database.json', 'r') as database:
    db = json.load(database)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def save_db():
    with open('database.json', 'w') as database:
        json.dump(db, database, indent=4)

def is_user_banned(username):
    return username in db.get("banned", {})

@app.route('/jeff')
def jeff():
    return '<video src="https://files.catbox.moe/0f88pf.mp4">'

@app.route('/api/check_ban', methods=['POST'])
def check_ban():
    data = request.json
    if not data or 'username' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    username = data["username"]
    if is_user_banned(username):
        reason = db["banned"][username]["reason"]
        return jsonify({'ban_message': f'This user has been banned for "{reason}", to appeal please contact support.'}), 200
    else:
        return jsonify({'message': f'{username} is not banned.'}), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    
    username = data['username']
    password = data['password']

    if is_user_banned(username):
        return jsonify({'error': f'You have been banned for "{db["banned"][username]["reason"]}", contact the staff team to appeal.'}), 400

    if username in db["users"] and verify_password(password, db["users"][username]):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    
    username = data['username']
    password = data['password']

    if username in db["users"]:
        return jsonify({'error': 'Username already exists'}), 409
    
    if username not in db["banned"]:
        pass
    else:
        return jsonify({'error': 'User with this username has already been banned.'}), 409

    hashed_password = hash_password(password)
    db["users"][username] = hashed_password
    save_db()

    return jsonify({'message': 'Registration successful'}), 201

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0')
