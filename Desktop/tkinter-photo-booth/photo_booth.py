# USAGE
# python photo_booth.py --output output

# import the necessary packages
from __future__ import print_function
from pyimagesearch.photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import argparse
import time
from pyimagesearch.AdapterBoard import MultiAdapter

# construct the argument parse and parse the arguments


# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
adapter = MultiAdapter()
adapter.Init(320,240)
adapter.selectChannel(1)
vs = adapter.camera
time.sleep(2.0)

# start the app
pba = PhotoBoothApp(vs, args["output"])
pba.root.mainloop()