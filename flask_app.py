from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
ORDERS = Counter('shop_orders_total', 'Real sifaris sayi')

@app.route('/')
def home():
    ORDERS.inc()
    return 'Sifaris qebul edildi!'

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(port=5000)
