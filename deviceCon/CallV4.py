import threading
import time
from VideoStreamV4 import app

def run_flask_app():
    app.run(host='0.0.0.0', port=8080, threaded=True)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    for i in range(10):
        print(i)
        time.sleep(1)
