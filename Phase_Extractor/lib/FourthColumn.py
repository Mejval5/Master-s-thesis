import tkinter as tk
from lib.HelperMethods import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np

class FourthColumn():

	def __init__(self, mainController):
		self.mainController = mainController
		self._static_images()
		self._third_column()

	def _third_column(self):
		self._third_column_frame()

		self._first_row()

	def _first_row(self):
		self.output_window = make_canvas(self.third_column_frame)
		self.output_window.configure(width=50,height=750)
		self.output_window.output_image_preview = self.blank_image
		self.output_window.create_image(0,0, image=self.output_window.output_image_preview,anchor="nw")

	def _third_column_frame(self):
		self.third_column_frame = make_frame(self.mainController.mainWindow, _row=0, _column=3, _raised=tk.RAISED)
		self.third_column_frame.configure(width=750)


	def _static_images(self):
		array = np.zeros((750, 50, 4), dtype=np.uint8)
		for k in range(750):
			for i in range(50):
				if i < 25:
					array[k,i] = [255* (1 - k / 750), 255* (1 - k / 750), 255* (1 - k / 750), 255]
				else:
					array[k,i] = [255,255,255,255]
				if k < 2 and i < 25:
					array[k,i] = [0,0,0,255]
				if k > 746 and i < 25:
					array[k,i] = [0,0,0,255]
				if i < 2 or (25 > i > 22):
					array[k,i] = [0,0,0,255]
				if 377 > k > 373 and 10 < i < 25:
					array[k,i] = [0,0,0,255]
		# array = np.int8(array)
		array = np.array(array)
		image = Image.fromarray(array)
		draw = ImageDraw.Draw(image)
		text = u"2π"
		font = ImageFont.truetype("lib/DejaVuSans.ttf", 18)
		draw.text((27, 1),text,font=font,fill=(0,0,0))
		text = u"π"
		draw.text((33, 365),text,font=font,fill=(0,0,0))
		text = u"0"
		draw.text((33, 730),text,font=font,fill=(0,0,0))
		self.side_bar = image
		self.blank_image = ImageTk.PhotoImage(image,"RGB")