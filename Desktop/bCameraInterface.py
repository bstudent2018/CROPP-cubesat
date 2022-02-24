

from picamera import PiCamera
#from AdapterBoard import *
import time
import tkinter as tk
import logging

camera = PiCamera()

def activateCameras(root):

    print("[INFO] warming up camera...")

    #logging.basicConfig(level=logging.DEBUG)

    vs = camera.start_preview()
    time.sleep(2.0)
    camera.stop_preview()
    
    # start the  widget
    pba = camera
    print("threads starting")
    autoTimelapse(pba)
    
    
#     while True:
#         pba.root.update()
    pba.root.mainloop()

def autoTimelapse(app):
    time.sleep(1)
    lapse = threading.Thread(target=app.timelapse,args=(21600,))
    lapse.start()
    


if __name__ == "__main__":
    root = tk.Tk()
    activateCameras(root)

