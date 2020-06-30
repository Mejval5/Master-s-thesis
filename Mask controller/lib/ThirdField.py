
import tkinter as tk
from datetime import datetime

from lib.HelperMethods import *

class ThirdField():

	def __init__(self,mainController):
		self.mainController = mainController
		self.make_third_field()

	def make_third_field(self):
		self.make_frame_3()
		self.make_rotate_field()
		self.make_rotate_field_label()
		self.make_rotate_time_field()
		self.make_rotate_time_field_label()
		self.make_window_select()
		self.make_window_select_label()
		self.make_window_display_checkbox()

	def make_frame_3(self):
		self.frame03 = tk.Frame(master=self.mainController.mainWindow, borderwidth=1)
		self.frame03.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

	def make_rotate_field(self):
		self.rotateFieldVariable = tk.StringVar()
		self.rotateFieldVariable.set("0")
		self.rotateFieldVariable.trace_add("write", self.rotate_field_change)
		self.rotateFieldEntry = tk.Entry(master=self.frame03,width=5,textvariable=self.rotateFieldVariable, validate="focusout", validatecommand=self.rotate_field_change)
		self.rotateFieldEntry.grid(row=0,column=0, padx=5, pady=5)

	def make_rotate_field_label(self):
		self.rotateFieldLabel = tk.Label(master=self.frame03, text="Rotation (deg)")
		self.rotateFieldLabel.grid(row=0,column=1, padx=5, pady=5)

	def rotate_field_change(self,var=0, indx=1, mode=2):
		 self.mainController.config.angle = float(check_if_entry_value_is_legal_realtime(self.rotateFieldVariable))

	def make_rotate_time_field(self):
		self.rotateTimeFieldVariable = tk.StringVar()
		self.rotateTimeFieldVariable.set("0")
		self.rotateTimeFieldVariable.trace_add("write", self.rotate_time_field_change)
		self.rotateTimeFieldEntry = tk.Entry(master=self.frame03,width=5,textvariable=self.rotateTimeFieldVariable, 
			validate="focusout", validatecommand=self.rotate_time_field_change)
		self.rotateTimeFieldEntry.grid(row=0,column=2, padx=5, pady=5)

	def make_window_select(self):
		self.windowSelectVariable = tk.StringVar()
		self.windowSelectVariable.set(self.mainController.display.monitorHolder[self.mainController.config.monitor])
		self.windowSelectVariable.trace_add("write", self.change_window)
		self.windowSelectMenu = tk.OptionMenu(self.frame03, self.windowSelectVariable,*self.mainController.display.monitorHolder)
		self.windowSelectMenu.config(width=20,anchor="w")
		self.windowSelectMenu.grid(row=0,column=4, padx=5, pady=5)

	def change_window(self,var=0, indx=1, mode=2):
		self.mainController.config.monitor = self.mainController.display.monitorHolder.index(self.windowSelectVariable.get())
		self.mainController.display.setup_display_window()

	def make_window_select_label(self):
		self.windowSelectLabel = tk.Label(master=self.frame03, text="Window")
		self.windowSelectLabel.grid(row=0,column=5, padx=5, pady=5)

	def make_window_display_checkbox(self):
		self.windowDisplayCheckboxVariable=tk.IntVar()
		self.windowDisplayCheckboxVariable.set(self.mainController.config.startDisplay)
		self.windowDisplayCheckboxVariable.trace_add("write", self.toggle_window)
		self.windowDisplayCheckbox = tk.Checkbutton(master=self.frame03, text="output enabled",variable=self.windowDisplayCheckboxVariable)
		self.windowDisplayCheckbox.configure(wraplength=50)
		self.windowDisplayCheckbox.grid(row=0,column=6, padx=5, pady=5)

	def toggle_window(self,var=0, indx=1, mode=2):
		self.change_window()

	def make_rotate_time_field_label(self):
		self.rotateTimeFieldLabel = tk.Label(master=self.frame03, text="Rotation speed (deg/s)")
		self.rotateTimeFieldLabel.grid(row=0,column=3, padx=5, pady=5)

	def rotate_time_field_change(self,var=0, indx=1, mode=2):
		self.mainController.config.timeStamp = datetime.now().timestamp()
		self.mainController.config.angleTime = float(check_if_entry_value_is_legal_realtime(self.rotateTimeFieldVariable))