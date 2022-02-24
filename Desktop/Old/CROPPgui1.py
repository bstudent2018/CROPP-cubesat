import tkinter as tk
import serial


USB_PORT = "/dev/ttyACM0"

try:
    usb = serial.Serial(USB_PORT,9600,timeout=2)
except:
    print("ERROR could not open USB port, check port name and permissions.")
    print("Exiting....")
    exit()

window = tk.Tk()
#window.rowconfigure([0,1],minsize=50)
#window.columnconfigure([0,1],minsize=50)

def sendStepper1():
    usb.write(b'stepper1On')
    print("Stepper 1 On")
    
def killStepper1():
    usb.write(b'stepper1Off')
    print("Stepper 1 Off")
    

def sendStepper2():
    usb.write(b'stepper2On')
    print("Stepper 2 On")
    
def killStepper2():
    usb.write(b'stepper2Off')
    print("Stepper 2 Off")
    

on1 = tk.Button(window, text="Run Stepper 1",command=sendStepper1,width=10,height=10)

off1 = tk.Button(window, text="Kill Stepper 1",command=killStepper1,width=10,height=10)
#on1.grid(row=0,column=0)
#off1.grid(row=1,column=0)


on1.pack()
off1.pack()


on2 = tk.Button(window, text="Run Stepper 2",command=sendStepper2,width=10,height=10)

off2 = tk.Button(window, text="Kill Stepper 2",command=killStepper2,width=10,height=10)
#on2.grid(row=0,column=1)
#off2.grid(row=1,column=1)

on2.pack()
off2.pack()



window.mainloop()