import tkinter as tk
from lib.HelperMethods import *
import numpy as np
from PIL import Image, ImageTk


class ManualAlign():

	def __init__(self, mainController, images, image_names, k = 0):
		self.mainController = mainController
		self.images = images
		self.image_names = image_names
		self.image_index = k
		self.open = True
		self.dragging = False
		self.dragging_index = [0, 0]
		self._create_window()

		self._image_frame()
		self._image_canvas()
		self._button_frame()
		self._buttons()
		self._image_label()
		self._setup_dots_holder()
		self._align_image()

	def _buttons(self):
		self.right_button = make_button(self.button_frame, "->", _command = lambda: self._change_image(1), _row=0, _column=1, _sticky="ew")

	def _image_label(self):
		self.current_image = make_label(self.button_frame, self.image_names[self.image_index], _row=1, _column=0, _columnspan=2)

	def _change_image(self, move_image_index):
		self._save_points()
		self.image_index = (self.image_index + move_image_index) % len(self.images)
		self.current_image.configure(text = self.image_names[self.image_index])
		self._show_image()

		if self.image_index == len(self.images) - 1:
			self.right_button.configure(text = "Finish Align", command = lambda: self._finish_align())

		self._align_image()

	def _show_image(self):
		self.image_canvas.output_image_preview = ImageTk.PhotoImage(self.images[self.image_index].resize((750,750),resample=1))
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
		self.image_canvas.bind('<Motion>', self._move_point)
		self._show_image()

	def _button_frame(self):
		self.button_frame = make_frame(self.show_images_window, _row=0, _column=0, _raised=tk.RAISED)
		self.button_frame.configure(width=150)
		self.button_frame.columnconfigure(0, weight=1)
		self.button_frame.columnconfigure(1, weight=1)

	def _paint(self, i, k):
		python_green = "#00FF00"
		x = self.oval_holder[i][k]["coordinates"][0]
		y = self.oval_holder[i][k]["coordinates"][1]
		x1, y1 = (x - 4), (y - 4)
		x2, y2 = (x + 4), (y + 4)
		self.oval_holder[i][k]["oval"] = self.image_canvas.create_oval(x1, y1, x2, y2, fill=python_green, outline="", width=0)
		self.image_canvas.tag_bind(self.oval_holder[i][k]["oval"], "<Button-1>", lambda event: self._start_drag(i, k, event))
		self.image_canvas.tag_bind(self.oval_holder[i][k]["oval"], "<ButtonRelease-1>", lambda e: self._stop_drag())

	def _stop_drag(self):
		self.dragging = False

	def _move_point(self, event):
		if self.dragging:
			x = event.x
			y = event.y
			x_last = self.last_coords[0]
			y_last = self.last_coords[1]
			i = self.dragging_index[0]
			k = self.dragging_index[1]
			self.image_canvas.move(self.oval_holder[i][k]["oval"], x - x_last, y - y_last)
			self.last_coords = [x, y]

	def _start_drag(self, i, k, event):
		self.dragging = True
		self.dragging_index = [i, k]
		self.last_coords = [event.x, event.y]

	def _setup_dots(self, i):
		self.oval_holder[i] = {} 
		for k in range(4):
			x = 300 * ((k+1) % 2)+300
			y = 300 * min(max(0, k-1),1)+300
			self.oval_holder[i][k] = {}
			self.oval_holder[i][k]["coordinates"] = [x, y]

	def _save_points(self):
		i = self.image_index
		for k in range(4):
			point_tuple = self.image_canvas.coords(self.oval_holder[i][k]["oval"])
			x = int((point_tuple[2] + point_tuple[0]) / 2)
			y = int((point_tuple[3] + point_tuple[1]) / 2)
			self.oval_holder[i][k]["coordinates"] = [x, y]

	def _setup_dots_holder(self):
		self.oval_holder = {}
		for i in range(len(self.images)):
			self._setup_dots(i)

	def _align_image(self):
		i = self.image_index
		for k in range(4):
			self._paint(i, k)

	def _finish_align(self):
		image_centers = {}
		for i in range(len(self.images)):
			x = 0
			y = 0
			for k in range(4):
				x += self.oval_holder[i][k]["coordinates"][0]
				y += self.oval_holder[i][k]["coordinates"][1] 
			image_centers[i] = [x/4, y/4]
		self.mainController.second_column._manual_align_return(image_centers)
		self.open = False
		self.show_images_window.destroy()		
		del self

		
	def on_closing(self):
		self.open = False
		self.show_images_window.destroy()