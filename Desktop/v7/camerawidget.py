# import the necessary packages
##from __future__ import print_function
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

class cameraWidget:
	"""
	Creates and controls Tkinter Camera Widget

	Contstructor Values
	-------------------
	root : Tkinter Window
		Tkinter window to create camera display in 
	vs : Video Stream
		Active video stream from cameras
	outputPath:
		Desired path for photo output
    
    
	Attributes
	----------
	frame : 
		List of frames to store photo arrays
	_switching_lock : threading lock
		Threading lock to only allow one thread to change GPIO at a time
	_update_lock : threading lock
		Threading lock to only allow one thread to change tkinter window at a time (Tkinter is only slightly thread-safe)
	stopEvent : threading event
		Threading event to signal end of program to threads
    
    
	Methods
	-------
	startThreads() : 
		Starts threads for each camera to get outputs
	singleCamLoop (index) :
		index : Int
			ID of camera, 0-3 ('A'-'D')
		Method for each thread to get respective photo and update tkinter display
	timelapse(interval)
		interval : Int 
			Time between photos, in seconds
		Takes photos on each camera every interval seconds
	takeSnapshot(i)
		i : Int
			Camera id 
		Saves last frame from given camera 
	onClose()
		Runs on close of tkinter window to stop threads and camera video stream
	"""


	def __init__(self, root,vs, outputPath):
		self.vs = vs
		self.outputPath = outputPath
		self.frame = [None,None,None,None]

		self._switching_lock = threading.Lock()
		self._update_lock = threading.Lock()
		
		self.stopEvent = threading.Event()

		self.root = root
		self.panel = [None,None,None,None]
		self.images = [None,None,None,None]


        #Make Camera Snapshot buttons
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

        #Initialize threads 
		self.aThread = threading.Thread(target=self.singleCamLoop,args=(0,))
		self.bThread = threading.Thread(target=self.singleCamLoop,args=(1,))
		self.cThread = threading.Thread(target=self.singleCamLoop,args=(2,))
		self.dThread = threading.Thread(target=self.singleCamLoop,args=(3,))

		self.mainThread = threading.Thread(target=self.mainUpdateLoop,args=())

        #Tkinter protocol to run onClose when window is closed
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)


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

			else:
				self.panel[index].configure(image=self.images[index])
				self.panel[index].image = self.images[index]


	def singleCamLoop(self,index):
        #Try/except fixes tkinter threading issue
		try:
			while not self.stopEvent.is_set():
                ######   LOCK   ######
				with self._switching_lock:
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

					else:
						self.panel[index].configure(image=image)
						self.panel[index].image = image
		except RuntimeError:
			print("[INFO] caught a RuntimeError")
			
	def cameraFlash(self,auto):
		auto.flashToggle()
		time.sleep(1)
        
	def lightsOnSunday(self,auto):
		time.sleep(60)
		auto.flashToggle()
		
		time.sleep(86400)
		auto.flashToggle()


	def timelapse(self,interval,auto):
		for i in range(4):
				ts = datetime.datetime.now()
				filename = "{}_{}.jpg".format(chr(65+i),ts.strftime("%Y-%m-%d_%H%M%S"))
				p = os.path.sep.join((self.outputPath, filename))

				time.sleep(0.5)
				cv2.imwrite(p, self.frame[i].copy())
				print("[INFO] saved {}".format(p))
		self.cameraFlash(auto)
		while not self.stopEvent.is_set():
			time.sleep(interval)
			self.cameraFlash(auto)
			time.sleep(1.5) #Allows for cameras to refocus to light
			for i in range(4):
				ts = datetime.datetime.now()
				filename = "{}_{}.jpg".format(chr(65+i),ts.strftime("%Y-%m-%d_%H%M%S"))
				p = os.path.sep.join((self.outputPath, filename))

				time.sleep(0.5)
				cv2.imwrite(p, self.frame[i].copy())
				print("[INFO] saved {}".format(p))
			self.cameraFlash(auto)

	def takeSnapshot(self,i):

		ts = datetime.datetime.now()
		filename = "{}_{}.jpg".format(chr(65+i),ts.strftime("%Y-%m-%d_%H%M%S"))
		p = os.path.sep.join((self.outputPath, filename))


		cv2.imwrite(p, self.frame[i].copy())
		print("[INFO] saved {}".format(p))




	def onClose(self):

		print("[INFO] closing...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()
