

from camerawidget import cameraWidget
from AdapterBoard import *
import time
import tkinter as tk
import logging
import CROPPguiAUTO

def activateCameras(root):
    """
    Initializes cameras and starts up Tkinter camera GIO
    
    
    """



    

    #Indicates if the autonomous mode should be started
    automatic = True
    
    #Initializes camera stream
    print("[INFO] warming up camera...")
    vs = WebcamVideoStream().start()
    time.sleep(2.0)

    
    if automatic:
        CROPPguiAUTO.connect()
        
    
    # start the  widget
    camDisplay = cameraWidget(root,vs, "output")
    camDisplay.startThreads()
    print("threads starting")

    if automatic:
        autoTimelapse(camDisplay)
    
    
#     while True:
#         camDisplay.root.update()
    camDisplay.root.mainloop()




def autoTimelapse(display):
    """
    display : 
             Camera display widget
        
    Starts threads for photo capture and light switching
    
    
    """


    auto = CROPPguiAUTO.Autonomouos()
    sunday = threading.Thread(target=display.lightsOnSunday,args=(auto,))
    sunday.start()
    #auto.lightThread.start()
    #time.sleep(1)
    lapse = threading.Thread(target=display.timelapse,args=(21600,auto))
    lapse.start()
    


if __name__ == "__main__":
    root = tk.Tk()
    activateCameras(root)
