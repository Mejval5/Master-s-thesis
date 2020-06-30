import tkinter as tk
from lib.HelperMethods import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import glob
import difflib
import numpy as np
import serial
import time

class SecondColumn():

	def __init__(self, mainController):
		self.mainController = mainController
		self.light_bool = False
		self.shutter_bool = True
		self._init_serial_light_only()
		self.right = 1
		self.left = 0
		self.x = 0
		self.y = 1
		self.z = 2
		self.text = ["X", "Y", "Z", "A"]
		self.dir = ["L", "R"]
		self._first_column()
		self.moving = False
		self._first_column()
		self.time_stamp = time.time()
		self._toggle_shutter()


	def _init_serial_light_only(self):
		self.serial_light_only = serial.Serial("COM16", 9800, timeout=1)


	def _first_column(self):

		self._first_row()
		self._second_row()


	def _first_row(self):
		self.light_frame = make_frame(self.mainController.mainWindow, _row=0, _column=1, _raised=tk.RAISED, _sticky="")
		self.light_frame.columnconfigure(0, weight=1, minsize=5)
		self.light_label = make_label(self.light_frame, _text = "Light control")
		self.light_toggle = make_button(self.light_frame, _text = "Toggle light", _row = 0, _command = lambda: self._toggle_light())
		self.light_var = tk.IntVar()
		self.light_var.set(self.light_bool)
		self.checkbox = tk.Checkbutton(master=self.light_frame,variable=self.light_var, state=tk.DISABLED)
		self.checkbox.grid(row=1,column=0, padx=0, pady=0, columnspan=1, rowspan=1)

	def _second_row(self):
		self.shutter_frame = make_frame(self.light_frame, _row=2, _column=0)
		self.shutter_frame.columnconfigure(0, weight=1, minsize=5)
		self.shutter_label = make_label(self.shutter_frame, _text = "Shutter control")
		self.shutter_toggle = make_button(self.shutter_frame, _text = "Toggle shutter", _row = 0, _command = lambda: self._toggle_shutter(), _sticky="n")
		self.shutter_var = tk.IntVar()
		self.shutter_var.set(self.shutter_bool)
		self.shutter_checkbox = tk.Checkbutton(master=self.shutter_frame,variable=self.shutter_var, state=tk.DISABLED)
		self.shutter_checkbox.grid(row=1,column=0, padx=0, pady=0, columnspan=1, rowspan=1)

	def _toggle_light(self):
		self.light_bool = not self.light_bool
		self.light_var.set(self.light_bool)
		var = self.light_bool * 1
		self._send_data_light_only(var, 3)

	def _toggle_shutter(self):
		self.shutter_toggle.configure(state="disabled")
		self.time_stamp = time.time()
		self.shutter_bool = not self.shutter_bool
		self.shutter_var.set(self.shutter_bool)
		var = self.shutter_bool * 1
		self.mainController.first_column._send_data(var, 3)

	def _send_data_light_only(self, direction, axis):
		speed = 0
		string = "<"+self.text[axis]+", "+str(direction)+", "+str(speed)+">"
		self.serial_light_only.write(string.encode('ASCII'))