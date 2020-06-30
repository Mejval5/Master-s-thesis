import tkinter as tk
from lib.HelperMethods import *
from lib.ImageViewer import ImageViewer
from lib.ManualAlign import ManualAlign
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import os
import math
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import scipy.signal

class SecondColumn():

	def __init__(self, mainController):
		self.mainController = mainController
		self._second_column()

	def _second_column(self):
		self._second_column_frame()

		self._first_row()
		self._second_row()
		self._third_row()
		self._fourth_row()
		self._fifth_row()
		self._sixth_row()
		self._seventh_row()

	def _second_column_frame(self):
		self.second_column_frame = make_frame(self.mainController.mainWindow, _row=0, _column=1, _raised=tk.RAISED)
		self.second_column_frame.columnconfigure(0, weight=1, minsize=75)


	def _first_row(self):
		self.first_row_frame = make_frame(self.second_column_frame, _row=0, _column=0, _pady=10)
		self.first_row_frame.columnconfigure(0, weight=1, minsize=75)
		self.first_row_button = make_button(self.first_row_frame, "Align", _command = lambda: self._align(), _row=0, _column=0, _pady = 0)
		# self.auto_align_checkbox = make_checkbox(self.first_row_frame, _text = "Auto align", _row=1, _column=0, _pady = 0)
		# self.auto_align_checkbox.var.trace_add("write", self._auto_align_toggle)
		# self.points_textfield = make_textfield(self.first_row_frame, _text = "Points", _row=2, _column=0, _pady = 0, _value="2")
		# self.points_textfield.textfield.config(state=tk.DISABLED)

	def _second_row(self):
		self.second_row_button = make_button(self.second_column_frame, "Open aligned images", _command = lambda: self._open_aligned_images(), _row=1, _column=0)

	def _third_row(self):
		self.third_row_button = make_button(self.second_column_frame, "Calculate phase", _command = lambda: self._x_step_algorithm(), _row=2, _column=0)
		self.steps_textfield = make_textfield(self.second_column_frame, _text = "Steps", _row=3, _column=0, _pady = 0, _value="4")
		self.auto_save_checkbox = make_checkbox(self.second_column_frame, _text = "Auto save", _row=4, _column=0, _pady = 0)

	def _fourth_row(self):
		self.fourth_row_button = make_button(self.second_column_frame, "Save output image", _command = lambda: self._save_output_image(), _row=5, _column=0)
		self.save_with_line_checkbox = make_checkbox(self.second_column_frame, "Save with line", _row=6, _column=0)

	def _fifth_row(self):
		self.fifth_row_button = make_button(self.second_column_frame, "Load output image", _command = lambda: self._load_output_image(), _row=7, _column=0)

	def _sixth_row(self):
		self.sixth_row_button = make_button(self.second_column_frame, "Get line plot", _command = lambda: self._get_line_plot(), _row=8, _column=0)
		self.draw_line_checkbox = make_checkbox(self.second_column_frame, _text = "Draw line", _row=9, _column=0, _pady = 0, _value=False, _command = lambda: self._remove_current_line())
		self.line_width_textfield = make_textfield(self.second_column_frame, _text = "Line width", _row=10, _column=0, _pady = 0, _value="5")
		self.line_width_textfield.var.trace_add("write", self._change_line_width)

	def _seventh_row(self):
		self.seventh_row_button = make_button(self.second_column_frame, "Load folder", _command = lambda: self._load_folder(), _row=11, _column=0)
		self.load_folder_textfield = make_textfield(self.second_column_frame, _text = "name", _row=12, _column=0, _pady = 0, _value="TOP ? x pi pul nahore_0.txt", _width=15)

	def _auto_align_toggle(self,var=0, indx=1, mode=2):
		if self.auto_align_checkbox.var.get() == 1:
			self.points_textfield.textfield.config(state=tk.DISABLED)
		else:
			self.points_textfield.textfield.config(state=tk.NORMAL)



	def _change_line_width(self,var=0, indx=1, mode=2):
		if hasattr(self,"line_scan"):
			event = lambda:None
			event.type="update_width"
			self.draw_line(event)

	def _get_line_width(self):
		width = 1
		try:
			width = max(int(self.line_width_textfield.var.get()),1)
		except:
			pass
		return width


	def _x_step_algorithm(self):
		steps = int(self.steps_textfield.var.get())
		are_images_loaded, number_of_images, loaded_bool_array = self._check_snom_images_are_loaded()
		if are_images_loaded and number_of_images >= steps:
			are_images_same_dim = self._check_snom_images_are_same_dimension(steps)
			if are_images_same_dim:
				image_holder = {}
				for i in range(steps):
					image_holder[i] = np.asarray(self.mainController.first_column.image_loader[i+5].image.convert('L'),dtype="float")
				if steps == 4:
					phase_image = self._calculate_phase_4_step(image_holder)
				if steps == 5:
					phase_image = self._calculate_phase_5_step(image_holder)
				self.phase_image_255 = np.uint8(phase_image/2/np.pi*255)
				self.output_image = Image.fromarray(self.phase_image_255,"L")
				self.mainController.third_column.output_window.output_image_preview = ImageTk.PhotoImage(self.output_image.resize((750,750)))
				self.mainController.third_column.output_window.create_image(0,0, image=self.mainController.third_column.output_window.output_image_preview,anchor="nw")
				self._remove_current_line()
				self.mainController.first_column._initial_dir(reset = True)
				if self.auto_save_checkbox.var.get()==1:
					self._auto_save()

	def _check_snom_images_are_loaded(self):
		are_loaded = False
		number = 0
		image_exist_bool = np.array([0, 0, 0, 0, 0])
		for i in range(5):
			bool = 0
			exists_attr = hasattr(self.mainController.first_column.image_loader[i+5],"image")
			if exists_attr:
				bool = self.mainController.first_column.image_loader[i+5].image != None
			image_exist_bool[i] = bool
		if np.array_equal(image_exist_bool, np.array([1,1,1,1,0])) or np.array_equal(image_exist_bool, np.array([1,1,1,1,1])):
			are_loaded = True
			number = np.sum(image_exist_bool)
		return are_loaded, number, image_exist_bool

	def _check_snom_images_are_same_dimension(self, steps):
		first_image_dim = self.mainController.first_column.image_loader[5].image.size
		for i in range(1,steps):
			if first_image_dim == self.mainController.first_column.image_loader[i+5].image.size:
				continue
			else:
				return False
		return True

	def _calculate_phase_4_step(self,input_images):
		return np.arctan2(input_images[3]-input_images[1],input_images[0]-input_images[2])

	def _calculate_phase_5_step(self,input_images):
		# return np.arccos(1/2*(input_images[4]-input_images[0])/(input_images[3]-input_images[1]))
		return np.arctan2(2*input_images[1]-2*input_images[3],2*input_images[2]-input_images[0]-input_images[4])


	def _auto_save(self):
			path = self.mainController.first_column.path
			self.path_output_folder = path.replace(os.path.basename(path),"")
			self._add_side_bar_and_save(self.output_image, self.path_output_folder+"_output_phase.png")

	def _save_output_image(self):
		if hasattr(self,"output_image"):
			try:
				if not_none(self.mainController.first_column, "path"):
					path = self.mainController.first_column.path
				elif not_none(self,"path"):
					path = self.path
				self.path_output_folder = path.replace(os.path.basename(path),"")
				self.path_to_save = filedialog.asksaveasfilename(filetypes=[("Image file", ".png")], initialdir=self.path_output_folder, initialfile="_output_phase",defaultextension='.png')
				if not_none(self,"line_scan") and self.save_with_line_checkbox.var.get() == 1:
					self._save_output_image_with_line(self.path_to_save)
				else:
					self._add_side_bar_and_save(self.output_image, self.path_to_save)
			except:
				pass

	def _add_side_bar_and_save(self, image, path):
		h = image.height
		scale = h / 750
		side_bar = self.mainController.fourth_column.side_bar.resize((int(scale*50), int(scale*750)),resample=2)
		output = concatenate_images_h(image, side_bar)
		output.save(path)


	def _save_output_image_with_line(self, path_to_save):
		self.output_image_with_line = Image.fromarray(self.phase_image_255).convert("RGB")
		draw = ImageDraw.Draw(self.output_image_with_line)
		if self.draw_line_checkbox.var.get() == 1:
			if not_none(self,"line_scan"):
				output_size = self.output_image.size
				width = int(self._get_line_width()/750*min(output_size[0],output_size[1]))
				for k in range(width):
					offset = self._get_offset(k)
					slope = (self.y/750*output_size[1]-self.y_old/750*output_size[1])/(self.x/750*output_size[0]-self.x_old/750*output_size[0])
					if abs(self.x - self.x_old) > abs(self.y - self.y_old):
						x_0 = slope * offset / (1 + slope**2)
						x = np.linspace(self.x_old/750*output_size[0]+x_0, self.x/750*output_size[0]+x_0, 1000)
						y = np.int32(self.y_old/750*output_size[1]+slope*(x-self.x_old/750*output_size[0])-offset)
						x = np.int32(x)
					else:
						y_0 = - slope * offset / (1 + slope**2)
						y = np.linspace(self.y_old/750*output_size[1]+y_0, self.y/750*output_size[1]+y_0, 1000)
						x = np.int32(self.x_old/750*output_size[0]+1/slope*(y-self.y_old/750*output_size[1])+offset)
						y = np.int32(y)
					for i in range(len(x)):
						a = y[i]
						b = x[i]
						draw.point((b, a),(0, 255, 0))
				self._add_side_bar_and_save(self.output_image_with_line, path_to_save)

	def draw_line(self, event):
		if self.draw_line_checkbox.var.get() == 1 and hasattr(self, "output_image"):
			if str(event.type) == 'ButtonPress':
				self.mainController.third_column.output_window.old_coords = event.x, event.y
			elif str(event.type) == "update_width":
				self._remove_current_line()
				self.line_scan = self.mainController.third_column.output_window.create_line(self.x, self.y, self.x_old, self.y_old, fill="#00FF00", width=self._get_line_width())
		else:
			if hasattr(self, "line_scan"):
					self.mainController.third_column.output_window.delete(self.line_scan)
			self.reset_coords()

	def draw(self, event):
		if self.draw_line_checkbox.var.get() == 1 and hasattr(self, "output_image"):
			self.x = max(0, min(event.x, 749))
			self.y = max(0, min(event.y, 749))
			if self.mainController.third_column.output_window.old_coords:
				self._remove_current_line()
				self.x_old, self.y_old = self.mainController.third_column.output_window.old_coords
				self.line_scan = self.mainController.third_column.output_window.create_line(self.x, self.y, self.x_old, self.y_old, fill="#00FF00", width=self._get_line_width())
		else:
			self._remove_current_line()
			self.reset_coords("event")

	def reset_coords(self,event="event"):
		self.mainController.third_column.output_window.old_coords = None

	def _remove_current_line(self):
		if hasattr(self, "line_scan"):
			self.mainController.third_column.output_window.delete(self.line_scan)
			self.line_scan = None

	def _get_line_plot(self):
		if self.draw_line_checkbox.var.get() == 1:
			if not_none(self,"line_scan"):
				output_size = self.output_image.size
				line_plot = {}
				width = int(self._get_line_width()/750*min(output_size[0],output_size[1]))
				for k in range(width):
					offset = self._get_offset(k)
					slope = (self.y/750*output_size[1]-self.y_old/750*output_size[1])/(self.x/750*output_size[0]-self.x_old/750*output_size[0])
					if abs(self.x - self.x_old) > abs(self.y - self.y_old):
						x_0 = slope * offset / (1 + slope**2)
						x = np.linspace(self.x_old/750*output_size[0]+x_0, self.x/750*output_size[0]+x_0, 1000)
						y = np.int32(self.y_old/750*output_size[1]+slope*(x-self.x_old/750*output_size[0])-offset)
						x = np.int32(x)
						var = x
					else:
						y_0 = - slope * offset / (1 + slope**2)
						y = np.linspace(self.y_old/750*output_size[1]+y_0, self.y/750*output_size[1]+y_0, 1000)
						x = np.int32(self.x_old/750*output_size[0]+1/slope*(y-self.y_old/750*output_size[1])+offset)
						y = np.int32(y)
						var = y
					var = var - np.amin(var)
					line_plot[k] = self.phase_image_255[y,x]/255*np.pi*2
					if k == 0:
						line_plot_sum = line_plot[k]
					else:	
						line_plot_sum += line_plot[k]
				line_plot_sum /= width
				self._show_plot(var, line_plot_sum)

	# returns values to scan surrounding aread of a line [...-3 -2 -1 0 1 2 3...] from the center (0,1,-1,2,-2,3,-3,...)
	def _get_offset(self, k):
		return math.ceil(k/2)*(-1)**((k%2)+1)

	def _show_plot(self, x, line_plot):
		
		self.mainController.line_plot_window = tk.Toplevel(self.mainController.mainWindow)
		self.mainController.line_plot_window.wm_title("Embedding in Tk")

		fig = Figure(figsize=(5, 4), dpi=100)
		fig.add_subplot(111).plot(x, line_plot)
		self.line_plot_data = np.asarray([x, line_plot])

		canvas = FigureCanvasTkAgg(fig, master=self.mainController.line_plot_window)  # A tk.DrawingArea.
		canvas.draw()

		toolbar = NavigationToolbar2Tk(canvas, self.mainController.line_plot_window)
		toolbar.update()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
		button = tk.Button(self.mainController.line_plot_window, text = "Save data as txt", command = lambda: self._save_lineplot())
		button.pack(side=tk.LEFT)
		canvas.mpl_connect("key_press_event", self._on_key_press)

	def _save_lineplot(self):
		try:
			if not_none(self.mainController.first_column, "path"):
				path = self.mainController.first_column.path
			elif not_none(self,"path"):
				path = self.path
			self.path_output_folder = path.replace(os.path.basename(path),"")
			self.path_to_save = filedialog.asksaveasfilename(filetypes=[("Line data", ".txt")], initialdir=self.path_output_folder, initialfile="_line_plot",defaultextension='.txt')
			self._save_lineplot_data()
		except:
			pass

	def _save_lineplot_data(self):
		np.savetxt(self.path_to_save, np.column_stack([self.line_plot_data[0],self.line_plot_data[1]]))

	def _on_key_press(self, event):
		print("you pressed {}".format(event.key))
		key_press_handler(event, canvas, toolbar)

	def _load_output_image(self):
		try:
			self.path = filedialog.askopenfilename(initialdir = "_data_folder", title="Open output data", filetypes = [("PNG data","*.png"),("TXT data", ".txt")])
			if self.path[-3:]=="png":
				image = Image.open(self.path).convert('L')
			elif self.path[-3:]=="txt":
				image = self.mainController.first_column._load_txt_data_as_image(self.path)
			self.output_image = image
			self.phase_image_255 = np.uint8(self.output_image)
			self.mainController.third_column.output_window.output_image_preview = ImageTk.PhotoImage(self.output_image.resize((750,750)))
			self.mainController.third_column.output_window.create_image(0,0, image=self.mainController.third_column.output_window.output_image_preview,anchor="nw")
			self._remove_current_line()
		except:
			pass


	def _load_folder(self):
		naming = self.load_folder_textfield.textfield.get()
		path = filedialog.askdirectory(initialdir = "_data_folder", title="Open input folder")
		path = path + "/"
		path = path.casefold()
		naming = naming.casefold()
		wildcard_position = naming.find('?') + len(path)
		if "top" in naming:
			i = range(0,5)
			self._iterate_folder(path + naming,i,wildcard_position)
			i = range(5,10)
			naming = naming.replace("top","tran")
			wildcard_position = naming.find('?') + len(path)
			self._iterate_folder(path + naming,i,wildcard_position)
		elif "tran" in naming:
			i = range(5,10)
			self._iterate_folder(path + naming,i,wildcard_position)
			i = range(0,5)
			naming = naming.replace("tran","top")
			wildcard_position = naming.find('?') + len(path)
			self._iterate_folder(path + naming,i,wildcard_position)

	def _iterate_folder(self,path,i,wildcard_position):
		try:
			for k in i:
					a = k%5
					image_path = path[:wildcard_position]+str(a)+path[wildcard_position+1:]
					self.mainController.first_column._load_image(k, image_path)
		except:
			pass

	def _align(self):
		are_images_loaded, number_of_images, loaded_bool_array = self._check_topography_images_are_loaded()
		if are_images_loaded:
			are_images_same_dim = self._check_topology_images_are_same_dimension(number_of_images)
			if are_images_same_dim:
				dimension_holder = self._create_dimension_holder(number_of_images)
				crop = self._auto_align(number_of_images, dimension_holder)
				self._align_by_crop(number_of_images, crop)

	def _align_by_crop(self, number_of_images, crop):
		for k in range(number_of_images):
			self.mainController.first_column.image_loader[k].image = self.mainController.first_column.image_loader[k].image.crop(crop[k])
			self.mainController.first_column.image_loader[k].preview_image = ImageTk.PhotoImage(self.mainController.first_column.image_loader[k].image.resize((100,100),resample=1))
			self.mainController.first_column.image_loader[k].image_preview.configure(image = self.mainController.first_column.image_loader[k].preview_image)
			self.mainController.first_column.image_loader[k+5].image = self.mainController.first_column.image_loader[k+5].image.crop(crop[k])
			self.mainController.first_column.image_loader[k+5].preview_image = ImageTk.PhotoImage(self.mainController.first_column.image_loader[k+5].image.resize((100,100),resample=1))
			self.mainController.first_column.image_loader[k+5].image_preview.configure(image = self.mainController.first_column.image_loader[k+5].preview_image)

	def _auto_align(self, number_of_images, dimension_holder):
		crop = {}
		images_shift = self._get_shift_for_images(number_of_images)
		dimension_holder = self._shift_images(dimension_holder, images_shift)
		x_min = np.amax([item[0] for item in dimension_holder])
		y_min = np.amax([item[1] for item in dimension_holder])
		x_max = np.amin([item[2] for item in dimension_holder])
		y_max = np.amin([item[3] for item in dimension_holder])
		if x_max - x_min > y_max - y_min:
			shorter_side = y_max - y_min
			x_max = x_min + shorter_side
		else:
			shorter_side = x_max - x_min
			y_max = y_min + shorter_side
		final_image_dimensions = [x_min, y_min, x_max, y_max]
		for k in range(number_of_images):
			y_min = final_image_dimensions[0] - dimension_holder[k][0]
			x_min = final_image_dimensions[1] - dimension_holder[k][1]
			y_max = final_image_dimensions[2] - dimension_holder[k][0]
			x_max = final_image_dimensions[3] - dimension_holder[k][1]
			crop[k] = (x_min, y_min, x_max, y_max)
		return crop


	def _shift_images(self, dimension_holder, images_shift):
		for k in range(len(images_shift)):
			dimension_holder[k][0] += images_shift[k][0]
			dimension_holder[k][1] += images_shift[k][1]
			dimension_holder[k][2] += images_shift[k][0]
			dimension_holder[k][3] += images_shift[k][1]
			dimension_holder[k][4] += images_shift[k][0] / 2
			dimension_holder[k][5] += images_shift[k][1] / 2
		return dimension_holder

	def _create_dimension_holder(self, number_of_images):
		dimensions = []
		for k in range(number_of_images):
			shape = np.int32(self.mainController.first_column.image_loader[k].image).shape
			dimensions.append([0, 0, shape[0], shape[1], shape[0]/2, shape[1]/2])
		return dimensions

	def _check_topography_images_are_loaded(self):
		are_loaded = False
		number = 0
		image_exist_bool = np.array([0, 0, 0, 0, 0])
		for i in range(5):
			bool = 0
			exists_attr = hasattr(self.mainController.first_column.image_loader[i],"image")
			if exists_attr:
				bool = self.mainController.first_column.image_loader[i].image != None
			image_exist_bool[i] = bool
		if np.array_equal(image_exist_bool, np.array([1,1,1,1,0])) or np.array_equal(image_exist_bool, np.array([1,1,1,1,1])):
			are_loaded = True
			number = np.sum(image_exist_bool)
		return are_loaded, number, image_exist_bool


	def _check_topology_images_are_same_dimension(self, steps):
		first_image_dim = self.mainController.first_column.image_loader[0].image.size
		for i in range(1,steps):
			if first_image_dim == self.mainController.first_column.image_loader[i].image.size:
				continue
			else:
				return False
		return True


	def _get_shift_for_images(self, k):
		shift = []
		for i in range (0,k):

			# get rid of the color channels by performing a grayscale transform
			# the type cast into 'float' is to avoid overflows
			im1_gray = np.power(np.float32(self.mainController.first_column.image_loader[0].image),2)
			im2_gray = np.power(np.float32(self.mainController.first_column.image_loader[i].image),2)

			# get rid of the averages, otherwise the results are not good
			im1_gray = im1_gray - np.mean(im1_gray)
			im2_gray = im2_gray - np.mean(im2_gray)

			# calculate the correlation image; note the flipping of onw of the images
			corr_img = scipy.signal.fftconvolve(im1_gray, im2_gray[::-1,::-1], mode='same')
			shift.append(np.unravel_index(np.argmax(corr_img), corr_img.shape))
			if i > 0:
				shift[i] = [shift[i][0] - shift[0][0], shift[i][1] - shift[0][1]]
		shift[0] = [0,0]
		return shift

	def _open_aligned_images(self, k = 0):
		are_images_loaded, number_of_images, loaded_bool_array_topography = self._check_topography_images_are_loaded()
		are_images_loaded, number_of_images, loaded_bool_array_snom = self._check_snom_images_are_loaded()
		image_array_bool = np.concatenate((loaded_bool_array_topography,loaded_bool_array_snom))
		image_list, image_array_names = self._get_images_with_bool_array(image_array_bool)
		if not_none(self.mainController,"image_viewer") and self.mainController.image_viewer.open:
			self.mainController.image_viewer.images = image_list
			self.mainController.image_viewer.image_names = image_array_names
			self.mainController.image_viewer.image_index = k
			self.mainController.image_viewer._change_image(0)
		if len(image_list) > 0:
			self.mainController.image_viewer = ImageViewer(self.mainController, image_list, image_array_names, k)

	def _get_images_with_bool_array(self, bool_array):
		image_list = {}
		image_name_list = {}
		for k in range(len(bool_array)):
			if bool_array[k]:
				image_list[k] = self.mainController.first_column.image_loader[k].image
				image_name_list[k] = self.mainController.first_column.image_loader[k].name_label["text"]
		return image_list, image_name_list


	def _manual_align(self, number_of_images, dimension_holder, k = 0):
		are_images_loaded, number_of_images, loaded_bool_array_topography = self._check_topography_images_are_loaded()
		image_array_bool = loaded_bool_array_topography
		image_list, image_array_names = self._get_images_with_bool_array(image_array_bool)
		if not_none(self.mainController,"manual_align"):
			if self.mainController.manual_align.open:
				return
		if len(image_list) > 0:
			self.mainController.manual_align = ManualAlign(self.mainController, image_list, image_array_names, k)

	def _manual_align_return(self, image_centers):
		shift = []
		number_of_images = len(image_centers)
		for i in range(number_of_images):
			shift.append([int((image_centers[0][0] - image_centers[i][0])/1.5), int((image_centers[0][1] - image_centers[i][1])/1.5)])
		shift[0] = [0,0]
		print(shift)
		dimension_holder = self._create_dimension_holder(number_of_images)
		dimension_holder = self._shift_images(dimension_holder, shift)
		x_min = np.amax([item[0] for item in dimension_holder])
		y_min = np.amax([item[1] for item in dimension_holder])
		x_max = np.amin([item[2] for item in dimension_holder])
		y_max = np.amin([item[3] for item in dimension_holder])
		if x_max - x_min > y_max - y_min:
			shorter_side = y_max - y_min
			x_max = x_min + shorter_side
		else:
			shorter_side = x_max - x_min
			y_max = y_min + shorter_side
		final_image_dimensions = [x_min, y_min, x_max, y_max]
		crop = {}
		for k in range(number_of_images):
			y_min = final_image_dimensions[0] - dimension_holder[k][0]
			x_min = final_image_dimensions[1] - dimension_holder[k][1]
			y_max = final_image_dimensions[2] - dimension_holder[k][0]
			x_max = final_image_dimensions[3] - dimension_holder[k][1]
			crop[k] = (x_min, y_min, x_max, y_max)
		self._align_by_crop(number_of_images, crop)