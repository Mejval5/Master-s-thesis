
import fractions
import tkinter as tk
from PIL import Image
from tkinter import font as tkFont


def check_if_entry_value_is_legal(value):
				try:
					fractions.Fraction(value.get())
				except:
					value.set("0")
				return value.get()

def check_if_entry_value_is_legal_realtime(value):
				try:
					fractions.Fraction(value.get())
				except:
					return 0
				return value.get()

def make_button(_master, _text, _command, _row=0, _column=0, _padx=0, _pady=0, _columnspan=1, _rowspan=1, _sticky=""):
	holder = tk.Button(master=_master, relief=tk.RAISED, text=_text, command=_command)
	set_grid(holder,_row,_column, _columnspan, _rowspan, _padx, _pady, _sticky)
	return holder

def make_frame(_master, _row=0, _column=0, _padx=0, _pady=0, _columnspan=1, _rowspan=1, _raised=tk.FLAT, _sticky = "nsew"):
	holder = tk.Frame(master=_master, borderwidth=5, relief= _raised)
	set_grid(holder,_row,_column,_columnspan, _rowspan, _padx, _pady, _sticky = _sticky)
	return holder

def make_label(_master, _text="", _row=0, _column=0, _padx=0, _pady=0, _columnspan=1, _rowspan=1, _raised=tk.FLAT):
	holder = tk.Label(master=_master, text=_text, borderwidth=5, relief= _raised)
	set_grid(holder,_row,_column,_columnspan, _rowspan, _padx, _pady,"ew")
	return holder

def make_scale(_master, _row=0, _column=0, _padx=0, _pady=0, _columnspan=1, _rowspan=1, _raised=tk.FLAT, _from_=0, _to=100, _resolution=1):
	holder = tk.Scale(master=_master, borderwidth=5, relief= _raised, from_=_from_, to=_to, resolution = _resolution, orient=tk.HORIZONTAL)
	set_grid(holder,_row,_column,_columnspan, _rowspan, _padx, _pady,"ew")
	return holder

def make_canvas(_master):
	holder = tk.Canvas(_master)
	set_grid(holder,_row=0,_column=0,_columnspan=1, _rowspan=1, _padx=0, _pady=0,_sticky="nsew")
	return holder

def make_checkbox(_master, _text="", _row=0, _column=0, _padx=5, _pady=5, _columnspan=1, _rowspan=1, _value=True, _command=""):
	checkbox_frame = make_frame(_master)
	checkbox_frame.var = tk.IntVar()
	checkbox_frame.var.set(_value)
	checkbox_frame.checkbox = tk.Checkbutton(master=checkbox_frame, text=_text,variable=checkbox_frame.var, command=_command)
	set_grid(checkbox_frame,_row,_column,_columnspan, _rowspan, _padx, _pady,"ew")
	set_grid(checkbox_frame.checkbox,_row=0,_column=0,_columnspan=1, _rowspan=1, _padx=0, _pady=0, _sticky="ew")
	return checkbox_frame

def make_textfield(_master, _text="", _row=0, _column=0, _padx=5, _pady=5, _columnspan=1, _rowspan=1, _value="0",_width=5):
	textfield_frame = make_frame(_master)
	textfield_frame.var = tk.StringVar()
	textfield_frame.var.set(_value)
	textfield_frame.textfield = tk.Entry(master=textfield_frame,width=_width,textvariable=textfield_frame.var,justify='right')
	textfield_frame.label = tk.Label(master=textfield_frame, text=_text, borderwidth=5)
	set_grid(textfield_frame,_row,_column,_columnspan, _rowspan, _padx, _pady,"ew")
	set_grid(textfield_frame.textfield,_row=0,_column=0,_columnspan=1, _rowspan=1, _padx=0, _pady=0, _sticky="ew")
	set_grid(textfield_frame.label,_row=0,_column=1,_columnspan=1, _rowspan=1, _padx=0, _pady=0, _sticky="ew")
	return textfield_frame

def set_grid(holder,_row,_column,_columnspan, _rowspan, _padx, _pady,_sticky=""):
	holder.grid(row=_row,column=_column, padx=_padx, pady=_pady, columnspan=_columnspan, rowspan=_rowspan, sticky=_sticky)

def convert_index_1D(i):
	if i < 5:
		return i, 0
	else:
		return i-5, 1

def convert_index_2D(i,j):
	return i + j*5

def not_none(object,child):
	if hasattr(object,child):
		if getattr(object,child) is not None:
			return True
	return False

def concatenate_images_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst