import tkinter as tk
from lib.HelperMethods import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import glob
import difflib
import numpy as np

class FirstColumn():

	def __init__(self, mainController):
		self.mainController = mainController
		self._static_images()
		self._first_column()

	def _first_column(self):
		self._first_column_frame()

		self._first_row()
		self._second_row()


	def _first_row(self):
		self._measure_labels()

	def _second_row(self):
		self.image_loading_frame = make_frame(self.first_column_frame, _row=1, _column=0, _columnspan=2)
		self.image_loading_frame.columnconfigure(0, weight=1, minsize=75)
		self.image_loading_frame.columnconfigure(1, weight=1, minsize=75)
		self.image_loader=[]
		for k in range(10):
			self.image_loader.append(self._image_loader(k))

	def _first_column_frame(self):
		self.first_column_frame = make_frame(self.mainController.mainWindow, _row=0, _column=0, _raised=tk.RAISED)
		self.first_column_frame.columnconfigure(0, weight=1, minsize=75)
		self.first_column_frame.columnconfigure(1, weight=1, minsize=75)

	def _load_folder_button(self):
		self.load_folder_button = make_button(self.first_column_frame, "Load Folder", self._load_folder, _row=2, _column=0, _columnspan=2)

	def _measure_labels(self):
		self.measure_labels = make_label(self.first_column_frame, "AFM", _row=0, _column=0)
		self.measure_labels = make_label(self.first_column_frame, "SNOM", _row=0, _column=1)

	def _image_loader(self,k):
		i, j = convert_index_1D(k)
		frame = self._image_loader_frame(i,j)
		frame = self._image_loader_module(frame,i,j)
		return frame

	def _image_loader_module(self, frame, i, j):
		frame.image_preview = make_label(frame, _row=0, _column=0, _raised = tk.RAISED, _rowspan=3)
		frame.preview_image = self.blank_image
		frame.image_preview.configure(image = frame.preview_image)
		frame.name_label = make_label(frame, "", _row=0, _column=1)
		frame.button = make_button(frame, "Load Image", _command = lambda: self._load_image_dialog(i,j), _row=1, _column=1)
		self._toggle_visibility_of_cross_button(frame, False)
		return frame

	def _image_loader_frame(self, i, j):
		frame = make_frame(self.image_loading_frame, _row=i, _column=j)
		return frame

	def _initial_dir(self, reset=False):
		if reset or not hasattr(self, "last_folder"):
			self.last_folder = "_data_folder"
		return self.last_folder

	def _load_image_dialog(self,i,j):
		k = convert_index_2D(i,j)
		try:
			self.path = filedialog.askopenfilename(initialdir = self._initial_dir(), title="Select measure data", filetypes = [("DATA files","*.png *.txt")])
			self.last_folder = self.path.replace(os.path.basename(self.path),"")

			self._load_image(k, self.path)
		except:
			pass

	def _load_image(self, k, path):
		self.path = path
		try:
			if self.path[-3:]=="png":
				image = Image.open(self.path)
			elif self.path[-3:]=="txt":
				image = self._load_txt_data_as_image(self.path)
		except:
			pass
		self.image_loader[k].image = image
		self.image_loader[k].preview_image = ImageTk.PhotoImage(image.resize((100,100),resample=1))
		self.image_loader[k].image_preview.configure(image = self.image_loader[k].preview_image)
		self.image_loader[k].image_preview.bind("<Button-1>", lambda e: self._show_image(k))
		self.image_loader[k].name_label.configure(text=os.path.basename(path))
		self._toggle_visibility_of_cross_button(self.image_loader[k], True, k)


	def _unload_image(self,i,j):
		k = convert_index_2D(i,j)
		self.image_loader[k].image = None
		self.image_loader[k].preview_image = self.blank_image
		self.image_loader[k].image_preview.configure(image = self.image_loader[k].preview_image)
		self.image_loader[k].image_preview.unbind("<Button-1>")
		self._toggle_visibility_of_cross_button(self.image_loader[k], False)


	def _static_images(self):
		self.blank_image = ImageTk.PhotoImage(Image.new("RGBA",(100,100)))
		self.cross_image = ImageTk.PhotoImage(Image.open("lib/img/cross.png").resize((20,20)))


	def _toggle_visibility_of_cross_button(self, frame, set_bool, k=0):
		if set_bool:
			if hasattr(frame,"remove_image_button"):
				frame.remove_image_button.destroy()
			i, j = convert_index_1D(k)
			frame.remove_image_button = make_button(frame, "", _command = lambda: self._unload_image(i, j), _row=2, _column=1, _sticky="w")
			frame.remove_image_button.configure(image = self.cross_image)
		else:
			if hasattr(frame,"remove_image_button"):
				frame.remove_image_button.destroy()
			frame.remove_image_button = make_label(frame, "", _row=2, _column=1)
			frame.name_label.configure(text="")

	def _load_txt_data_as_image(self,filename):
		
		image_array_holder = []

		with open(filename, 'r') as f:
			for line in f.readlines():
				image_array_holder.append(line.replace('\n', '').split('\t'))
		image_numpy = np.float32(np.array(image_array_holder))
		a_min = np.amin(image_numpy)
		image_numpy = image_numpy-a_min
		a_max = np.amax(image_numpy)
		image_numpy = image_numpy/a_max
		image_numpy = image_numpy*255
		image_final = Image.fromarray(image_numpy)
		return image_final

	def _show_image(self, k):
		self.mainController.second_column._open_aligned_images(k)