import time
import random
import threading
import sys

from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

from flask import Flask, Response




app = Flask('instrumented-python-app')

REQUEST_COUNT = Counter(
    'python_app_requests_total',
    'Total number of user-facing requests processed',
    ['endpoint', 'method']
)

QUEUE_SIZE_GAUGE = Gauge(
    'python_app_queue_size',
    'Current number of items waiting in the background processing queue'
)

# --- 2. Application Routes ---

@app.route('/')
def home():
    endpoint = '/'
    method = 'GET'
    
    REQUEST_COUNT.labels(endpoint=endpoint, method=method).inc()
    
    print(f"User requested {endpoint}. Counter updated.")
    
    return """
    <div style="font-family: Inter, sans-serif; text-align: center; margin-top: 50px;">
        <h1 style="color: #4CAF50;">Welcome to the Instrumented Web App!</h1>
        <p>This is a basic Flask application.</p>
        <p>Every time you refresh this page, the 
           <code style="background-color: #eee; padding: 2px 4px; border-radius: 3px;">python_app_requests_total</code> 
           metric is incremented.</p>
        <p>View the metrics at: <a href="/metrics" style="color: #1E88E5;">/metrics</a></p>
    </div>
    """

@app.route('/metrics')
def metrics():
    """
    Prometheus endpoint: Returns the latest metrics in Prometheus format.
    """

    data = generate_latest()
    

    return Response(data, mimetype=CONTENT_TYPE_LATEST)


def background_queue_simulator():

    while True:
        if random.random() < 0.6:
            QUEUE_SIZE_GAUGE.inc(random.uniform(0.1, 1.5))
        else:
            current_val = QUEUE_SIZE_GAUGE.collect()[0].samples[0].value
            if current_val > 0.5:
                 QUEUE_SIZE_GAUGE.dec(random.uniform(0.1, 0.5))
        
        # Output current state to the console
        current_queue = QUEUE_SIZE_GAUGE.collect()[0].samples[0].value
        print(f"[{time.strftime('%H:%M:%S')}] Background Queue Size updated to: {current_queue:.2f}")
        sys.stdout.flush() 

        time.sleep(random.uniform(2.0, 5.0))


if __name__ == '__main__':

    
    PORT = 8000
    
    thread = threading.Thread(target=background_queue_simulator, daemon=True)
    thread.start()
    
    print(f"--- Application started. ---")
    print(f"Access Web App at: http://localhost:{PORT}/")
    print(f"Prometheus endpoint at: http://localhost:{PORT}/metrics")
    

    app.run(host='0.0.0.0', port=PORT, debug=False)
