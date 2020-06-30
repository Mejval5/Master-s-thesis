import tkinter as tk

class InitializeWindow():

	def __init__(self, mainController):
		self.mainController = mainController
		self.initialize_window()

	def initialize_window(self):
		self.mainWindow = tk.Tk()
		self.mainWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.mainWindow.title(self.mainController.config.name)

	def on_closing(self):
		self.mainController.config.active=False

	def get_window(self):
		return self.mainWindow