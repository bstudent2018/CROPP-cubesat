from imutils.video import VideoStream
import AdapterBoard 
import numpy as np
from cameraapp import CameraApp
import tkinter as tk 




Arducam_adapter_board = AdapterBoard.MultiAdapter()
if __name__ == "__main__":
    
        
    Arducam_adapter_board.init(320,240)
#     Arducam_adapter_board.previewAllNew()
    root = tk.Tk()
    root.wm_protocol("WM_DELETE_WINDOW", lambda: root.quit())
    cam = CameraApp("~/Photos",root,Arducam_adapter_board)

    
