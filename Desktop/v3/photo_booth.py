# USAGE
# python photo_booth.py --output output

# import the necessary packages

from photoboothapp import PhotoBoothApp
from AdapterBoard import *
import time
import tkinter as tk


# initialize the video stream and allow the camera sensor to warmup

def activateCameras(root):

    print("[INFO] warming up camera...")

    vs = WebcamVideoStream().start()
    time.sleep(2.0)

    # start the app
    pba = PhotoBoothApp(root,vs, "output")
    #pba.startThreads()
    pba.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    activateCameras(root)
