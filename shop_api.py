from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
orders = {}
next_id = 1

@app.route('/orders', methods=['GET'])
def list_orders():
    return jsonify(list(orders.values()))

@app.route('/orders', methods=['POST'])
def create_order():
    global next_id
    data = request.get_json(force=True)
    order = {"id": next_id, "item": data.get("item", "PC")}
    orders[next_id] = order
    next_id += 1
    return jsonify(order), 201

@app.route('/orders/<int:oid>', methods=['GET'])
def get_order(oid):
    o = orders.get(oid)
    if not o:
        return jsonify({"error": "tapilmadi"}), 404
    return jsonify(o)

@app.route('/orders/<int:oid>', methods=['PUT'])
def update_order(oid):
    o = orders.get(oid)
    if not o:
        return jsonify({"error": "tapilmadi"}), 404
    data = request.get_json(force=True)
    o["item"] = data.get("item", o["item"])
    return jsonify(o)

@app.route('/orders/<int:oid>', methods=['DELETE'])
def delete_order(oid):
    if oid in orders:
        del orders[oid]
        return '', 204
    return jsonify({"error": "tapilmadi"}), 404

@app.route('/feed', methods=['GET'])
def feed():
    try:
        u = requests.get('http://localhost:5003/users', timeout=3).json()
    except Exception as e:
        u = {"error": str(e)}
    return jsonify({"orders": list(orders.values()), "users": u})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
