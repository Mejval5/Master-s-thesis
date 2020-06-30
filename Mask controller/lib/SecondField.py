
from lib.Vortex import Vortex
from lib.MakeSquare import MakeSquare
from lib.ChangeCenter import ChangeCenter
import tkinter as tk


class SecondField():

	def __init__(self,mainController):
		self.mainController = mainController
		mainController.frame01Object = Frame1(self.mainController)
		mainController.newPatternLabel = NewPatternLabel(self.mainController)
		mainController.vortex = Vortex(self.mainController)
		mainController.square = MakeSquare(self.mainController)
		mainController.changeCenter = ChangeCenter(self.mainController)



class Frame1():

	def __init__(self,mainController):
		self.mainController = mainController
		self.make_frame01()

	def make_frame01(self):
		self.frame01 = tk.Frame(master=self.mainController.mainWindow, borderwidth=1, relief=tk.RAISED)
		self.frame01.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

class NewPatternLabel():

	def __init__(self,mainController):
		self.mainController = mainController
		self.make_new_pattern_label()

	def make_new_pattern_label(self):
		self.new_pattern_label = tk.Label(master=self.mainController.frame01Object.frame01, text="Generate new pattern")
		self.new_pattern_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)