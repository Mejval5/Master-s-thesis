import tkinter as tk

class InitializeWindow():

	def __init__(self, mainController):
		self.mainController = mainController
		self.initialize_window()

	def initialize_window(self):
		self.mainWindow = tk.Tk()
		self.mainWindow.geometry("+25+50")
		self.mainWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.mainWindow.title(self.mainController.config.name)

	def on_closing(self):
		self.mainController.second_column._send_data_light_only(0, 3)
		self.mainController.first_column.serial_port.close()
		self.mainController.second_column.serial_light_only.close()
		self.mainController.config.active=False

	def get_window(self):
		return self.mainWindow