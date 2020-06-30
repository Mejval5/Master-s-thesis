

import tkinter as tk

from lib.HelperMethods import *

class ChangeCenter():

	def __init__(self,mainController):
		self.mainController = mainController
		self.make_change_center()

	def make_change_center(self):
		self.make_change_center_frame()
		self.make_change_center_label()
		self.make_change_center_frame_xy()
		self.make_change_center_x()
		self.make_change_center_y()
		self.make_change_center_x_label()
		self.make_change_center_y_label()
		self.make_change_center_checkbox_frame()
		self.make_change_center_checkbox()
		self.make_change_center_centrize_button()

	def make_change_center_frame(self):
		self.frame_change_center = tk.Frame(master=self.mainController.frame01Object.frame01, borderwidth=1, relief=tk.RAISED)
		self.frame_change_center.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

	def make_change_center_label(self):
		self.change_center_label = tk.Label(master=self.frame_change_center, text="Center of beam")
		self.change_center_label.grid(row=0,column=0, padx=5, pady=5, columnspan=2)

	def make_change_center_frame_xy(self):
		self.change_center_frame = tk.Frame(master=self.frame_change_center)
		self.change_center_frame.grid(row=1,column=0, padx=5, pady=5)

	def make_change_center_x(self):
		self.change_center_x_variable = tk.StringVar()
		self.change_center_x_variable.set(self.mainController.config.centerX)
		self.change_center_x_variable.trace_add("write", self.change_center_x)
		self.change_center_x_entry = tk.Entry(master=self.change_center_frame,width=5,textvariable=self.change_center_x_variable,justify='left')
		self.change_center_x_entry.grid(row=0,column=1, padx=5, pady=5)

	def make_change_center_y(self):
		self.change_center_y_variable = tk.StringVar()
		self.change_center_y_variable.set(self.mainController.config.centerY)
		self.change_center_y_variable.trace_add("write", self.change_center_y)
		self.change_center_y_entry = tk.Entry(master=self.change_center_frame,width=5,textvariable=self.change_center_y_variable,justify='left')
		self.change_center_y_entry.grid(row=1,column=1, padx=5, pady=5)

	def make_change_center_x_label(self):
		self.change_center_x_label= tk.Label(master=self.change_center_frame,width=5,text="x =")
		self.change_center_x_label.grid(row=0,column=0, padx=5, pady=5)

	def make_change_center_y_label(self):
		self.change_center_y_label = tk.Label(master=self.change_center_frame,width=5,text="y =")
		self.change_center_y_label.grid(row=1,column=0, padx=5, pady=5)

	def make_change_center_checkbox_frame(self):
		self.change_center_checkbox_frame = tk.Frame(master=self.frame_change_center)
		self.change_center_checkbox_frame.grid(row=1,column=1, padx=5, pady=5)

	def make_change_center_checkbox(self):
		self.change_center_checkbox_variable=tk.IntVar()
		self.change_center_checkbox_variable.set(self.mainController.config.startChangeCenter)
		self.change_center_checkbox = tk.Checkbutton(master=self.change_center_checkbox_frame, text="use mouse",variable=self.change_center_checkbox_variable)
		self.change_center_checkbox.grid(row=0,column=0, padx=5, pady=5)

	def make_change_center_centrize_button(self):
		self.change_center_centrize_checkbox = tk.Button(master=self.change_center_checkbox_frame, text="Center", command=lambda: self.center_image())
		self.change_center_centrize_checkbox.grid(row=1,column=0, padx=5, pady=5)

	def get_mouse_position(self,event):
		x, y = event.x, event.y
		if self.change_center_checkbox_variable.get()==1:
			self.set_center_mouse(x,y)

	def set_center_mouse(self,x,y):
		self.mainController.config.centerX=float('%.3f'%(float(x)/float(self.mainController.config.previewX)))
		self.mainController.config.centerY=float('%.3f'%(1-float(y)/float(self.mainController.config.previewY)))
		self.set_center()

	def change_center_x(self,var=0, indx=1, mode=2):
		self.mainController.config.centerX = float(check_if_entry_value_is_legal_realtime(self.change_center_x_variable))
		self.set_center()

	def change_center_y(self,var=0, indx=1, mode=2):
		self.mainController.config.centerY = float(check_if_entry_value_is_legal_realtime(self.change_center_y_variable))
		self.set_center()

	def center_image(self):
		self.mainController.config.centerX=0.5
		self.mainController.config.centerY=0.5
		self.set_center()

	def set_center(self,var=0, indx=1, mode=2):
		self.change_center_x_variable.set(str(self.mainController.config.centerX))
		self.change_center_y_variable.set(str(self.mainController.config.centerY))
		self.mainController.rotationObject.set_center(self.mainController.config.centerX,self.mainController.config.centerY)
