import VideoStreamV3 as VStream
import time
import threading


def run():
	VStream.app.run(host='0.0.0.0', port=5000) 


s = threading.Thread(target = run, daemon = True)
s.start()


for i in range(100):
	print(i)
	time.sleep(1)
