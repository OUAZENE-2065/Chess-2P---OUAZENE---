import customtkinter as ctk
from option_window import OptionWindow

def func(d):
     global dict_
     dict_ = d

def function1(op = False):
     global dict_
     option_win = OptionWindow(root, 'Data Entry Form', tree,dict_, op)
     if op:
          root.after(10, lambda : func(option_win.dict))
     else :
          root.wait_window(option_win)
          dict_ = option_win.dict
     
def function2():
     for key, data in dict_.items():
          print(f'{key}:  {data}')

ctk.set_appearance_mode('dark')

root = ctk.CTk()
root.resizable(False,False)
root.title('Data Entry Form')

dict_ = {}
# Entry, Cbox, Sbox, Check
tree = [
     'taps', [
          [
               'User Data', [
                    'LFs', [
                         [
                              'User Information',
                              [
                                   {
                                        'type':'Entry',
                                        'id':'First Name',
                                        'row':1,
                                        'column':0,
                                        'label':'First Name',
                                        'l-row':0,
                                        'l-col':0,
                                        'text':'',
                                        'values':None,
                                        'var':'',
                                   },
                                   {
                                        'type':'Entry',
                                        'id':'Last Name',
                                        'row':1,
                                        'column':1,
                                        'label':'Last Name',
                                        'l-row':0,
                                        'l-col':1,
                                        'text':'',
                                        'values':None,
                                        'var':'',
                                   },
                                   {
                                        'type':'Cbox',
                                        'id':'Title',
                                        'row':1,
                                        'column':2,
                                        'label':'Title',
                                        'l-row':0,
                                        'l-col':2,
                                        'text':'',
                                        'values':["","Dr.","Ms.","Mr."],
                                        'var':'',
                                   },
                                   {
                                        'type':'Sbox',
                                        'id':'Age',
                                        'row':4,
                                        'column':0,
                                        'label':'Age',
                                        'l-row':3,
                                        'l-col':0,
                                        'text':'',
                                        'values':[18, 100],
                                        'var':'18',
                                   },
                                   {
                                        'type':'Cbox',
                                        'id':'Nationality',
                                        'row':4,
                                        'column':1,
                                        'label':'Nationality',
                                        'l-row':3,
                                        'l-col':1,
                                        'text':'',
                                        'values':sorted(['Africa','Europe','Asia','Antarctica','North America','South America','Oceania']),
                                        'var':'',
                                   }
                              ]
                         ],
                         [
                              '',
                              [
                                   {
                                        'type':'Check',
                                        'id':'Registration Status',
                                        'row':1,
                                        'column':0,
                                        'label':'Registration Status',
                                        'l-row':0,
                                        'l-col':0,
                                        'text':'Currently Registered',
                                        'values':['registered', 'not registered'],
                                        'var':'not registered',
                                   },
                                   {
                                        'type':'Sbox',
                                        'id':'# Completed Courses',
                                        'row':1,
                                        'column':1,
                                        'label':'# Completed Courses',
                                        'l-row':0,
                                        'l-col':1,
                                        'text':'',
                                        'values':[0, 'infinity'],
                                        'var':'0',
                                   },
                                   {
                                        'type':'Sbox',
                                        'id':'# Semesters',
                                        'row':1,
                                        'column':2,
                                        'label':'# Semesters',
                                        'l-row':0,
                                        'l-col':2,
                                        'text':'',
                                        'values':[0, 'infinity'],
                                        'var':'0',
                                   }
                              ]
                         ],
                         [
                              'Terms & Conditions',
                              [
                                   {
                                        'type':'Check',
                                        'id':'Terms & Conditions',
                                        'row':0,
                                        'column':0,
                                        'label':None,
                                        'l-row':None,
                                        'l-col':None,
                                        'text':'I accept the terms and conditions.',
                                        'values':['True', 'False'],
                                        'var':'False',
                                   }
                              ]
                         ]
                    ]
               ]
          ]
     ]
]

function1(True)

ctk.CTkButton(root, text='formula show', command=function1).pack(expand= True, padx= 20, pady= 20)
ctk.CTkButton(root, text='data show', command=function2).pack(expand= True, padx= 20, pady= 20)

root.mainloop()