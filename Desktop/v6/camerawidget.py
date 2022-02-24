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
	def __init__(self, root,vs, outputPath):


		self.vs = vs
		self.outputPath = outputPath
		self.frame = [None,None,None,None]

		self._lock = threading.Lock()
		self._update_lock = threading.Lock()
		self.thread = None
		self.stopEvent = None


		#self.root = tki.Tk()
		self.root = root
		self.panel = [None,None,None,None]
		self.images = [None,None,None,None]


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




		self.stopEvent = threading.Event()

        #self.thread = threading.Thread(target=self.videoLoop, args=())
		#self.thread.start()

		self.aThread = threading.Thread(target=self.singleCamLoop,args=(0,))
		self.bThread = threading.Thread(target=self.singleCamLoop,args=(1,))
		self.cThread = threading.Thread(target=self.singleCamLoop,args=(2,))
		self.dThread = threading.Thread(target=self.singleCamLoop,args=(3,))

		self.mainThread = threading.Thread(target=self.mainUpdateLoop,args=())



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

					else:
						self.panel[index].configure(image=image)
						self.panel[index].image = image
		except RuntimeError:
			print("[INFO] caught a RuntimeError")



	def timelapse(self,interval):
		while not self.stopEvent.is_set():
			time.sleep(interval)
			for i in range(4):
				ts = datetime.datetime.now()
				filename = "CAM{}_{}.jpg".format(chr(65+i),ts.strftime("%Y-%m-%d_%H:%M:%S"))
				p = os.path.sep.join((self.outputPath, filename))

				time.sleep(0.5)
				cv2.imwrite(p, self.frame[i].copy())
				print("[INFO] saved {}".format(p))

	def takeSnapshot(self,i):





		ts = datetime.datetime.now()
		filename = "CAM{}_{}.jpg".format(chr(65+i),ts.strftime("%Y-%m-%d_%H:%M:%S"))
		p = os.path.sep.join((self.outputPath, filename))


		cv2.imwrite(p, self.frame[i].copy())
		print("[INFO] saved {}".format(p))

	def onClose(self):

		print("[INFO] closing...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()
