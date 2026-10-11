from flask import Flask, request, jsonify

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

if __name__ == '__main__':
    app.run(port=5002)
