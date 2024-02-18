import cv2
from picamera2 import Picamera2
import numpy as np

# Initialize the camera
picam2 = Picamera2()
dispW, dispH = 1280, 720
picam2.preview_configuration.main.size = (dispW, dispH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.preview_configuration.controls.FrameRate = 30
picam2.configure("preview")
picam2.start()

eyesCascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

while True:
    frame = picam2.capture_array()
    frame = cv2.flip(frame, 0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    eyes = eyesCascade.detectMultiScale(gray, 1.1, 4)
    
    if eyes > 0:
        print(f"Attention detected!")
    
        # Draw rectangle around the eyes
        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cv2.destroyAllWindows()
