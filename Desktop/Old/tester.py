import serial
from time import sleep

USB_PORT = "/dev/ttyACM0"
global usb

def connect():
    global usb
    try:
        usb = serial.Serial(USB_PORT,9600,2) # Steppers and LED strips
    except:
        print("ERROR could not open USB port, check port name and permissions.")
        print("Exiting....")
        exit(-1)
        
        
connect()

while True:
    usb.write(b'stepper1On')
    sleep(3)
    usb.write(b'stepper1Off')
    sleep(3)