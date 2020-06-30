import tkinter as tk
from tkinter import font as tkFont
from lib.HelperMethods import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import glob
import difflib
import numpy as np
import serial

class FirstColumn():

	def __init__(self, mainController):
		self.mainController = mainController
		self._init_serial()
		self.font_axis = tkFont.Font(family='Helvetica', size=36, weight='bold')
		self.right = 1
		self.left = 0
		self.x = 0
		self.y = 1
		self.z = 2
		self.text = ["X", "Y", "Z", "A"]
		self.dir = ["L", "R"]
		self._first_column()
		self.moving = False

	def _init_serial(self):
		self.serial_port = serial.Serial("COM15", 9800, timeout=1)

	def _first_column(self):
		self._first_column_frame()

		self._panels()


	def _panels(self):
		self.panels = {}
		self._first_row()
		self._second_row()
		self._third_row()

	def _first_row(self):
		self.panels[self.x] = self._make_panel(self.x)

	def _second_row(self):
		self.panels[self.y] = self._make_panel(self.y)

	def _third_row(self):
		self.panels[self.z] = self._make_panel(self.z)

	def _make_panel(self, axis):
		panel = lambda: None
		panel.controls_frame = make_frame(self.first_column_frame, _row=axis, _column=0, _columnspan=1)
		panel.controls_frame.columnconfigure(0, weight=1, minsize=75)
		panel.controls_frame.columnconfigure(1, weight=1, minsize=75)

		panel.dir_buttons_frame = make_frame(panel.controls_frame, _row=0, _column=1, _columnspan=1)
		panel.dir_buttons_frame.columnconfigure(0, weight=1, minsize=75)
		panel.dir_buttons_frame.columnconfigure(1, weight=1, minsize=75)
		panel.left_button = make_button(panel.dir_buttons_frame, _text = "<--", _row=0, _column=0, _command = lambda: None)
		panel.right_button = make_button(panel.dir_buttons_frame, _text = "-->", _row=0, _column=1, _command = lambda: None)
		panel.left_button.bind('<ButtonPress-1>', lambda k: self._move(self.left, axis, True))
		panel.left_button.bind('<ButtonRelease-1>', lambda k: self._move(self.left, axis, False))
		panel.right_button.bind('<ButtonPress-1>', lambda k: self._move(self.right, axis, True))
		panel.right_button.bind('<ButtonRelease-1>', lambda k: self._move(self.right, axis, False))

		panel.label = make_label(panel.controls_frame,  _text = self.text[axis], _row = 0, _column = 0, _rowspan = 2)
		panel.label.configure(font = self.font_axis)

		panel.scale = make_scale(panel.controls_frame, _from_=1, _to=200, _resolution = 0, _row=1, _column = 1)

		return panel


	def _first_column_frame(self):
		self.first_column_frame = make_frame(self.mainController.mainWindow, _row=0, _column=0)
		self.first_column_frame.rowconfigure(0, weight=1, minsize=10)
		self.first_column_frame.rowconfigure(1, weight=1, minsize=10)
		self.first_column_frame.rowconfigure(2, weight=1, minsize=10)
		self.first_column_frame.rowconfigure(3, weight=1, minsize=10)

	def _move(self, direction, axis, bool):
		self.curr_dir = direction
		self.curr_axis = axis
		self.moving = bool
		
	def _send_data(self, direction, axis):
		try:
			speed = self.panels[axis].scale.get()
		except:
			speed = 0
		string = "<"+self.text[axis]+", "+str(direction)+", "+str(speed)+">"
		self.serial_port.write(string.encode('ASCII'))