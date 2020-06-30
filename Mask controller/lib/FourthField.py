from PIL import Image, ImageTk
import tkinter as tk

class FourthField():

	def __init__(self,mainController):
		self.mainController = mainController
		self.create_fourth_field()

	def create_fourth_field(self):
		self.make_frame_4()
		self.make_image_preview_label()
		self.update_images()

	def make_frame_4(self):
		self.frame_4 = tk.Frame(master=self.mainController.mainWindow, borderwidth=1, relief=tk.RAISED)
		self.frame_4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

	def make_image_preview_label(self):
		self.displayPreviewWindowLabel = tk.Label(master=self.frame_4)
		self.displayPreviewWindowLabel.bind('<Button-1>', self.mainController.changeCenter.get_mouse_position)
		self.displayPreviewWindowLabel.pack(side="left")

	def update_images(self):
		self.update_image()
		self.update_image_preview()
		self.update_image_preview_label()

	def update_image(self,angle=0):
		self.mainController.rotationObject.rotate_image(self.mainController.angle.get_angle())
		self.displayImage = ImageTk.PhotoImage(self.mainController.rotationObject.imageHolder)

	def update_image_preview(self):
		self.displayImagePreview = ImageTk.PhotoImage(self.mainController.rotationObject.imageHolder.resize((self.mainController.config.previewX,self.mainController.config.previewY),resample=3))
			
	def update_image_preview_label(self):
		self.displayPreviewWindowLabel.configure(image = self.displayImagePreview)
		self.displayPreviewWindowLabel.image = self.displayImagePreview