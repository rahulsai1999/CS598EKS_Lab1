import sys
import signal
from sense_hat import SenseHat

sense = SenseHat()
sense.clear() 

# Initial coordinates of the pixel
x, y = 3, 5
# Set the initial pixel to red
sense.set_pixel(x, y, (255, 0, 0))

def signal_handler(sig, frame):
    sense.clear()
    sys.exit(0)

# Bind the signal handler to SIGINT
signal.signal(signal.SIGINT, signal_handler)

while True:
    for event in sense.stick.get_events():
        if event.action == 'pressed':
            # Clear the current pixel
            sense.set_pixel(x, y, (0, 0, 0))

            # Update coordinates based on the direction of the joystick
            if event.direction == 'up' and y > 0:
                y -= 1
            elif event.direction == 'down' and y < 7:
                y += 1
            elif event.direction == 'right' and x < 7:
                x += 1
            elif event.direction == 'left' and x > 0:
                x -= 1

            # Update the pixel to red at the new coordinates
            sense.set_pixel(x, y, (255, 0, 0))

            # Exit on middle button press
            if event.direction == 'middle':
                sense.clear()
                sys.exit(0)
