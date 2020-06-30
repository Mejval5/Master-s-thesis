import tkinter as tk
from lib.HelperMethods import *
import numpy as np
from PIL import Image, ImageTk


class ImageViewer():

	def __init__(self, mainController, images, image_names, k = 0):
		self.mainController = mainController
		self.images = images
		self.open = True
		self.image_names = image_names
		self.image_index = k
		self._create_window()

		self._image_frame()
		self._image_canvas()
		self._button_frame()
		self._buttons()
		self._image_label()

	def _buttons(self):
		self.left_button = make_button(self.button_frame, "<-", _command = lambda: self._change_image(-1), _row=0, _column=0, _sticky="ew")
		self.right_button = make_button(self.button_frame, "->", _command = lambda: self._change_image(1), _row=0, _column=1, _sticky="ew")

	def _image_label(self):
		self.current_image = make_label(self.button_frame, self.image_names[self.image_index], _row=1, _column=0, _columnspan=2)

	def _change_image(self, move_image_index):
		self.image_index = (self.image_index + move_image_index) % len(self.images)
		self.current_image.configure(text = self.image_names[self.image_index])
		self._show_image()


	def _show_image(self):
		self.image_canvas.output_image_preview = ImageTk.PhotoImage(self.images[self.image_index].resize((750,750),resample=2))
		self.image_canvas.create_image(0,0, image=self.image_canvas.output_image_preview,anchor="nw")

	def _create_window(self):
		self.show_images_window = tk.Toplevel(self.mainController.mainWindow)
		self.show_images_window.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.show_images_window.columnconfigure(0, weight=1, minsize=200)
		self.show_images_window.columnconfigure(1, weight=1, minsize=750)

	def _image_frame(self):
		self.image_frame = make_frame(self.show_images_window, _row=0, _column=1, _raised=tk.RAISED)
		self.image_frame.configure(height = 750, width=750)

	def _image_canvas(self):
		self.image_canvas = make_canvas(self.image_frame)
		self.image_canvas.configure(width=750,height=750)
		self._show_image()

	def _button_frame(self):
		self.button_frame = make_frame(self.show_images_window, _row=0, _column=0, _raised=tk.RAISED)
		self.button_frame.configure(width=150)
		self.button_frame.columnconfigure(0, weight=1)
		self.button_frame.columnconfigure(1, weight=1)

	def on_closing(self):
		self.open = False
		self.show_images_window.destroy()