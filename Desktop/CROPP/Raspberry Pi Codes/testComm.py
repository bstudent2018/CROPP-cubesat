import serial


USB_PORT = "/dev/ttyACM0"
global usb

try:
    usb = serial.Serial(USB_PORT,9600,timeout=2) # Steppers and LED strips
except:
    print("ERROR could not open USB port 1, check port name and permissions.")
    print("Exiting....")
    exit(-1)
