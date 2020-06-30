
from datetime import datetime

class Angle():

	def __init__(self, mainController):
		self.mainController = mainController

	def get_angle_time(self):
		return (datetime.now().timestamp()-self.mainController.config.timeStamp)*self.mainController.config.angleTime
	
	def get_angle(self):
		return self.mainController.config.angle+self.get_angle_time()