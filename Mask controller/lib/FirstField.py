import tkinter as tk
from lib.HelperMethods import *

class FirstField():

	def __init__(self, mainController):
		self.mainController = mainController
		self.make_frame0()
		self.make_correction_coeff_field()
		self.make_correction_coeff_label()

	def make_frame0(self):
		self.frame0 = tk.Frame(master=self.mainController.mainWindow, borderwidth=1)
		self.frame0.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

	def make_correction_coeff_field(self):
		self.corr_coeff_entry_variable = tk.StringVar()
		self.corr_coeff_entry_variable.set(str(self.mainController.config.correctionFactor))
		self.corr_coeff_entry_variable.trace_add("write", self.change_corr_coeff)
		self.corr_coeff_entry = tk.Entry(master=self.frame0,width=5,textvariable=self.corr_coeff_entry_variable, validate="focusout", validatecommand=self.change_corr_coeff)
		self.corr_coeff_entry.grid(row=0,column=0, padx=5, pady=5)

	def change_corr_coeff(self,var=0, indx=1, mode=2):
		self.mainController.rotationObject.correctionFactor = get_correction_factor_from_wavelength(float(check_if_entry_value_is_legal_realtime(self.corr_coeff_entry_variable)))/255

	def make_correction_coeff_label(self):
		self.correction_coeff_label = tk.Label(master=self.frame0, text="Wavelength")
		self.correction_coeff_label.grid(row=0,column=1, padx=5, pady=5)