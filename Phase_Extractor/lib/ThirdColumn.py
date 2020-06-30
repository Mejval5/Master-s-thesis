import tkinter as tk
from lib.HelperMethods import *
from tkinter import filedialog
from PIL import Image, ImageTk

class ThirdColumn():

	def __init__(self, mainController):
		self.mainController = mainController
		self._static_images()
		self._third_column()

	def _third_column(self):
		self._third_column_frame()

		self._first_row()

	def _first_row(self):
		self.output_window = make_canvas(self.third_column_frame)
		self.output_window.configure(width=750,height=750)
		self.output_window.output_image_preview = self.blank_image
		self.output_window.create_image(0,0, image=self.output_window.output_image_preview,anchor="nw")

		self.output_window.bind('<ButtonPress-1>', self.mainController.second_column.draw_line)
		self.output_window.bind('<ButtonRelease-1>', self.mainController.second_column.draw_line)
		self.output_window.bind('<B1-Motion>', self.mainController.second_column.draw)
		self.output_window.bind('<ButtonRelease-1>', self.mainController.second_column.reset_coords)

	def _third_column_frame(self):
		self.third_column_frame = make_frame(self.mainController.mainWindow, _row=0, _column=2, _raised=tk.RAISED)
		self.third_column_frame.configure(width=750)


	def _static_images(self):
		self.blank_image = ImageTk.PhotoImage(Image.new("RGBA",(750,750)))

