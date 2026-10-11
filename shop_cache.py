from flask import Flask, request, jsonify
import requests, json, time

app = Flask(__name__)
orders = {}
next_id = 1
DB_TIME = 0.5   # "bazanin yavasligi" - simulyasiya
CACHE_TTL = 30  # saniye

def cache_get(key):
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=0.3)
        v = r.get(key)
        return json.loads(v) if v else None
    except Exception:
        return None

def cache_set(key, val):
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=0.3)
        r.setex(key, CACHE_TTL, json.dumps(val))
    except Exception:
        pass

def db_read():
    time.sleep(DB_TIME)   # DB yavasdir
    return list(orders.values())

@app.route('/orders')
def list_orders():
    t0 = time.time()
    hit = cache_get('orders')
    if hit is not None:
        return jsonify({"source": "REDIS", "ms": round((time.time()-t0)*1000, 1), "data": hit})
    data = db_read()
    cache_set('orders', data)
    return jsonify({"source": "DB", "ms": round((time.time()-t0)*1000, 1), "data": data})

@app.route('/orders', methods=['POST'])
def create_order():
    global next_id
    data = request.get_json(force=True)
    order = {"id": next_id, "item": data.get("item", "PC")}
    orders[next_id] = order
    next_id += 1
    try:
        import redis
        redis.Redis(host='localhost', port=6379).delete('orders')  # keş LOHANT
    except Exception:
        pass
    return jsonify(order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)