from prometheus_client import Counter, start_http_server
import time

REQUESTS = Counter('myapp_requests_total', 'Test saygac')

if __name__ == '__main__':
    start_http_server(8000)
    print("Metrics: http://localhost:8000/metrics")
    while True:
        REQUESTS.inc()
        time.sleep(2)
