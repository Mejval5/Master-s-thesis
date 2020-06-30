

class Loop():

	def __init__(self, mainController):
		self.mainController = mainController
		self.mainController.rotationObject.square(self.mainController.square.get_square_values())
		self.main_loop()

	def main_loop(self):
		while self.mainController.config.active:
			self.mainController.fourthField.update_images()
			self.mainController.mainWindow.update_idletasks()
			self.mainController.mainWindow.update()
			if self.mainController.thirdField.windowDisplayCheckboxVariable.get()==1:
				self.mainController.display.fullscreen_image()
