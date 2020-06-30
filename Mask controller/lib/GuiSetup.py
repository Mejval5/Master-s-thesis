import tkinter as tk

from lib.FirstField import FirstField
from lib.SecondField import SecondField
from lib.FourthField import FourthField
from lib.ThirdField import ThirdField

class GuiSetup():


	def __init__(self,mainController):
		self.mainController = mainController
		self.gui_setup()

	def gui_setup(self):
		self.setup_rows_and_columns()

		self.setup_first_column()
		self.setup_second_column()

		self.mainController.display.setup_display_window()

	def setup_first_column(self):
		self.mainController.firstField = FirstField(self.mainController)
		self.mainController.secondField = SecondField(self.mainController)

	def setup_second_column(self):
		self.mainController.thirdField = ThirdField(self.mainController)
		self.mainController.fourthField = FourthField(self.mainController)

	def setup_rows_and_columns(self):
		self.configure_first_row()
		self.configure_second_row()

	def configure_first_row(self):
		self.mainController.mainWindow.rowconfigure(0, weight=1, minsize=50)

	def configure_second_row(self):
		self.mainController.mainWindow.rowconfigure(1, weight=1, minsize=50)

	def configure_first_column(self):
		self.mainController.mainWindow.columnconfigure(0, weight=1, minsize=75)

