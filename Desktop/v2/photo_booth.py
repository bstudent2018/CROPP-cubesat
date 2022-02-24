# USAGE
# python photo_booth.py --output output

# import the necessary packages
from __future__ import print_function
from photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import argparse
import time
from newCamAdapter import CamAdapter




adapter = CamAdapter()


# start the app
pba = PhotoBoothApp("",adapter)
pba.root.mainloop()