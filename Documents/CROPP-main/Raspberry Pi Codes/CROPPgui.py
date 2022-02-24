from tkinter import *
import serial
# from Camera_Adapter.AdapterBoard import MultiAdapter
# from Camera_Adapter.cameraapp import CameraApp
# from imutils.video import VideoStream
import time
from PIL import Image
from PIL import ImageTk


USB_PORT = "/dev/ttyACM0"
global usb

USB_PORT2 = "/dev/ttyACM1"
global usb2



def connect():
    global usb
    global usb2
    try:
        usb = serial.Serial(USB_PORT,9600,timeout=2) # Steppers and LED strips
    except:
        print("ERROR could not open USB port 1, check port name and permissions.")
        print("Exiting....")
        exit(-1)

    try:
        usb2 = serial.Serial(USB_PORT2,9600,timeout=2) # Pumps, Linear Actuators, and Temp/Humidity sensor
    except:
        print("ERROR could not open USB port 2, check port name and permissions.")
        print("Exiting....")
        exit(-1)

#connect()

window = Tk()
window.geometry("1200x500")


info = Frame(window)
info.grid(row=0,column=0)


data = Frame(window)
data.grid(row=0,column=1)

stepperFrame = Frame(data)
stepperFrame.grid(row=0,column=0,padx=10,sticky='n')

ledFrame= Frame(data)
ledFrame.grid(row=0,column=1,padx=10,sticky='n')

tempHumidFrame = Frame(data)
tempHumidFrame.grid(row=0,column=2,padx=4,sticky='n')

tempFrame = Frame(tempHumidFrame)
tempFrame.grid(row=0,column=0)

humidFrame = Frame(tempHumidFrame)
humidFrame.grid(row=1,column=0)


linearFrame = Frame(data)
linearFrame.grid(row=1,column=1)

pumpFrame = Frame(data)
pumpFrame.grid(row=1,column=0)

cameraFrame = Frame(data)
cameraFrame.grid(row=0,column=2)




def on_close():
    th.output.close()
    window.destroy()
window.protocol("WM_DELETE_WINDOW",on_close)






def writeToArduino(command):
    global usb
    try:
        usb.write(command)
    except NameError:
        print("usb not connected")
    print(command.decode())

def writeToArduino2(command):
    global usb2
    try:
        usb2.write(command)
    except NameError:
        print("usb not connected")
    print(command.decode())



def sendStepper1():
    writeToArduino(b'stepper1On\n')


def killStepper1():
    writeToArduino(b'stepper1Off\n')


def sendStepper2():
    writeToArduino(b'stepper2On\n')


def killStepper2():
    writeToArduino(b'stepper2Off\n')


def killAllSteppers():
    writeToArduino(b'allStepperOff\n')

def toggleWhite():
    writeToArduino(b'toggleWhite\n')

def toggleUVC():
    writeToArduino(b'toggleUVC\n')

def makeLEDButtons():
    whiteToggle = Button(ledFrame,text="Toggle White LED's",command=toggleWhite,width=20,height=5,bg="white")
    whiteToggle.grid(row=0,column=0,padx=1,pady=5)
    uvcToggle = Button(ledFrame,text="Toggle UVC LED's",command=toggleUVC,width=20,height=5,bg="lightblue")
    uvcToggle.grid(row=1,column=0,padx=1,pady=5)


def makeStepperButtons():
    on1 = Button(stepperFrame, text="Run Stepper 1",command=sendStepper1,width=10,height=5,bg="green")
    off1 = Button(stepperFrame, text="Kill Stepper 1",command=killStepper1,width=10,height=5,bg="red")
    on1.grid(row=0,column=0,padx=1,pady=5)
    off1.grid(row=0,column=1,padx=1,pady=5)


    on2 = Button(stepperFrame, text="Run Stepper 2",command=sendStepper2,width=10,height=5,bg="green")
    off2 = Button(stepperFrame, text="Kill Stepper 2",command=killStepper2,width=10,height=5,bg="red")
    on2.grid(row=1,column=0,padx=1,pady=5)
    off2.grid(row=1,column=1,padx=1,pady=5)


    allOff = Button(stepperFrame,text="Kill All Steppers",command=killAllSteppers,height=5,bg="darkred")
    allOff.grid(row=3,column=0,columnspan=2,padx=0,pady=5,sticky="nesw")



def makePumpButtons():
    pumps = []

    pumps.append(Checkbutton(pumpFrame,text="Pump 1",command = lambda: togglePump(1),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 2",command = lambda: togglePump(2),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 3",command = lambda: togglePump(3),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 4",command = lambda: togglePump(4),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 5",command = lambda: togglePump(5),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 6",command = lambda: togglePump(6),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 7",command = lambda: togglePump(7),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 8",command = lambda: togglePump(8),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 9",command = lambda: togglePump(9),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 10",command = lambda: togglePump(10),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 11",command = lambda: togglePump(11),width = 10))
    pumps.append(Checkbutton(pumpFrame,text="Pump 12",command = lambda: togglePump(12),width = 10))


    for ind,pump in enumerate(pumps):
        pump.grid(row=int(ind/2),column=ind%2,padx=1,pady=1)


def togglePump(ind):
    writeToArduino2(bytes('$pump{:02d}'.format(ind),'utf-8'))

def toggleAct1():
    writeToArduino2(b'act1')
def toggleAct2():
    writeToArduino2(b'act2')

def makeActuatorButtons():
    act1Toggle = Button(linearFrame,text="Toggle Linear Actuator 1",command=toggleAct1,width =20,height = 5)
    act2Toggle = Button(linearFrame,text="Toggle Linear Actuator 2",command=toggleAct2,width=20,height=5)
    act1Toggle.grid(row=0,column=0,padx=1,pady=1)
    act2Toggle.grid(row=1,column=0,padx=1,pady=1)



class tempHumid:
    def __init__(self,t,h):
        self.humid = 0
        self.h = h

        self.temp = 0
        self.t = t
        self.code = b'getTH\n'
        self.frame = Frame(window)

        self.output = open("output.txt","a")


        self.frame.after(5000,self.refreshValues)


    def refreshValues(self):



        writeToArduino2(self.code)

        data = usb2.read_until('\n')
        data=data.decode()
        print(data)
        self.humid,self.temp = data.split('!')
        self.humid = self.humid.strip()
        self.temp = self.temp.strip()

        self.h.configure(text="Humidity: {}%".format(self.humid))
        self.t.configure(text="Temperature: {} C".format(self.temp))
        self.output.write("{}% | {}C\n".format(self.humid,self.temp))

        self.frame.after(10000,self.refreshValues)



def makeTempHumid():

#tempOut = liveReadout(tempFrame,"Temperature")
    tempOut = Label(tempFrame,text="Temperature: ",font=(20),justify=LEFT)
    tempOut.pack()
#humidOut = liveReadout(humidFrame,"Humidity" )
    humidOut = Label(humidFrame,text="Humidity: ",font=(20),justify=LEFT)
    humidOut.pack()
    global th
    th = tempHumid(tempOut,humidOut)


def makeInfo():
    image = Image.open("panther_head.png")
    image = image.resize((200, int(200/1.24710221)), Image.ANTIALIAS)
    panther = ImageTk.PhotoImage(image)

    title = Label(info,text = "CROPP \n(CubeSat Research of Plants Platform) \nGround Station Test GUI",font=(30))
    photo = Label(info,image = panther)
    photo.image = panther
    title.grid(row=0,column=0)
    photo.grid(row=1,column=0)


def startCameras():
    camAdapter = MultiAdapter()
    Arducam_adapter_board.init(320,240)
    cameras = CameraApp("/",cameraFrame,camAdapter)








if __name__ == '__main__':
    #connect()
    makeStepperButtons()
    makeLEDButtons()
    makeTempHumid()
    makePumpButtons()
    makeActuatorButtons()
    # startCameras()
    makeInfo()

    while True:
        window.update()
