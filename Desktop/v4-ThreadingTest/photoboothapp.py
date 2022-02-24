# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
import time
import logging

class PhotoBoothApp:
	def __init__(self, root,vs, outputPath):
		# store the video stream object and output path, then initialize
		# the most recently read frame, thread for reading frames, and
		# the thread stop event
		self.vs = vs
		self.outputPath = outputPath
		self.frame = [None,None,None,None]

		self._lock = threading.Lock()
		self._update_lock = threading.Lock()
		self.thread = None
		self.stopEvent = None

		# initialize the root window and image panel
		#self.root = tki.Tk()
		self.root = root
		self.panel = [None,None,None,None]
		self.images = [None,None,None,None]
		# create a button, that when pressed, will take the current
		# frame and save it to file
		btnA = tki.Button(self.root, text="Snapshot A",
			command=lambda: self.takeSnapshot(0))
		btnA.grid(row=1,column=0, padx=10,
			pady=10)
		
		btnB = tki.Button(self.root, text="Snapshot B",
			command=lambda: self.takeSnapshot(1))
		btnB.grid(row=1,column=1 , padx=10,
			pady=10)
		
		btnC = tki.Button(self.root, text="Snapshot C",
			command=lambda: self.takeSnapshot(2))
		btnC.grid(row=1,column=2, padx=10,
			pady=10)
		
		btnD = tki.Button(self.root, text="Snapshot D",
			command=lambda: self.takeSnapshot(3))
		btnD.grid(row=1,column=3,  padx=10,
			pady=10)



		# start a thread that constantly pools the video sensor for
		# the most recently read frame
		self.stopEvent = threading.Event()
		
        #self.thread = threading.Thread(target=self.videoLoop, args=())
		#self.thread.start()
        
		self.aThread = threading.Thread(target=self.singleCamLoop,args=(0,))
		self.bThread = threading.Thread(target=self.singleCamLoop,args=(1,))
		self.cThread = threading.Thread(target=self.singleCamLoop,args=(2,))
		self.dThread = threading.Thread(target=self.singleCamLoop,args=(3,))

		self.mainThread = threading.Thread(target=self.mainUpdateLoop,args=())
        
		# set a callback to handle when the window is closed
    
		#self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
    
    
	def startThreads(self):
		#self.mainThread.start()
		self.aThread.start()
		
		self.bThread.start()
		
		self.cThread.start()

		self.dThread.start()




	def mainUpdateLoop(self):
		#time.sleep(0.1)
		#with self._update_lock:
		
		for index in range(4):
# 			if self.images[index] is None:
# 				continue
			if self.panel[index] is None:
				self.panel[index] = tki.Label(image=self.images[index])
				self.panel[index].image = self.images[index]
				self.panel[index].pack(side="left", padx=10, pady=10)
			# otherwise, simply update the panel
			else:
				self.panel[index].configure(image=self.images[index])
				self.panel[index].image = self.images[index]


	def singleCamLoop(self,index):
		try:
			while not self.stopEvent.is_set():
                ######   LOCK   ######
				with self._lock:
					logging.debug("Thread %s accesing GPIO",index)
					self.vs.adapter.select_channel(chr(65+index))
					self.frame[index] = self.vs.read()
					self.frame[index] = self.vs.read()
					logging.debug("Thread %s finished with GPIO",index)
				######  UNLOCK  ######
				self.frame[index] = imutils.resize(self.frame[index], width=320)
				time.sleep(0.1)
				image = cv2.cvtColor(self.frame[index], cv2.COLOR_BGR2RGB)
				#image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image=Image.fromarray(image))
				with self._update_lock:
					time.sleep(0.075)
					self.images[index] = image
					if self.panel[index] is None:
						self.panel[index] = tki.Label(image=image)
						self.panel[index].image = image
						self.panel[index].grid(row=0,column=index, padx=10, pady=10)
				# otherwise, simply update the panel
					else:
						self.panel[index].configure(image=image)
						self.panel[index].image = image
		except RuntimeError:
			print("[INFO] caught a RuntimeError")


	def camALoop(self):
		try:
			while not self.stopEvent.is_set():
				time.sleep(0.1)                
				self.vs.adapter.select_channel('A')
				self.frame[0] = self.vs.read()
				self.frame[0] = imutils.resize(self.frame[0], width=300)
            
				image = cv2.cvtColor(self.frame[0], cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
				if self.panel[0] is None:
					self.panel[0] = tki.Label(image=image)
					self.panel[0].image = image
					self.panel[0].pack(side="left", padx=10, pady=10)
            # otherwise, simply update the panel
				else:
					self.panel[0].configure(image=image)
					self.panel[0].image = image
		except RuntimeError:
			print("[INFO] caught a RuntimeError")

	def camBLoop(self):
		try:
			while not self.stopEvent.is_set():
				time.sleep(0.1) 
				self.vs.adapter.select_channel('B')
				self.frameB = self.vs.read()
				self.frameB = imutils.resize(self.frameB, width=300)
            
				image = cv2.cvtColor(self.frameB, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
				if self.panel[1] is None:
					self.panel[1] = tki.Label(image=image)
					self.panel[1].image = image
					self.panel[1].pack(side="left", padx=10, pady=10)
            # otherwise, simply update the panel
				else:
					self.panel[1].configure(image=image)
					self.panel[1].image = image
					
					
		except RuntimeError:
			print("[INFO] caught a RuntimeError")

	def camCLoop(self):
		try:
			while not self.stopEvent.is_set():
				time.sleep(0.1) 
				self.vs.adapter.select_channel('C')
				self.frameC = self.vs.read()
				self.frameC = imutils.resize(self.frameC, width=300)
            
				image = cv2.cvtColor(self.frameC, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
				if self.panel[2] is None:
					self.panel[2] = tki.Label(image=image)
					self.panel[2].image = image
					self.panel[2].pack(side="left", padx=10, pady=10)
            # otherwise, simply update the panel
				else:
					self.panel[2].configure(image=image)
					self.panel[2].image = image
		except RuntimeError:
			print("[INFO] caught a RuntimeError")

	def camDLoop(self):
		try:
			while not self.stopEvent.is_set():
				time.sleep(0.1) 
				self.vs.adapter.select_channel('D')
				self.frameD = self.vs.read()
				self.frameD = imutils.resize(self.frameD, width=300)
            
				image = cv2.cvtColor(self.frameD, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
				if self.panel[3] is None:
					self.panel[3] = tki.Label(image=image)
					self.panel[3].image = image
					self.panel[3].pack(side="left", padx=10, pady=10)
            # otherwise, simply update the panel
				else:
					self.panel[3].configure(image=image)
					self.panel[3].image = image
		except RuntimeError:
			print("[INFO] caught a RuntimeError")

    

    
	def videoLoop(self):
		# DISCLAIMER:
		# I'm not a GUI developer, nor do I even pretend to be. This
		# try/except statement is a pretty ugly hack to get around
		# a RunTime error that Tkinter throws due to threading
		try:
			# keep looping over frames until we are instructed to stop
			while not self.stopEvent.is_set():
				for i in [0,1,2,3]:
					self.vs.adapter.select_channel(chr(65+i))
					time.sleep(0.1)
					# grab the frame from the video stream and resize it to
					# have a maximum width of 300 pixels
					self.frame[i] = self.vs.read()
					self.frame[i] = self.vs.read()
					self.frame[i] = self.vs.read()
					self.frame[i] = imutils.resize(self.frame[i], width=320)
            
					# OpenCV represents images in BGR order; however PIL
					# represents images in RGB order, so we need to swap
					# the channels, then convert to PIL and ImageTk format
					image = cv2.cvtColor(self.frame[i], cv2.COLOR_BGR2RGB)
					image = Image.fromarray(image)
					image = ImageTk.PhotoImage(image)
					# if the panel is not None, we need to initialize it
					if self.panel[i] is None:
						self.panel[i] = tki.Label(image=image)
						self.panel[i].image = image
						self.panel[i].pack(side="left", padx=10, pady=10)
					# otherwise, simply update the panel
					else:
						self.panel[i].configure(image=image)
						self.panel[i].image = image

		except RuntimeError:
			print("[INFO] caught a RuntimeError")

	def timelapse(self,interval):
		while not self.stopEvent.is_set():
			time.sleep(interval)
			for i in range(4):
				ts = datetime.datetime.now()
				filename = "CAM{}_{}.jpg".format(chr(65+i),ts.strftime("%Y-%m-%d_%H:%M:%S"))
				p = os.path.sep.join((self.outputPath, filename))

				# save the file
				cv2.imwrite(p, self.frame[i].copy())
				print("[INFO] saved {}".format(p))

	def takeSnapshot(self,i):
		# grab the current timestamp and use it to construct the
		# output path
		
		
		
		
		ts = datetime.datetime.now()
		filename = "CAM{}_{}.jpg".format(chr(65+i),ts.strftime("%Y-%m-%d_%H:%M:%S"))
		p = os.path.sep.join((self.outputPath, filename))

		# save the file
		cv2.imwrite(p, self.frame[i].copy())
		print("[INFO] saved {}".format(p))

	def onClose(self):
		# set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
		print("[INFO] closing...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()