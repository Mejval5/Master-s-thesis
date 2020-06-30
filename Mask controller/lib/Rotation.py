from PIL import Image, ImageTk
import numpy as np
import cv2
import screeninfo
import time
import tkinter as tk
import fractions

class Rotation():


	def __init__(self,mainController):
		self.mainController = mainController
		self.width, self.height = (self.mainController.config.outputX*2 , self.mainController.config.outputY*2)
		self.imageMade = Image.new("L",(self.width,self.height))
		self.imageHolder = self.imageMade
		self.correctionFactor = self.mainController.config.correctionFactor/256
		self.outputX = self.mainController.config.outputX
		self.outputY = self.mainController.config.outputY
		self.centerX = self.mainController.config.centerX
		self.centerY = self.mainController.config.centerY
		self.changed_value = True
		self.last_angle = 0

	def phiVal(self):
		holder=np.indices((self.height,self.width))
		phi=np.arctan2(holder[0]-self.height/2,holder[1]-self.width/2)
		return(phi)

	def vortex(self,values=(0,2)):
		phi = self.phiVal()
		phiSin = (np.sin((values[0]+phi)*(values[1]-values[0])/2)+1)/2
		val = np.mod(phiSin*1,1.0001)*self.correctionFactor*256/2
		self.imageMade=Image.fromarray(val)

	def square(self, values=(0,1,1,0)):
		phi = self.phiVal()
		phiS = np.sin(phi)
		phiC = np.cos(phi)
		phi[(phiS<=0) * (phiC<=0)]=values[0]
		phi[(phiS>=0) * (phiC<=0)]=values[1]
		phi[(phiS<=0) * (phiC>=0)]=values[2]
		phi[(phiS>=0) * (phiC>=0)]=values[3]
		val=np.mod(phi,2.0001)*self.correctionFactor*256/2
		self.imageMade=Image.fromarray(val)

	def rotate_image(self,angle=0):
		if self.changed_value or self.last_angle is not angle:
			self.imageRotated=self.imageMade.rotate(angle)
			self.crop_image()
			self.changed_value = False
			self.last_angle = angle

	def crop_image(self):
			width, height = self.imageRotated.size
			minX=width*self.centerX-self.outputX*self.centerX
			maxX=width*self.centerX+self.outputX*(1-self.centerX)
			minY=height*self.centerY-self.outputY*self.centerY
			maxY=height*self.centerY+self.outputY*(1-self.centerY)
			self.imageHolder = self.imageRotated.crop((minX, minY, maxX, maxY))

	def set_center(self, x, y):
		self.centerX=1-x
		self.centerY=y
		self.changed_value = True

	def changed_value(self):
		self.changed_value = True