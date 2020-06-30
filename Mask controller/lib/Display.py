from datetime import datetime
import screeninfo
import cv2
import numpy as np

class Display():

	def __init__(self, mainController):
		self.mainController = mainController
		self.get_displays()
		self.get_display_resolution()
		self.make_display_name()

	def setup_display(self):
		self.make_display_name()
		cv2.namedWindow(self.mainController.display_name, cv2.WND_PROP_FULLSCREEN)
		cv2.moveWindow(self.mainController.display_name, self.screen.x - 1, self.screen.y - 1)
		cv2.setWindowProperty(self.mainController.display_name, cv2.WND_PROP_FULLSCREEN,
							  cv2.WINDOW_FULLSCREEN)

	def make_display_name(self):
		self.mainController.display_name = 'Window' + str(self.mainController.config.monitor)

	def setup_display_window(self):
		cv2.destroyAllWindows()
		if self.mainController.thirdField.windowDisplayCheckboxVariable.get()==1:
			self.get_display_resolution()
			self.setup_display()

	def is_display_closed(self):
		return cv2.getWindowProperty(self.mainController.display_name, cv2.WND_PROP_VISIBLE)<1

	def close_display(self):
		self.mainController.thirdField.windowDisplayCheckboxVariable.set(0)
		cv2.destroyAllWindows()

	def fullscreen_image(self):
		if self.is_display_closed():
			self.close_display()
		else:
			self.convert_image_to_display()
			self.show_image_on_display()

	def convert_image_to_display(self):
		self.imageArray = np.array(self.mainController.rotationObject.imageHolder)/256

	def show_image_on_display(self):
		cv2.imshow(self.mainController.display_name, self.imageArray)

	def get_display_resolution(self):
		while True:
			try:
				self.screen = screeninfo.get_monitors()[self.mainController.config.monitor]
				self.screenWidth, self.screenHeight = self.screen.width, self.screen.height
			except :
				continue
			else:
				break

	def get_displays(self):
		# Sometimes monitors do not show up for some reason, so it is necessary to do more iterations to really get all of them.
		self.monitorHolder={}
		t=datetime.now().timestamp()+self.mainController.config.waitForDisplays
		while True:
			try:
				monitors = screeninfo.get_monitors()
				if len(monitors)>len(self.monitorHolder):
					self.monitorHolder=monitors
			except:
				continue
			else:
				if t<datetime.now().timestamp():
					break
		self.format_displays()

	def format_displays(self):
		for display in self.monitorHolder:
			index = self.monitorHolder.index(display)
			disp = "Screen " + str(index) + ": " + str(display.width) + " x " + str(display.height)
			self.monitorHolder[index]=disp
