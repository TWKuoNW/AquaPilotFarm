import cv2
import threading

class Camera:
    def __init__(self, camera_idx):
        self.cap = cv2.VideoCapture(camera_idx, cv2.CAP_V4L2)
        self.lock = threading.Lock()

    def get_frame(self):
        with self.lock:
            success, frame = self.cap.read()
            if not success:
                return None
            else:
                frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_LINEAR)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                return frame
