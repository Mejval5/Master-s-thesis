
import tkinter as tk

from lib.HelperMethods import *


class MakeSquare():

	def __init__(self, mainController):
		self.mainController = mainController
		self.make_square()

	def make_square(self):
		self.create_square_frame()
		self.create_square_label()
		self.create_square_sections_holder_frame()
		self.create_square_section_frame()
		self.create_square_section_entry()
		self.create_square_section_pi_labels()
		self.create_square_set_button()

	def create_square_frame(self):
		self.frame_square = tk.Frame(master=self.mainController.frame01Object.frame01, borderwidth=1, relief=tk.RAISED)
		self.frame_square.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

	def create_square_label(self):
		self.square_label = tk.Label(master=self.frame_square, text="Square")
		self.square_label.grid(row=0,column=0, padx=5, pady=5)

	def create_square_sections_holder_frame(self):
		self.square_sections_holder_frame = tk.Frame(master=self.frame_square, borderwidth=1)
		self.square_sections_holder_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

	def create_square_section_frame(self):
		index = 0
		self.square_section_frame=[]
		for i in range(2):
			for j in range(2):
				self.square_section_frame.append(tk.Frame(master=self.square_sections_holder_frame))
				self.square_section_frame[index].grid(row=j,column=i, padx=5, pady=5)
				index+=1

	def create_square_section_entry(self):
		index = 0
		stringTuple=("0.0","1.0","1.0","0.0")
		self.square_section_entry=[]
		self.square_section_variable=[]
		for i in range(2):
			for j in range(2):
				self.square_section_variable.append(tk.StringVar())
				self.square_section_variable[index].set(stringTuple[index])
				self.square_section_entry.append(tk.Entry(master=self.square_section_frame[index],width=10,textvariable=self.square_section_variable[index],justify='right'))
				self.square_section_entry[index].grid(row=0,column=0, padx=5, pady=5)
				index+=1

	def get_square_section_entry(self):
		index = 0
		self.get_square_section=[]
		for i in range(2):
			for j in range(2):
				value = self.get_value_from_square(index)
				self.get_square_section.append(value)
				index+=1
		return self.get_square_section		


	def get_value_from_square(self,index):
		return check_if_entry_value_is_legal(self.square_section_variable[index])

	def get_square_values(self):
		returnValues = []
		index = 0
		for value in self.get_square_section_entry():
			fract = fractions.Fraction(value)
			returnValues.append(fract.numerator/fract.denominator)
		return returnValues

	def create_square_section_pi_labels(self):
		index = 0
		self.range_max_label=[]
		for i in range(2):
			for j in range(2):
				self.range_max_label.append(tk.Label(master=self.square_section_frame[index], text="\u03C0"))
				self.range_max_label[index].grid(row=0,column=1, padx=0, pady=5)
				index+=1
 
	def create_square_set_button(self):
		self.square_set_button = tk.Button(master=self.frame_square, relief=tk.RAISED,text="Generate",command=lambda: self.mainController.rotationObject.square(self.get_square_values()))
		self.square_set_button.grid(row=2,column=0, padx=5, pady=5)
