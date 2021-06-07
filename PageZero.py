__author__ = "Yu Du"
__Email__ = "yu.du@clinchoice.com"
__date__ = "Dec 15,2020"
#######################################################################################################################

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from out_writer import Compiler
from PIL import ImageTk, Image
from tkinter import filedialog

class Selector(tk.Frame):
	"""docstring for Selector"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.compiler = Compiler()
		self.topFrame = tk.Frame(self)
		self.topFrame.pack()
		self.midFrame = tk.Frame(self)
		self.midFrame.pack(pady=50)
		self.endFrame = tk.Frame(self)
		self.endFrame.pack(pady=75)
		self.font = tkfont.Font(family='Helvetica Neue', size=15)
		self.get_all()

	def get_all(self):
		self.get_top()
		self.get_mid()
		self.get_end()

	def get_top(self):
		PATH = './data/logo.jpeg'
        # Logo
		logo = ImageTk.PhotoImage(Image.open(PATH))
		self.logo = tk.Label(self.topFrame, image=logo)
		self.logo.image = logo
		self.logo.pack(side='top', pady=20)
		tk.Label(self.topFrame, text="Welcome to eCRF Compiler", font=self.controller.title_font).pack(side='top', pady=50)
		tk.Label(self.topFrame, text="Attention!! This is a alpha version for ClinChoice Internal Use Only! No other distributions is allowed").pack(side='top')

	def get_mid(self):
		self.startnew = tk.Button(self.midFrame, text = "New Draft",width=25, height=5, bg='#4267B2',fg='white', font=self.font,command=lambda:self.new_file()).pack(side='left',padx=30,pady=15)
		self.resume = tk.Button(self.midFrame, text = "Resume Work",width=25, height=5, bg='#4267B2',fg='white', font=self.font,command=lambda:self.resume_file()).pack(side='right', padx=30,pady=15)

	def get_end(self):
		self.exit = tk.Button(self.endFrame, text="Exit", width=30, command=lambda: self.controller.destroy()).pack(pady=30)

	def resume_file(self):
		self.controller.file_bol = False
		self.controller.filename = filedialog.askopenfilename(initialdir="./output/", filetypes=(("Excel Workbook (.xlsx)", "*.xlsx"), ("all_files", "*")))
		if self.controller.filename != '':
			self.controller.show_frame('Editor')
			self.controller.selected = self.compiler.read_selected(self.controller.filename) # This assign the forms and fields in exsiting file to the python dictionary.


	def new_file(self):
		self.controller.file_bol = True
		self.controller.show_frame('Editor')









