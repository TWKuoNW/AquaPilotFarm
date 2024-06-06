import cv2
from flask import Flask, Response
import threading

app = Flask(__name__)

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
        self.lock = threading.Lock()

    def get_frame(self):
        with self.lock:
            success, frame = self.cap.read()
            if not success:
                return None
            else:
                frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                return frame

camera = Camera()

def generate_frames(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
