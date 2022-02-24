import AdapterBoard 
import cv2 as cv 
import numpy as np
from cameraapp import CameraApp
from AdapterBoard import MultiAdapter
import tkinter as tk
import datetime
import os

Arducam_adapter_board = AdapterBoard.MultiAdapter()
if __name__ == "__main__":
    os.system("i2cset -y 1 0x70 0x00 0x04")
    Arducam_adapter_board.init(320,240)
    
    ts = datetime.datetime.now()
    filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
    p = os.path.sep.join(("", filename))
    
    frame = Arducam_adapter_board.getFrame(1)
    # save the file
    cv.imwrite(p, frame)
    print("[INFO] saved {}".format(filename))

#     root = tk.Tk()
#     cam = CameraApp("/",root,