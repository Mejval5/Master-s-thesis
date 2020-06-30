
import tkinter as tk

from lib.HelperMethods import *

class Vortex():

	def __init__(self,mainController):
		self.mainController = mainController
		self.make_vortex()

	def make_vortex(self):
		self.create_vortex_frame()
		self.create_vortex_label()
		self.create_vortex_range_frame()
		self.create_vortex_range_min()
		self.create_vortex_range_max()
		self.create_vortex_set_button()	


	def create_vortex_frame(self):
		self.frame_vortex = tk.Frame(master=self.mainController.frame01Object.frame01, borderwidth=1, relief=tk.RAISED)
		self.frame_vortex.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

	def create_vortex_label(self):
		self.vortex_label = tk.Label(master=self.frame_vortex, text="Vortex")
		self.vortex_label.grid(row=0,column=0, padx=5, pady=5)

	def create_vortex_range_frame(self):
		self.vortex_range_frame = tk.Frame(master=self.frame_vortex, borderwidth=1)
		self.vortex_range_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

	def create_vortex_range_min_frame(self):
		self.range_min_frame = tk.Frame(master=self.vortex_range_frame,width=10)
		self.range_min_frame.grid(row=0,column=0, padx=5, pady=5)

	def create_vortex_range_min_entry(self):
		self.range_min_entry_variable = tk.StringVar()
		self.range_min_entry_variable.set("0.0")
		self.range_min_entry = tk.Entry(master=self.range_min_frame,width=10,textvariable=self.range_min_entry_variable,justify='right')
		self.range_min_entry.grid(row=1,column=0, padx=5, pady=5)

	def create_vortex_range_min_pi_label(self):
		self.range_min_label = tk.Label(master=self.range_min_frame, text="\u03C0")
		self.range_min_label.grid(row=1,column=1, padx=0, pady=5)

	def create_vortex_range_min_label(self):
		self.range_min_label = tk.Label(master=self.range_min_frame, text="Min")
		self.range_min_label.grid(row=0,column=0, padx=0, pady=5)

	def create_vortex_range_max_frame(self):
		self.range_max_frame = tk.Frame(master=self.vortex_range_frame,width=10)
		self.range_max_frame.grid(row=0,column=1, padx=5, pady=5)

	def create_vortex_range_max_entry(self):
		self.range_max_entry_variable = tk.StringVar()
		self.range_max_entry_variable.set("2.0")
		self.range_max_entry = tk.Entry(master=self.range_max_frame,width=10,textvariable=self.range_max_entry_variable,justify='right')
		self.range_max_entry.grid(row=1,column=0, padx=5, pady=5)

	def create_vortex_range_max_label(self):
		self.range_min_label = tk.Label(master=self.range_max_frame, text="Max")
		self.range_min_label.grid(row=0,column=0, padx=0, pady=5)

	def create_vortex_range_max_pi_label(self):
		self.range_max_label = tk.Label(master=self.range_max_frame, text="\u03C0")
		self.range_max_label.grid(row=1,column=1, padx=0, pady=5)

	def create_vortex_range_min(self):
		self.create_vortex_range_min_frame()
		self.create_vortex_range_min_entry()
		self.create_vortex_range_min_label()
		self.create_vortex_range_min_pi_label()

	def create_vortex_range_max(self):
		self.create_vortex_range_max_frame()
		self.create_vortex_range_max_entry()
		self.create_vortex_range_max_label()
		self.create_vortex_range_max_pi_label()

	def create_vortex_set_button(self):
		self.vortex_set_button = tk.Button(master=self.frame_vortex, relief=tk.RAISED,text="Generate",command=self.make_vortex_func)
		self.vortex_set_button.grid(row=2,column=0, padx=5, pady=5)

	def get_value_from_vortex(self):
		minFrac = fractions.Fraction(check_if_entry_value_is_legal(self.range_min_entry_variable))
		maxFrac = fractions.Fraction(check_if_entry_value_is_legal(self.range_max_entry_variable))
		minVal = minFrac.numerator/minFrac.denominator
		maxval = maxFrac.numerator/maxFrac.denominator
		return (minVal,maxval)

	def make_vortex_func(self):
		self.mainController.rotationObject.vortex(self.get_value_from_vortex())
