# USAGE
# python photo_booth.py --output output

# import the necessary packages

from photoboothapp import PhotoBoothApp
from AdapterBoard import *
import time
import tkinter as tk
import logging

# initialize the video stream and allow the camera sensor to warmup

def activateCameras(root):

    print("[INFO] warming up camera...")
    
    #logging.basicConfig(level=logging.DEBUG)
    
    vs = WebcamVideoStream().start()
    time.sleep(2.0)
    

    # start the app
    pba = PhotoBoothApp(root,vs, "output")
    pba.startThreads()
    print("threads starting")
    #autoTimelapse(pba)
    #while True and pba.root:
    #    pba.root.update()
    pba.root.mainloop()

def autoTimelapse(app):
    lapse = threading.Thread(target=app.timelapse,args=(5,))
    lapse.start()


if __name__ == "__main__":
    root = tk.Tk()
    activateCameras(root)
