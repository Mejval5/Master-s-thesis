

class Loop():

	def __init__(self, mainController):
		self.mainController = mainController
		self.main_loop()

	def main_loop(self):
		while self.mainController.config.active:
			self.mainController.mainWindow.update_idletasks()
			self.mainController.mainWindow.update()
			if hasattr(self.mainController,"line_plot_window"):
				if self.mainController.line_plot_window is not None:
					self.mainController.line_plot_window.update_idletasks()
					self.mainController.line_plot_window.update()
