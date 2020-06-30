import time

class Loop():

	def __init__(self, mainController):
		self.mainController = mainController
		self.time_stamp = time.time()
		self.time_wait = 0.25
		self.shutter_spin = 2.0
		self.main_loop()

	def main_loop(self):
		while self.mainController.config.active:
			self.mainController.mainWindow.update_idletasks()
			self.mainController.mainWindow.update()
			if self.mainController.first_column.moving and (self.time_stamp+self.time_wait) < time.time():
				self.mainController.first_column._send_data(self.mainController.first_column.curr_dir, self.mainController.first_column.curr_axis)
				self.time_stamp = time.time()

			if hasattr(self.mainController,"line_plot_window"):
				if self.mainController.line_plot_window is not None:
					self.mainController.line_plot_window.update_idletasks()
					self.mainController.line_plot_window.update()

			if str(self.mainController.second_column.shutter_toggle['state']) == "disabled" and (self.mainController.second_column.time_stamp + self.shutter_spin) < time.time():
				self.mainController.second_column.shutter_toggle.configure(state="active")
