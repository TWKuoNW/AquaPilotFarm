import cv2
import os

def list_connected_cameras():
    index = 0
    arr = []
    while(index < 20):
        cap = cv2.VideoCapture(index + cv2.CAP_V4L2)
        if(cap.isOpened()):
            ret, _ = cap.read()
            if ret:
                arr.append(index)
        cap.release()
        index += 1
    return arr

cameras = list_connected_cameras()
print("Connected cameras:", cameras)

if cameras:
    caps = []
    outs = []

    if(not os.path.exists('output')):
        os.makedirs('output')

    for i in range(len(cameras)):
        cap = cv2.VideoCapture(cameras[i])
        if(not cap.isOpened()):
            print(f"Error: Could not open camera {cameras[i]}.")
            exit()

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_filename = f'output/v{i+1}.avi'
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_filename, fourcc, 20.0, (frame_width, frame_height))

        caps.append(cap)
        outs.append(out)

    while(True):
        for i in range(len(cameras)):
            ret, frame = caps[i].read()
            if(not ret):
                print(f"Error: Failed to capture image from camera {cameras[i]}")
                break

            cv2.imshow(f'Video Capture {i+1}', frame)
            outs[i].write(frame)

        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

    for cap, out in zip(caps, outs):
        cap.release()
        out.release()

    cv2.destroyAllWindows()
else:
    print("No cameras found.")
