__author__ = "Yu Du"
__Email__ = "yu.du@clinchoice.com"
__date__ = "Nov 19,2020"
#######################################################################################################################

import tkinter as tk
from tkinter import ttk
from db_reader import DB
from PIL import ImageTk, Image
import tkinter.messagebox
from tkinter.font import Font
from functools import partial


class Editor(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.box_dict = dict()  # dictionary to store all the boxes
        self.database = DB()
        self.controller = controller
        ##################################### Frames ###################################################################
        self.topFrame = tk.Frame(self)
        self.topFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.addFrame = tk.Frame(self)
        self.addFrame.grid(row=5, pady=5)
        self.addFrame2 = tk.Frame(self)
        self.addFrame2.grid(row=5, column=1, pady=5)
        self.prevFrame = tk.Frame(self)
        self.prevFrame.grid(row=6, column=0, pady=25, sticky="nsew")
        self.editFrame = tk.Frame(self)
        self.editFrame.grid(row=6, column=1)
        self.endFrame = tk.Frame(self)
        self.endFrame.grid(row=7)
        ##################################### Column Config ############################################################
        self.columnconfigure(0, weight=1)
        # self.topFrame.columnconfigure(0, weight=1)
        # self.topFrame.columnconfigure(1, weight=5)
        ##################################### Elements #################################################################
        self.formSearch = None
        self.fieldSearch = None
        self.formList = None
        self.num_form = None
        self.num_field = None
        self.treev = None
        self.logo = None
        # show all the frames
        self.get_all()

    def get_all(self):
        """
        Method to call all the frames when the app starts
        Helper to debug and show partial frame
        :return:
        """
        self.get_top()
        self.get_mid()
        # self.get_add()
        self.get_end()

    def get_top(self):
        """
        "Top" part includes 1 frame: 3 sections, logo on the left, title on the middle and the statistics on the right top coner
        :return:
        """
        # self.topFrame.columnconfigure(0, weight=1)
        self.topFrame.columnconfigure(1, weight=1)
        PATH = './data/logo.jpeg'
        # Logo
        logo = ImageTk.PhotoImage(Image.open(PATH))
        self.logo = tk.Label(self.topFrame, image=logo)
        self.logo.image = logo
        self.logo.grid(row=0, column=0, sticky='w')
        # # Title
        tk.Label(self.topFrame, text="Welcome to eCRF Compiler", font=self.controller.title_font).grid(row=0, column=1, sticky='nsew')
        tk.Button(self.topFrame, text="Connect to Database", width=30, command=lambda: self.load_data()).grid(row=1, column=1, sticky='ns')
        tk.Label(self.topFrame, text="eCRF Phase-I Library Statics").grid(row=0, column=2)
        tk.Label(self.topFrame, text="# Forms: ").grid(row=0, column=3, padx=5, pady=5)
        self.num_form = tk.Label(self.topFrame, text='NA')
        self.num_form.grid(row=0, column=4, padx=5, pady=5)
        tk.Label(self.topFrame, text="# Fields: ").grid(row=1, column=3, padx=5, pady=5)
        self.num_field = tk.Label(self.topFrame, text='NA')
        self.num_field.grid(row=1, column=4,padx=5, pady=5)

    def get_mid(self):
        """
        "Mid" frame consists of 2 frames:
        :return:
        """
        # Create FormList Searchbox
        self.formList = tk.Listbox(self.topFrame, selectmode="single", exportselection=0, width=50, height=10)
        self.formList.bind('<<ListboxSelect>>', self.add_tree)
        tk.Label(self.topFrame, text="Form List").grid(row=2, column=1, pady=5)
        self.formSearch = tk.Entry(self.topFrame)
        self.formSearch.grid(row=3, column=1, pady=5)
        # Form list search function
        self.formSearch.bind('<KeyRelease>', self.checkkey)
        self.formList.grid(row=4, column=1, pady=5)
        # Initiated treeview frame, create treeview instance
        self.treev = Tree(self.prevFrame, self.box_dict)
        # self.treev.configure(height=15) # Treeview table height
        # Create Tree view edit frame
        tk.Button(self.editFrame, text="Remove", width=10, command=self.treev.remove_select). \
            pack(side='top', pady=10)
        tk.Button(self.editFrame, text="Move Up", width=10, command=self.treev.move_up).pack(side='top', pady=10)
        tk.Button(self.editFrame, text="Move Down", width=10, command=self.treev.move_down).pack(side='top', pady=10)

    def get_add(self):
        df = self.database.get_records('AE')
        df_col = list(df.columns)
        col_num = 0
        for col in df_col:
            lb = tk.Label(self.addFrame, text=col.split("(")[0], wraplength=200)
            lb.grid(row=0, column=col_num)
            self.box_dict[col] = tk.Entry(self.addFrame, width=10)
            self.box_dict[col].grid(row=1, column=col_num, sticky='w',padx=6)
            col_num += 1
        tk.Button(self.addFrame2, text="Update Record", width=10, command=lambda: self.treev.update_record()). \
            pack(side='top')

    def get_end(self):
        """
        Get the "end" part. Includes only one frame.
        :return:
        """
        tk.Button(self.endFrame, text="Add to Cart", width=10, command=lambda: self.add_cart()). \
            pack(side='left', padx=20, pady=20)
        cart = tk.Button(self.endFrame, text="View Cart", command=lambda: self.controller.show_frame('Exporter'))
        cart.pack(side='right')
        # tk.Button(self.endFrame, text="Back", width=10, command=lambda: self.controller.show_frame('Selector')).pack()

    def load_data(self):
        """
        helper function to load data including the database statistics and preload all the stats
        :return: Null
        """
        self.get_forms()
        num_forms, num_fields = self.database.get_stats()
        self.num_form.config(text=str(num_forms))
        self.num_field.config(text=str(num_fields))

    def get_forms(self):
        """
        helper function to load the form list from database and insert into listbox
        :return:
        """
        forms = self.database.get_forms()
        for form in forms:
            self.formList.insert('end', form)
        return None

    def checkkey(self, event):
        """
        helper function to dynamically update the search box and value assoicated with.
        :param event:
        :return:
        """
        value = event.widget.get()
        if value == '':
            data = self.database.get_forms()
        else:
            data = []
            for oid, name in self.database.get_forms():
                if value.lower() in oid.lower() or value.lower() in name.lower():
                    data.append((oid, name))
                    # update data in listbox
        self.update_list(data)

    def update_list(self, data):
        # clear previous data
        self.formList.delete(0, 'end')
        # put new data
        for item in data:
            self.formList.insert('end', item)

    @staticmethod
    def motion_handler(tree, event):
        f = Font(font='TkDefaultFont')
        # A helper function that will wrap a given value based on column width
        def adjust_newlines(val, width, pad=10):
            if not isinstance(val, str):
                return val
            else:
                words = val.split()
                lines = [[],]
                for word in words:
                    line = lines[-1] + [word,]
                    if f.measure(' '.join(line)) < (width - pad):
                        lines[-1].append(word)
                    else:
                        lines[-1] = ' '.join(lines[-1])
                        lines.append([word,])

                if isinstance(lines[-1], list):
                    lines[-1] = ' '.join(lines[-1])

                return '\n'.join(lines)

        if (event is None) or (tree.identify_region(event.x, event.y) == "separator"):
            # You may be able to use this to only adjust the two columns that you care about
            # print(tree.identify_column(event.x))

            col_widths = [tree.column(cid)['width'] for cid in tree['columns']]

            for iid in tree.get_children():
                new_vals = []
                for (v,w) in zip(tree.item(iid)['values'], col_widths):
                    new_vals.append(adjust_newlines(v, w))
                tree.item(iid, values=new_vals)

    def add_tree(self, event):
        """
        Helper function to add more records into the tree view.
        :param event:
        :return:
        """
        self.treev.remove_all()
        w = event.widget
        index = w.curselection()
        formoid, formname = w.get(index)
        df = self.database.get_records(formoid)
        df_col = list(df.columns)
        df_col = list(x.split('\n')[0] for x in df_col)
        self.treev["columns"] = df_col

        for x in df_col:
            self.treev.heading(x, text=x, anchor=tk.CENTER)
            self.treev.column(x, anchor=tk.CENTER, width=120, stretch=tk.YES)
        for index, row in df.iterrows():
            if list(row)[0] != "EOF":
                self.treev.insert("", index='end', values=list(row))

        # self.treev.bind('<B1-Motion>', partial(self.motion_handler, self.treev))
        # self.motion_handler(self.treev, None)   # Perform initial wrapping

    def add_cart(self):
        try:
            formoid, name = self.formList.get(self.formList.curselection())
        except tk.TclError:
            tk.messagebox.showerror("Error", "You must connect to database and select at least one item to add")
        fields = list()
        for line in self.treev.get_children():
            fields.append(self.treev.item(line)['values'][2])
        self.controller.selected[formoid] = fields


class Tree(ttk.Treeview):
    def __init__(self, master, box_dict=None, **kw):
        super(Tree, self).__init__(master=master, **kw)
        self.style = ttk.Style()
        self.style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 10), relief=[('active','groove'),('pressed','sunken')])
        self.style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'),  background="gray")
        self.style.configure("Treeview", rowheight=30) # Treeview table height
        # self.configure(height=15) # Treeview table height
        self.selectmode = 'extended'
        self['show'] = 'headings'
        self.bind("<Double-1>", self.clicker)
        self.vsb = tk.Scrollbar(master, orient=tk.VERTICAL, command=self.yview)
        self.hsb = tk.Scrollbar(master, orient=tk.HORIZONTAL, command=self.xview)
        self.configure(yscrollcommand=self.vsb.set)
        self.configure(xscrollcommand=self.hsb.set)
        self.box_dict = box_dict
        self.vsb.pack(side='right', fill='y')
        self.hsb.pack(side='bottom', fill='x')
        self.pack(fill=tk.BOTH)

    def select_record(self):
        # Clear the entry box
        for key, item in self.box_dict.items():
            item.delete(0, 'end')
        # Grab the record number
        selected = self.focus()
        # Grab the record values
        values = self.item(selected, 'values')
        i = 0
        for box in self.box_dict.values():
            box.insert(0, values[i])
            i += 1

    def update_record(self):
        selected = self.focus()
        # save the new item
        new_record = list()
        for box in self.box_dict.values():
            new_record.append(box.get())
        self.item(selected, text='', values=new_record)
        # Clear the entry box
        for key, item in self.box_dict.items():
            item.delete(0, 'end')

    def clicker(self, e):
        self.select_record()

    def remove_select(self):
        for record in self.selection():
            self.delete(record)

    def remove_all(self):
        for record in self.get_children():
            self.delete(record)

    def move_up(self):
        rows = self.selection()
        for row in rows:
            self.move(row, self.parent(row), self.index(row) - 1)

    def move_down(self):
        rows = self.selection()
        for row in rows:
            self.move(row, self.parent(row), self.index(row) + 1)
