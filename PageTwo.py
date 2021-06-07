__author__ = "Yu Du"
__Email__ = "yu.du@Clinchoice.com"
__date__ = "Dec 1,2020"
##########################################################################################################
import tkinter as tk
from PageOne import Tree
from tkinter import ttk
from db_reader import DB
from out_writer import Compiler
import time
from PIL import ImageTk, Image
import tkinter.messagebox


class Exporter(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.compiler = Compiler()
        self.database = DB()
        ##################################### Frames ###################################################################
        self.topFrame = tk.Frame(self, height=300)
        self.topFrame.grid(row=0, column=0, columnspan=1, sticky="nsew")
        self.prevFrame = tk.Frame(self)
        self.prevFrame.grid(row=1, column=0, sticky="nsew", pady=20)
        self.selectFrame = tk.Frame(self)
        self.selectFrame.grid(row=2, column=0, pady=10)
        self.endFrame = tk.Frame(self)
        self.endFrame.grid(row=3, column=0, pady=10)
        self.columnconfigure(0, weight=1)
        ##################################### Elements #################################################################
        self.formList = None
        self.mpb_text = None
        self.treev = None
        self.var1 = None
        self.var2 = None
        self.var3 = None
        # show all the frames
        self.get_all()

    def get_all(self):
        """
        Method to call all the frames when the app starts
        :return:
        """
        self.get_top()
        self.get_mid()
        self.get_select()
        self.get_end()

    def get_top(self):
        self.topFrame.columnconfigure(1, weight=1)
        PATH = './data/logo.jpeg'
        # Logo
        logo = ImageTk.PhotoImage(Image.open(PATH))
        self.logo = tk.Label(self.topFrame, image=logo)
        self.logo.image = logo
        self.logo.grid(row=0, column=0, sticky='w')
        # Title
        tk.Label(self.topFrame, text="Welcome to eCRF Compiler", font=self.controller.title_font).grid(row=0, column=1, sticky='nsew')
        tk.Button(self.topFrame, text="Load Cart", width=30, command=lambda: self.get_cart()).grid(row=1, column=1, sticky='ns')
        tk.Label(self.topFrame, text="eCRF Phase-I Library Statics").grid(row=0, column=2)
        tk.Label(self.topFrame, text="# Forms: ").grid(row=0, column=3, padx=5, pady=5)
        num_form, num_field = self.database.get_stats()
        self.num_form = tk.Label(self.topFrame, text = str(num_form))
        self.num_form.grid(row=0, column=4, padx=5, pady=5)
        tk.Label(self.topFrame, text="# Fields: ").grid(row=1, column=3, padx=5, pady=5)
        self.num_field = tk.Label(self.topFrame, text= str(num_field))
        self.num_field.grid(row=1, column=4,padx=5, pady=5)

    def get_mid(self):
        self.formList = tk.Listbox(self.topFrame, selectmode="single", exportselection=0, width=50, height=10)
        self.formList.bind('<<ListboxSelect>>', self.prev_tree)
        tk.Label(self.topFrame, text="Form List").grid(row=2, column=1, pady=5)
        self.formSearch = tk.Entry(self.topFrame)
        self.formSearch.grid(row=3, column=1, pady=5)
        # Form list search function
        self.formSearch.bind('<KeyRelease>', self.checkkey)
        self.formList.grid(row=4, column=1, pady=5)
        self.treev = Tree(self.prevFrame)
        self.treev.configure(height=7) # Treeview table height

    def get_select(self):
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.IntVar()
        self.var4 = tk.IntVar()
        self.var5 = tk.IntVar()
        tk.Checkbutton(self.selectFrame, text="Signature Page", variable=self.var1).grid(row=0, column=0, sticky='w')
        tk.Checkbutton(self.selectFrame, text="Instruction Page", variable=self.var2).grid(row=0, column=1, sticky='w')
        tk.Checkbutton(self.selectFrame, text="Version History Page", variable=self.var3).grid(row=0, column=2, sticky='w')
        tk.Checkbutton(self.selectFrame, text="Dynamic Page", variable=self.var4).grid(row=0, column=3, sticky='w')
        tk.Checkbutton(self.selectFrame, text="Derivation Page", variable=self.var5).grid(row=0, column=4, sticky='w')

    def get_end(self):
        self.mpb_text = tk.Label(self.endFrame)
        self.mpb_text.pack(side='top')
        self.mpb = ttk.Progressbar(self.endFrame, orient="horizontal", length=200, mode="determinate")
        self.mpb.pack(pady=10)
        self.mpb["maximum"] = 100
        tk.Button(self.endFrame, text="Export", width=10, command=lambda: self.output()).pack(side='left', padx=20,
                                                                                              pady=10)
        tk.Button(self.endFrame, text="Back", width=10, command=lambda: self.controller.show_frame('Editor')
                  ).pack(side='right', padx=25, pady=10)

    def get_cart(self):
        # To test if this is first time calling the method, if not, deleted previously selected
        self.formList.delete(0, 'end')

        # To test if the program going to read from existing file or assign new cart.
        if self.controller.file_bol == False:
            # selected_dict = self.compiler.read_selected(self.controller.filename)
            self.compiler.selected = self.controller.get_selected()


        if self.controller.file_bol == True:
            self.compiler.selected = self.controller.get_selected()

        # self.compiler.selected = selected_dict  # assigned for output purposes. Assign the selected value in the compiler
        forms = list()
        for key in self.compiler.selected.keys():
            forms.append(key)
        data = self.database.get_selectedForm(forms)
        for x in data:
            self.formList.insert('end', x)
        return None

    def prev_tree(self, event):
        self.remove_all()
        w = event.widget
        index = w.curselection()
        formoid, formname = w.get(index)
        fields = self.compiler.selected[formoid]
        df = self.database.get_selectedFields(fields)
        df_col = list(df.columns)
        df_col = list(x.split('\n')[0] for x in df_col)
        self.treev["columns"] = df_col
        for x in df_col:
            self.treev.heading(x, text=x, anchor=tk.CENTER)
            self.treev.column(x, anchor=tk.CENTER, width=120, stretch=tk.YES)
        for index, row in df.iterrows():
            if list(row)[0] != "EOF":
                self.treev.insert("", index='end', values=list(row))

    def checkkey(self, event):
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

    def remove_all(self):
        for record in self.treev.get_children():
            self.treev.delete(record)

    def step(self):
        """
        function to create a progress bar of downloading process.
        """
        self.mpb_text.config(text='Downloading...')
        self.mpb['value'] = 20
        self.update()
        time.sleep(1)
        self.mpb['value'] = 50
        self.update()
        time.sleep(1)
        self.mpb['value'] = 80
        self.update()
        time.sleep(1)
        self.mpb['value'] = 100
        self.mpb_text.config(text="Completed!")

    def output(self):
        sign_bol = False
        ins_bol = False
        ver_bol = False
        dyn_bol = False
        der_bol = False

        if self.var1.get() == 1:
            sign_bol = True
        if self.var2.get() == 1:
            ins_bol = True
        if self.var3.get() == 1:
            ver_bol = True
        if self.var4.get() == 1:
            dyn_bol = True
        if self.var5.get() == 1:
            der_bol = True

        try:
            self.compiler.output(sign_bol, ins_bol, ver_bol, dyn_bol, der_bol)
            self.step()
        except IndexError as e:
            tk.messagebox.showerror("Error", "Please select at least one form.") 
        except PermissionError as e:
            tk.messagebox.showerror("Error", "Please check the permission of the file.")


        if len(self.compiler.na_dict) != 0:
            tk.messagebox.showwarning("Warning", "Exact dictionary not found\nplease find more details in 'Missing_Dict.txt'")
            self.compiler.out_text()
        return None
