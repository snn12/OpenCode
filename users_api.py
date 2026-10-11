from flask import Flask, request, jsonify
app = Flask(__name__)
users = {1: {"id": 1, "name": "Senan"}}
@app.route('/users', methods=['GET'])
def l():
    return jsonify(list(users.values()))
@app.route('/users', methods=['POST'])
def c():
    d = request.get_json(force=True)
    nid = max(users) + 1
    users[nid] = {"id": nid, "name": d.get("name", "Anon")}
    return jsonify(users[nid]), 201
if __name__ == '__main__':
    app.run(port=5003)
