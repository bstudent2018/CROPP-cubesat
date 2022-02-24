import RPi.GPIO as gp
import os
import cv2 as cv
import numpy as np
import time
# from imutils.video import VideoStream
# import imutils

class MultiAdapter:
    camNum = 4
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
    #camera = cv.VideoCapture(0)
    os.system("i2cset -y 1 0x70 0x00 0x04")
    camera = cv.VideoCapture(0) 

#     camera = VideoStream(usePiCamera=True).start()
    time.sleep(2)
    width = 320
    height = 240

    def __init__(self):
        gp.setwarnings(False)
        gp.setmode(gp.BOARD)
        gp.setup(7, gp.OUT)
        gp.setup(11, gp.OUT)
        gp.setup(12, gp.OUT)
        gp.setup(15, gp.OUT)
        gp.setup(16, gp.OUT)
        gp.setup(21, gp.OUT)
        gp.setup(22, gp.OUT)
        gp.output(11, True)
        gp.output(12, True)
        gp.output(15, True)
        gp.output(16, True)
        gp.output(21, True)
        gp.output(22, True)
        
        
        

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

    def init(self,width,height):
        for i in range(self.camNum):
           self.height = height
           self.width = width
           
           self.choose_channel(chr(65+i))
           frame = self.camera.read()
           if frame is not None:
               print("camera %s init OK" %(chr(65+i)))
               pname = "image_"+ chr(65+i)+".jpg"
               cv.imwrite(pname,frame)
               time.sleep(1)
           else:
               print("Init Failed....")
    
    def getFrame(self,cam_num):
        self.select_channel(chr(65+cam_num))
        return self.camera.read()
    
    def capture(self,cam_num):
        self.select_channel(chr(65+cam_num))
        


    def previewSingleNew(self,cam_num):
        self.select_channel(chr(65+cam_num-1))
        while True:
            frame = self.camera.read()
            frame = imutils.resize(frame,self.width)

#             timestamp = datetime.datetime.now()
#             ts = timestamp.strftime("%A %d %B %Y %I %M:%S%p")
#             cv.putText(frame,ts,(10,frame.shape[0]-10),cv.FONT_HERSHEY_SIMPLEX,0.35,(0,0,255),1)

            cv.imshow("Frame",frame)
            key = cv.waitKey(1) & 0xFF

            if key == ord("q"):
                break
        cv.destroyAllWindows()
        camera.stop()

    

    def previewAllNew(self):
        font                   = cv.FONT_HERSHEY_PLAIN
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 1
        factor  = 20
        black = np.zeros(((self.height+factor)*2, self.width*2, 3), dtype= np.uint8)
        i = 0

        while True:
            
            for i in range(0,4):
                self.select_channel(chr(65+i))
                frame = self.camera.read()
    #             frame = imutils.resize(frame,self.width)
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
                
                
                cv.putText(black,'CAM '+index, bottomLeftCornerOfText, font, fontScale,fontColor,lineType)
                cv.imshow("Arducam Multi Camera Demo",black)

                key = cv.waitKey(1) & 0xFF

                if key == ord("q"):
                    break
        cv.destroyAllWindows()
        self.camera.stop()


    def preview(self):
        font                   = cv.FONT_HERSHEY_PLAIN
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 1
        factor  = 20
        black = np.zeros(((self.height+factor)*2, self.width*2, 3), dtype= np.uint8)
        i = 0
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
            if i==self.camNum:
                i = 0
            cv.putText(black,'CAM '+index, bottomLeftCornerOfText, font, fontScale,fontColor,lineType)
            cv.imshow("Arducam Multi Camera Demo",black)
            if cv.waitKey(1) & 0xFF == ord('q'):
                del frame
                self.camera.release()
                cv.destroyAllWindows()
                break
            
            
            
    def capture(self):
        import picamera
        import picamera.array
        
        
        
    def previewSingle(self,camNum):
        font                   = cv.FONT_HERSHEY_PLAIN
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 1
        factor  = 20
        black = np.zeros(((self.height+factor)*2, self.width*2, 3), dtype= np.uint8)
        i = 0
        while True:
            self.select_channel(chr(65+num_cam-1))
            ret, frame = self.camera.read()
            ret, frame = self.camera.read()
            ret, frame = self.camera.read()
            frame.dtype=np.uint8

            black[factor:factor+self.height, 0:self.width, :] = frame
            bottomLeftCornerOfText = (factor,factor)
            index = chr(65+num_cam-1)
            cv.putText(black,'CAM '+index,bottomLeftCornerOfText,font,fontScale,fontColor,lineType)
            cv.imshow("Arducam Single Camera",black)
            if cv.waitKey(1) & 0xFF == ord('q'):
                del frame
                self.camera.release()
                cv.destroyAllWindows()
                break
