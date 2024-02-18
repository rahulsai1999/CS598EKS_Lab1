import fcntl
import socket
import struct
from sense_hat import SenseHat

# Initialize SenseHat
sense = SenseHat()
sense.clear()

def get_ip_address(ifname):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])
    except OSError:
        return "Not Found"

# Fetch IP address
ip_address = get_ip_address('wlan0')

# Define text and background colours
red = (255, 0, 0)
blue = (0, 0, 0)

# Show message
# print(ip_address)
sense.show_message("IP: " + ip_address, text_colour=red, back_colour=blue, scroll_speed=0.05)
sense.clear()
