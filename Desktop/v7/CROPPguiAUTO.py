from tkinter import *
from tkinter import messagebox
import serial
#from photo_booth import activateCameras
# from Camera_Adapter.AdapterBoard import MultiAdapter
# from Camera_Adapter.cameraapp import CameraApp
# from imutils.video import VideoStream
import time
from PIL import Image
from PIL import ImageTk
import threading
import logging
import justCameras

USB_PORT = "/dev/ttyACM0"
global usb

USB_PORT2 = "/dev/ttyACM1"
global usb2





global window
global info
global data 
global stepperFrame
global ledFrame
global tempHumidFrame
global tempFrame
global humidFrame
global linearFrame
global pumpFrame
global cameraFrame

global closeEvent


def createWindow():
    global window
    global info
    global data 
    global stepperFrame
    global ledFrame
    global tempHumidFrame
    global tempFrame
    global humidFrame
    global linearFrame
    global pumpFrame
    global cameraFrame
    
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
    tempHumidFrame.grid(row=0,column=2,padx=1,sticky='w')

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
    
    window.protocol("WM_DELETE_WINDOW",on_close)


def on_close():
    global closeEvent
    closeEvent.set()
#     th.output.close()
    print("Closing....")
    window.destroy()
    


def connect():
    global usb
    global usb2
    usbFail = True
    usb2Fail = True
    
    global closeEvent
    closeEvent = threading.Event()
    
    #try:
        #usb = serial.Serial(USB_PORT,9600,timeout=2) # Steppers and LED strips
    #except:
        #usbFail = True

    #try:
        #usb2 = serial.Serial(USB_PORT2,9600,timeout=2) # Pumps, Linear Actuators, and Temp/Humidity sensor
    #except:
        #usb2Fail = True

    while usbFail:
        try:
            usb = serial.Serial(USB_PORT,9600,timeout=2) # Steppers and LED strips
            usbFail = False
        except:
            usb2Fail = True
        messagebox.showwarning("ARDUINO NOT CONNECTED","Arduino 1 (Steppers and LED's) not connected.\nReconnect and press ok")
        
        
            
    while usb2Fail:
        try:
            usb2 = serial.Serial(USB_PORT2,9600,timeout=2) # Steppers and LED strips
            usb2Fail = False
        except:
            usb2Fail = True
        messagebox.showerror("ARDUINO NOT CONNECTED","Arduino 2 (Pumps, Actuators, and Temp/Humidity Sensor) not connected.\nReconnect and press ok")
        
          



def writeToArduino(command):
    global usb
    try:
        usb.write(command)
    except NameError:
        logging.warn("usb not connected")
    logging.info(command.decode())

def writeToArduino2(command):
    global usb2
    try:
        usb2.write(command)
    except NameError:
        logging.warn("usb not connected")
    logging.info(command.decode())



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
    on1 = Button(stepperFrame, text="Run Grow Belt",command=sendStepper1,width=10,height=5,bg="green")
    off1 = Button(stepperFrame, text="Kill Grow Belt",command=killStepper1,width=10,height=5,bg="red")
    on1.grid(row=0,column=0,padx=1,pady=5)
    off1.grid(row=0,column=1,padx=1,pady=5)


    #on2 = Button(stepperFrame, text="Run Stepper 2",command=sendStepper2,width=10,height=5,bg="green")
    #off2 = Button(stepperFrame, text="Kill Stepper 2",command=killStepper2,width=10,height=5,bg="red")
    #on2.grid(row=1,column=0,padx=1,pady=5)
    #off2.grid(row=1,column=1,padx=1,pady=5)


    #allOff = Button(stepperFrame,text="Kill All Steppers",command=killAllSteppers,height=5,bg="darkred")
    #allOff.grid(row=3,column=0,columnspan=2,padx=0,pady=5,sticky="nesw")

def killAllPumps(pumps,pumpValues):
    writeToArduino2(b'killPumps')
    for ind,pump in enumerate(pumps):
        if pumpValues[ind].get() == 1:
            logging.info("Toggle {}".format(ind+1))
            pump.deselect()
            
def startAllPumps(pumps,pumpValues):
    writeToArduino2(b'allPumps')
    for ind,pump in enumerate(pumps):
        if pumpValues[ind].get() == 0:
            pump.select()
        

def makePumpButtons():
    pumps = []
    pumpValues = [IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar()]
    
    pumps.append(Checkbutton(pumpFrame,text="Pump 0",command = lambda: togglePump(0),width = 10,variable=pumpValues[0]))
    pumps.append(Checkbutton(pumpFrame,text="Pump 1",command = lambda: togglePump(1),width = 10,variable=pumpValues[1]))
    pumps.append(Checkbutton(pumpFrame,text="Pump 2",command = lambda: togglePump(2),width = 10,variable=pumpValues[2]))
    pumps.append(Checkbutton(pumpFrame,text="Pump 3",command = lambda: togglePump(3),width = 10,variable=pumpValues[3]))
    pumps.append(Checkbutton(pumpFrame,text="Pump 4",command = lambda: togglePump(4),width = 10,variable=pumpValues[4]))
    pumps.append(Checkbutton(pumpFrame,text="Pump 5",command = lambda: togglePump(5),width = 10,variable=pumpValues[5]))
    pumps.append(Checkbutton(pumpFrame,text="Pump 6",command = lambda: togglePump(6),width = 10,variable=pumpValues[6]))
    pumps.append(Checkbutton(pumpFrame,text="Pump 7",command = lambda: togglePump(7),width = 10,variable=pumpValues[7]))
    pumps.append(Checkbutton(pumpFrame,text="Pump 8",command = lambda: togglePump(8),width = 10,variable=pumpValues[8]))
    pumps.append(Checkbutton(pumpFrame,text="Pump 9",command = lambda: togglePump(9),width = 10,variable=pumpValues[9]))
    pumps.append(Checkbutton(pumpFrame,text="Pump 10",command = lambda: togglePump(10),width = 10,variable=pumpValues[10]))
    pumps.append(Checkbutton(pumpFrame,text="Pump 11",command = lambda: togglePump(11),width = 10,variable=pumpValues[11]))


    for ind,pump in enumerate(pumps):
        pump.grid(row=int(ind/2),column=ind%2,padx=1,pady=1)
    killPumps = Button(pumpFrame,text = "Kill All Pumps",command = lambda: killAllPumps(pumps,pumpValues))
    killPumps.grid(row=6,column=0)
    startPumps = Button(pumpFrame,text="Start All Pumps",command = lambda: startAllPumps(pumps,pumpValues))
    startPumps.grid(row=6,column=1)
    
    
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
        
       
        self.thread = threading.Thread(target = self.refreshValues,args=())
        

        self.frame.after(5000,self.thread.start)
        self.frame.after(5000,self.updateDisplay)
        #stopEvent = None
        #temphumThread = threading.Thread(target=makeTempHumid,args=())
        #temphumThread.start()

    def refreshValues(self):
        global closeEvent
        while not closeEvent.is_set():

            writeToArduino2(self.code)

            data = usb2.read_until('\n')
            data=data.decode()
            logging.info(data)
            try:
                self.humid,self.temp = data.split('!')
                self.humid = self.humid.strip()
                self.temp = self.temp.strip()
            except:
                logging.debug("Invalid temperature values recieved")
            
            time.sleep(10)    
            #self.frame.after(10000,self.refreshValues)
    def updateDisplay(self):
        self.h.configure(text="Humidity: {}%".format(self.humid))
        self.t.configure(text="Temperature: {} C".format(self.temp))
        self.output.write("{}% | {}C\n".format(self.humid,self.temp))
        
        self.frame.after(5000,self.updateDisplay)


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




def debugMode():
    logging.basicConfig(level=logging.DEBUG)


class Autonomouos:
    def __init__(self):
        self.lightHoursOn = 60
        self.lightHoursOff= 21600
        
        #Interval between photos, in minutes
        self.photoInterval = 5
        
#         self.toggleWhite = toggleWhite
        
        self.lightThread = threading.Thread(target = self.toggleLights,args=())
        autoLabel = Label(text="Autonomous Lighting Mode is running at an interval of {} hours.".format(self.lightHoursOn))
        autoLabel.grid(row=0,column=0)
        
#         while True:
#             self.toggleLights()
    
    def flashToggle(self):
        toggleWhite()
    
    def toggleLights(self):
         toggleWhite()
         while True and not closeEvent.is_set():
            time.sleep(self.lightHoursOff)
            toggleWhite()
            time.sleep(self.lightHoursOn)
            toggleWhite()
            



def runAuto():
    createWindow()
    makeInfo()
    auto = Autonomouos()
    auto.lightThread.start()
    window.update()

    


    while True and not closeEvent.is_set():
        window.update()

if __name__ == '__main__':
    
    createWindow()
    makeInfo()
    
    auto = Autonomouos()
    auto.lightThread.start()
    window.update()

#     auto.toggleLights()
#     connect()
#     makeStepperButtons()
#     makeLEDButtons()
#     makeTempHumid()
#     makePumpButtons()
#     makeActuatorButtons()
#     # startCameras()
    
    
    debug= Button(text="debug mode",command=debugMode)
    debug.grid(row=6,column=0,sticky='sw')
    

    #activateCameras(window)

    while True and not closeEvent.is_set():
        window.update()
