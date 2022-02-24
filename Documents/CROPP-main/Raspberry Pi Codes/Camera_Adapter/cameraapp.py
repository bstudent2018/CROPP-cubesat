# import the necessary packages
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading
import datetime
import imutils
import cv2
import os

class CameraApp:
	def __init__(self, outputPath,root,multiAdapter):
		# store the video stream object and output path, then initialize
		# the most recently read frame, thread for reading frames, and
		# the thread stop event
		self.vs = multiAdapter.vs
		self.multiAdapter = multiAdapter
		self.outputPath = outputPath
		self.frame = None
		self.thread = None
		self.stopEvent = None

		# initialize the root window and image panel
		self.root = root
		self.panel = [None] * multiAdapter.camNum

		# create a button, that when pressed, will take the current
		# frame and save it to file
		for i in range(0,4):
			btn = tk.Button(self.root, text="Snapshot!",
				command=lambda: self.takeSnapshot(i))
			btn.grid(side="bottom", fill="both", expand="yes", padx=10,
				pady=10)

		# start a thread that constantly pools the video sensor for
		# the most recently read frame
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()

		# set a callback to handle when the window is closed

		self.root.wm_title("PyImageSearch PhotoBooth")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoLoop(self):
		# DISCLAIMER:
		# I'm not a GUI developer, nor do I even pretend to be. This
		# try/except statement is a pretty ugly hack to get around
		# a RunTime error that Tkinter throws due to threading
		try:
			# keep looping over frames until we are instructed to stop
			while not self.stopEvent.is_set():


				for i in range(0,4):
					# self.multiAdapter.select_channel(chr(65+i))
				# grab the frame from the video stream and resize it to
				# have a maximum width of 300 pixels
					# self.frame = self.vs.read()
					# self.frame = imutils.resize(self.frame, width=300)


					self.frame = self.multiAdapter.getFrame(i)


					# OpenCV represents images in BGR order; however PIL
					# represents images in RGB order, so we need to swap
					# the channels, then convert to PIL and ImageTk format
					image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
					image = Image.fromarray(image)
					image = ImageTk.PhotoImage(image)

					# if the panel is not None, we need to initialize it
					if self.panel[i] is None:
						self.panel[i] = tk.Label(image=image)
						self.panel[i].image = image
						self.panel[i].grid(column = i%2,row = i >> 1)
					# otherwise, simply update the panel
					else:
						self.panel[i].configure(image=image)
						self.panel[i].image = image

		except RuntimeError:
			print("[INFO] caught a RuntimeError")

	def takeSnapshot(self,ind):
		# grab the current timestamp and use it to construct the
		# output path
		ts = datetime.datetime.now()
		filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
		p = os.path.sep.join((self.outputPath, filename))

		# save the file
		self.multiAdapter.select_channel(chr(65+ind))
		self.frame = self.vs.read()
		self.frame = imutils.resize(self.frame,width=300)
		cv2.imwrite(p, self.frame.copy())
		print("[INFO] saved {}".format(filename))

	def onClose(self):
		# set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
		print("[INFO] closing...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()
