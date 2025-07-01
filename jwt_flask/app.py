from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
flag = "flag"

users = {
    "guest": {"password": "guest", "isAdmin": False},
    "admin": {"password": "admin", "isAdmin": True}
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if not user or user["password"] != password:
        return jsonify({"error": "bad login"}), 401

    token_data = {
        "username": username,
        "isAdmin": user["isAdmin"]
    }

    token = jwt.encode(token_data, key="", algorithm="none")
    return jsonify({"token": token})

@app.route('/admin')
def admin():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if not token:
        return jsonify({"error": "missing token"}), 401

    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
    except:
        return jsonify({"error": "invalid token"}), 401

    if decoded.get("isAdmin"):
        return jsonify({"flag": flag})
    return jsonify({"error": "not admin"}), 403

if __name__ == "__main__":
    app.run()
