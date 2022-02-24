
import RPi.GPIO as gp
import os
import cv2 as cv 
import numpy as np
import time

class CamAdapter:
    camNum = 4
    width = 320
    height = 240
    adapter_info = {   "A":{   "i2c_cmd":"i2cset -y 0 0x70 0x00 0x04",
                                    "gpio_sta":[0,0,1],
                            },
                        "B":{
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x05",
                                "gpio_sta":[1,0,1],
                            },
                        "C":{
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x06",
                                "gpio_sta":[0,1,0],
                            },
                        "D":{
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x07",
                                "gpio_sta":[1,1,0],
                            },
                        "NoCamera":{
                                "gpio_sta":[0,1,1]
                            }
                     } 
                     
    camera = cv.VideoCapture(0)
    if not camera.isOpened():
        print("Cannot Open Camera")
        exit()
    

    def __init__(self):
        gp.setwarnings(False)
        gp.setmode(gp.BOARD)
        gp.setup(7,gp.OUT)
        gp.setup(11,gp.OUT)
        gp.setup(12,gp.OUT)
        
        gp.output(7,False)
        gp.output(11,True)
        gp.output(12,True)
        self.camera.set(3, self.width)
        self.camera.set(4, self.height)
        for i in range(self.camNum):
            self.choose_channel(chr(65+i))
            print("Got camera {}".format(chr(65+i)))
            
#             ret, frame = self.camera.read()
            ret, frame = self.camera.read()
            if ret == True:
               print("camera %s init OK" %(chr(65+i)))
               pname = "image_"+ chr(65+i)+".jpg"
               cv.imwrite(pname,frame)
               time.sleep(2)

    def choose_channel(self,index):
        channel_info = self.adapter_info.get(index)
        if channel_info == None:
            print("Can't get this info")
        os.system(channel_info["i2c_cmd"]) # i2c write
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
        
    def getFrame(self,index):
        self.select_channel(chr(65+index))
        ret,frame = self.camera.read()
        if not ret:
            print("Cannot Recieve Frame")
        return ret, frame
     