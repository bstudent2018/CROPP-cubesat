import RPi.GPIO as gp
import os
import cv2 as cv
import numpy as np
import time
from datetime import datetime
import threading



class WebcamVideoStream:
    """
    Class to control the video stream of the cameras
        Adapted from imutils WebcamVideoStream

    Attributes
    ----------
    adapter : MultiAdapter
        Instance of MultiAdapter class that controls camera switching
    stream
        Video stream of camera
    stopped : threading Event
        Indicates if the threads need to be stopped


    Methods
    -------
    start()
        Starts the thread to read frames from video stream
    update()
        Loops indefinetly in thread to grab next frame in stream
    read()
        Returns most recently read frames
    stop()
        Signals the thread to stop
    """

    def __init__(self):
        """
        Initializes the video camera stream and reads the first frame
        from the stream

        """
        self.adapter= MultiAdapter()
        self.adapter.init(320,240)
        self.adapter.select_channel('A')
        self.stream = self.adapter.camera
        (self.grabbed, self.frame) = self.stream.read()

        self.name = "VideoStream"
        self.stopped = False

    def start(self):
        """
        Starts thread to read frames from VideoStream
        """
        t = threading.Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        """
        Keeps looping until thread stop indicator is set
        Grabs next frame from VideoStream
        """
        while True:
            if self.stopped:
                return

            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        """
        Returns the frame most recently read
        """
        return self.frame

    def stop(self):
        """
        Indicates that the thread should be stopped
        """
        self.stopped = True





class MultiAdapter:
    """
    Class to control camera switching the multicamera adapter
    

    Attributes
    ----------
    numCameras : 
        Number of Cameras
    adapter_info : Dictionary
        Dictionary containing relevant i2c commands and GPIO setups for camera switching
    camera : 
        OpenCv VideoCapture object
    width : 
        Width, in pixels, of camera output
    height : 
        Height, in pixels, of camera output
    
    Methods
    -------
    choose_channel(index)
        index : Int
            Index (0-3) of camera to switch to 
        Switches camera output to given camera (0:A,1:B,2:C,3:D)
        Uses both I2C and GPIO
        Only used in initialization
    select_channel(index)
        index : Int
            Index (0-3) of camera to switch to
        Switches camera output to given camera (0:A,1:B,2:C,3:D)
        Uses ONLY GPIO
    init(width,height)
        width : Int
            Width, in pixels, of camera output    
        height : 
            Height, in pixels, of camera output
        Used to actually start cameras and make sure they are properly outputting    
    getSnapshot(i,frame)
        i : Int
            Index of camera to take photo from 
        frame : 
            Captured image frame
        Saves frame as JPG image
    preview()
        Shows live camera views side by side
        Pressing 'C' saves photos from all cameras
        Pressing 'Q' closes window
    
        
            
    """
    numCameras = 4
    adapter_info = {   "A":{   "i2c_cmd":"i2cset -y 1 0x70 0x00 0x04",
                                    "gpio_sta":[0,0,1],
                            },
                        "B":{
                                "i2c_cmd":"i2cset -y 1 0x70 0x00 0x05",
                                "gpio_sta":[1,0,1],
                            },
                        "C":{
                                "i2c_cmd":"i2cset -y 1 0x70 0x00 0x06",
                                "gpio_sta":[0,1,0],
                            },
                        "D":{
                                "i2c_cmd":"i2cset -y 1 0x70 0x00 0x07",
                                "gpio_sta":[1,1,0],
                            },
                     }
    camera = cv.VideoCapture(0)
    width = 320
    height = 240

    def __init__(self):

       os.system("i2cset -y 1 0x70 0x00 0x04")
       time.sleep(1)
       gp.setwarnings(False)
       gp.setmode(gp.BOARD)
       gp.setup(7, gp.OUT)
       gp.setup(11,gp.OUT)
       gp.setup(12,gp.OUT)

    def choose_channel(self,index):
        channel_info = self.adapter_info.get(index)
        if channel_info == None:
            print("Can't get this info")
        flag = os.system(channel_info["i2c_cmd"]) # i2c write
        while flag:
            flag = os.system(channel_info["i2c_cmd"]) # i2c write

        gpio_sta = channel_info["gpio_sta"] # gpio write
        gp.output(7, gpio_sta[0])
        gp.output(11, gpio_sta[1])
        gp.output(12, gpio_sta[2])
    def select_channel(self,index):
        channel_info = self.adapter_info.get(index)
        if channel_info == None:
            print("Can't get this info")
        gpio_sta = channel_info["gpio_sta"] # gpio write
        gp.output(7, gpio_sta[0])
        gp.output(11, gpio_sta[1])
        gp.output(12, gpio_sta[2])

    def init(self,width,height):
        for i in range(self.numCameras):
           self.height = height
           self.width = width
           self.choose_channel(chr(65+i))
           self.camera.set(3, self.width)
           self.camera.set(4, self.height)
           ret, frame = self.camera.read()
           if ret == True:
               print("camera %s init OK" %(chr(65+i)))
               pname = "image_"+ chr(65+i)+"_INIT.jpg"
               cv.imwrite(pname,frame)
               time.sleep(1.2)


    def getSnapshot(self,i,frame):
        now = datetime.now()
        pname = "image_"+ chr(65+i)+"_"+now.strftime("%H%M%S")+".jpg"
        cv.imwrite(pname,frame)


    def preview(self):
        font                   = cv.FONT_HERSHEY_PLAIN
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 1
        factor  = 20
        black = np.zeros(((self.height+factor)*2, self.width*2, 3), dtype= np.uint8)
        i = 0
        amount=0
        while True:

            self.select_channel(chr(65+i))
            ret, frame = self.camera.read()
            ret, frame = self.camera.read()
            ret, frame = self.camera.read()
            frame.dtype=np.uint8
            if i == 0:
                black[factor:factor+self.height, 0:self.width, :] = frame
                bottomLeftCornerOfText = (factor,factor)
                index = chr(65+i)
            elif i == 1:
                black[factor:factor+self.height, self.width:self.width*2,:] = frame
                bottomLeftCornerOfText = (factor+self.width, factor)
                index = chr(65+i)
            elif i == 2:
                black[factor*2+self.height:factor*2+self.height*2, 0:self.width,:] = frame
                bottomLeftCornerOfText = (factor, factor*2+self.height)
                index = chr(65+i)
            elif i == 3:
                black[factor*2+self.height:factor*2+self.height*2, self.width:self.width*2,:] = frame
                bottomLeftCornerOfText = (factor+self.width, factor*2+self.height)
                index = chr(65+i)
            i = i+1
            if i==self.numCameras:
                i = 0
            cv.putText(black,'CAM '+index, bottomLeftCornerOfText, font, fontScale,fontColor,lineType)
            cv.imshow("Arducam Multi Camera Demo",black)
            if cv.waitKey(1) & 0xFF == ord('q'):
                del frame
                self.camera.release()
                cv.destroyAllWindows()
                break
            if cv.waitKey(1) & 0xFF == ord('c'):
                if amount <= 0:
                    amount =4

            if amount > 0:
                self.getSnapshot(i,frame)
                amount -=1
