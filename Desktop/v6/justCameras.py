

from camerawidget import cameraWidget
from AdapterBoard import *
import time
import tkinter as tk
import logging
import CROPPguiAUTO

def activateCameras(root):

    print("[INFO] warming up camera...")

    #logging.basicConfig(level=logging.DEBUG)

    vs = WebcamVideoStream().start()
    time.sleep(2.0)

    auto = True

    if auto:
        CROPPguiAUTO.connect()
    
    # start the  widget
    pba = cameraWidget(root,vs, "output")
    pba.startThreads()
    print("threads starting")
    
    if auto:
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