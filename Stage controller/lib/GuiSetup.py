import tkinter as tk

from lib.FirstColumn import FirstColumn
from lib.SecondColumn import SecondColumn

class GuiSetup():


	def __init__(self,mainController):
		self.mainController = mainController
		self._gui_load()

	def _gui_load(self):
		self._rows_and_columns()

		self._first_column()
		self._second_column()


	def _first_column(self):
		self.mainController.first_column = FirstColumn(self.mainController)

	def _second_column(self):
		self.mainController.second_column = SecondColumn(self.mainController)

	def _rows_and_columns(self):
		self._configure_first_column()

	def _configure_first_column(self):
		self.mainController.mainWindow.columnconfigure(0, weight=1, minsize=220)
		self.mainController.mainWindow.columnconfigure(1, weight=1, minsize=75)
