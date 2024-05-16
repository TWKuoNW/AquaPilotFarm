import time
import cv2

cap = cv2.VideoCapture(2 + cv2.CAP_V4L2)

while(cap.isOpened()):
   ret, frame = cap.read()
   frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
   cv2.imshow("frame", frame)
   
   if(cv2.waitKey(1) == 27):
      break
cap.release()
cv2.destroyAllWindows()
