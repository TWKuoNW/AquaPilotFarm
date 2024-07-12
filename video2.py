from flask import Flask, Response
from camera import Camera

class VideoStream():
    def __init__(self, camera_idx):
        self.app = Flask(__name__)
        self.camera = Camera(camera_idx)
        self.add_routes()

    def add_routes(self):
        self.app.add_url_rule('/video', 'video', self.video)

    def generate_frames(self, camera):
        while True:
            frame = camera.get_frame()
            if frame is None:
                break
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def video(self):
        return Response(self.generate_frames(self.camera), mimetype='multipart/x-mixed-replace; boundary=frame')

    def run(self, host='0.0.0.0', port=8002, threaded=True):
        self.app.run(host=host, port=port, threaded=threaded)

if __name__ == '__main__':
    video_stream = VideoStream(1)
    video_stream.run()
