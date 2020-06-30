import tkinter as tk

from lib.FirstColumn import FirstColumn
from lib.SecondColumn import SecondColumn
from lib.ThirdColumn import ThirdColumn
from lib.FourthColumn import FourthColumn

class GuiSetup():


	def __init__(self,mainController):
		self.mainController = mainController
		self._gui_load()

	def _gui_load(self):
		self._rows_and_columns()

		self._first_column()
		self._second_column()
		self._third_column()
		self._fourth_column()


	def _first_column(self):
		self.mainController.first_column = FirstColumn(self.mainController)

	def _second_column(self):
		self.mainController.second_column = SecondColumn(self.mainController)

	def _third_column(self):
		self.mainController.third_column = ThirdColumn(self.mainController)

	def _fourth_column(self):
		self.mainController.fourth_column = FourthColumn(self.mainController)


	def _rows_and_columns(self):
		self._configure_first_column()
		self._configure_second_column()
		self._configure_third_column()

	def _configure_first_column(self):
		self.mainController.mainWindow.columnconfigure(0, weight=1, minsize=800)

	def _configure_second_column(self):
		self.mainController.mainWindow.columnconfigure(1, weight=1, minsize=150)

	def _configure_third_column(self):
		self.mainController.mainWindow.columnconfigure(2, weight=1, minsize=200)
