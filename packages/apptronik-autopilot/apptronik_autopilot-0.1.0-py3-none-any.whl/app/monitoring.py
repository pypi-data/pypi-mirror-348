from prometheus_client import start_http_server, Counter

api_calls = Counter('api_calls_total', 'Total API calls')

def start_metrics_server(port=8001):
    """Start Prometheus metrics server on the given port."""
    start_http_server(port) 