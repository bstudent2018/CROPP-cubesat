

from picamera import PiCamera
#from AdapterBoard import *
import time
import tkinter as tk
import logging
import CROPPguiAUTO

def activateCameras(root):

    print("[INFO] warming up camera...")

    #logging.basicConfig(level=logging.DEBUG)

    vs = WebcamVideoStream().start()
    time.sleep(2.0)

    CROPPguiAUTO.connect()
    
    # start the  widget
    pba = cameraWidget(root,vs, "output")
    pba.startThreads()
    print("threads starting")
    autoTimelapse(pba)
    
    
#     while True:
#         pba.root.update()
    pba.root.mainloop()

def autoTimelapse(app):
    auto = CROPPguiAUTO.Autonomouos()
    auto.lightThread.start()
    time.sleep(1)
    lapse = threading.Thread(target=app.timelapse,args=(21600,))
    lapse.start()
    


if __name__ == "__main__":
    root = tk.Tk()
    activateCameras(root)
