import cv2
from flask import Flask, Response

app = Flask(__name__)

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read() 
        if not success:
            break
        else:
            frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            #cv2.imshow("frame", frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                   
@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
