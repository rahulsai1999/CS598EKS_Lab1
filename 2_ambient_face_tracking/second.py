import sys
import cv2
import time
from sense_hat import SenseHat
from picamera2 import Picamera2

sense = SenseHat()
picam2 = Picamera2()

dispW, dispH = 1280, 720
picam2.preview_configuration.main.size = (dispW, dispH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.preview_configuration.controls.FrameRate = 30
picam2.configure("preview")
picam2.start()

# Load the face cascade for face detection
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Get initial temperature and humidity
initial_temp = sense.get_temperature()

try:
    while True:
        # Get current temperature and humidity
        current_temp = sense.get_temperature()
        print("Current Temperature: ", current_temp)
        
        # Check for significant changes in temperature or humidity
        if abs(current_temp - initial_temp) > 1:
            print("Significant change detected, starting face detection.")
            
            while True:
                frame = picam2.capture_array()
                frame = cv2.flip(frame, 0)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = faceCascade.detectMultiScale(gray, 1.1, 4)
                
                # Print the number of faces detected
                print(f"Number of faces detected: {len(faces)}")
                
                # Draw rectangle around each face
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                # Display the resulting frame
                cv2.imshow('Frame', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            initial_temp = current_temp
            
        # Wait a bit before the next read
        time.sleep(2)
        
except KeyboardInterrupt:
    cv2.destroyAllWindows()
    picam2.stop()
    sys.exit(0)

