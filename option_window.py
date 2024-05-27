import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

class OptionWindow(ctk.CTkToplevel):
    def __init__(self, parent, title, tree, dict, update_data = False):
        super().__init__(master = parent)
        self.resizable(False, False)
        self.title(title)
        self.attributes('-topmost', True)

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack()

        self.update_data = update_data
        self.vars = {}
        self.dict = dict

        self.create_element(self.main_frame, tree)

        self.subframe = ttk.Frame(self.main_frame)
        self.subframe.grid(row=3,column=0,sticky='news',padx=20,pady=10)
        self.ok = ttk.Button(self.subframe,text='   OK   ',command=self.submit)
        self.ok.pack(side='right', padx=10)
        self.cancel = ttk.Button(self.subframe,text=' Cancel ',command=self.cancel_func)
        self.cancel.pack(side='right', padx=10)

        if self.update_data:
            self.submit()

    def create_element(self, parent, element):
        if element[0] == 'taps':
            nbook = ttk.Notebook(parent)
            taps = {}
            count = 0
            for item in element[1]:
                count += 1
                taps[count] = tk.Frame(nbook)
                nbook.add(taps[count], text=item[0])
                self.create_element(taps[count], item[1])
            nbook.grid(row=0, column=0, sticky= 'news')
        elif element[0] == 'LFs':
            LFs = {}
            count = -1
            for item in element[1]:
                count += 1
                LFs[count] = ttk.LabelFrame(parent, text= item[0])
                LFs[count].grid(row=count,column=0,sticky='news' ,padx=20,pady=10)
                LFs[count].columnconfigure((0, 1, 2), weight=1, uniform='a')
                for widget in item[1]:
                    self.create_widget(LFs[count], widget['type'],widget['id'],widget['row'],widget['column'],
                    text= widget['text'],
                    label= widget['label'],
                    label_row= widget['l-row'],
                    label_column= widget['l-col'],
                    values= widget['values'],
                    var= widget['var'] if self.update_data else self.dict[widget['id']])

    def create_widget(self, parent, type_, id, row, column,var=None, text='', label=None, label_row=None, label_column=None, padx=10, pady=5, values=[]):
        if label:
            ttk.Label(parent, text=label).grid(row=label_row, column=label_column, padx=padx, pady=pady)
        self.vars[id] = tk.StringVar(value= var)
        if type_ == 'Entry':
            ttk.Entry(parent, textvariable=self.vars[id]).grid(row=row, column=column, padx=padx, pady=pady)
        elif type_ == 'Cbox':
            ttk.Combobox(parent,textvariable=self.vars[id],values = values).grid(row=row, column=column, padx=padx, pady=pady)
        elif type_ == 'Sbox':
            ttk.Spinbox(parent,textvariable=self.vars[id],from_=values[0], to=values[1]).grid(row=row, column=column, padx=padx, pady=pady)
        elif type_ == 'Check':
            ttk.Checkbutton(parent, text=text, variable=self.vars[id],onvalue=values[0], offvalue=values[1]).grid(row=row, column=column, padx=padx, pady=pady)

    def cancel_func(self):
        self.destroy()

    def submit(self):
        self.dict = {id: value.get() for id ,value in self.vars.items()}
        self.destroy()
