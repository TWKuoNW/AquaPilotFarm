import socket
import cv2

cap = cv2.VideoCapture(0)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 6789))

print("UDP server up and listening")

data, address = server_socket.recvfrom(65500)
print(address)

while True:
   """
   data, address = server_socket.recvfrom(1024)
   print(f"Message from {address}: {data.decode()}")
   """
   
   ret, frame = cap.read()
   resized_image = cv2.resize(frame, (480, 320), interpolation=cv2.INTER_LINEAR)
   
   _, data = cv2.imencode('.jpg', resized_image)
   
   server_socket.sendto(data, address)
