import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox
import tkinter as tk
from json import load, dump
from copy import deepcopy
from PIL import Image , ImageTk
import time
import webbrowser
from option_window import OptionWindow
from pygame import mixer

ctk.set_appearance_mode('dark')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        
        with open('data.json', 'r') as file:
            self.data = load(file)
        
        self.title('Chess 2P')
        self.geometry(f'{self.data["width"]}x{self.data["height"]}+50+0')
        
        self.NUMTOALPHA = {
            1 : 'A',
            2 : 'B',
            3 : 'C',
            4 : 'D',
            5 : 'E',
            6 : 'F',
            7 : 'G',
            8 : 'H'
        }
        self.POINTS = {
            'Pawn': 1 ,
            'Knight': 3 ,
            'Bishop': 3 ,
            'Rock': 5 ,
            'Queen': 9 ,
        }
        self.temp_images = {}
        self.temp_images['squares'] = {}
        self.temp_images['pieces'] = {}
        self.temp_images['actions'] = []
        self.temp_images['CheckMate'] = []
        self.begin_turn = 'White'
        self.squares = {}
        self.pieces = {}
        mixer.init()
        self.flip = False
        self.auto_flip = False
        self.audio = True
        self.themes_or_colors = True
        self.in_game = False
        self.play = False
        self.can_save = False
        self.bsquare_color = False
        self.wsquare_color = False
        self.with_moves = ctk.BooleanVar(value=False)
        self.with_moves.trace('w', self.save_active)
        self.dict_ = {}
        self.tree = [
                'taps', [
                    [
                        'Game settings', [
                                'LFs', [
                                    [
                                        'Before Play',
                                        [
                                            {
                                                    'type':'Cbox',
                                                    'id':'turn',
                                                    'row':1,
                                                    'column':1,
                                                    'label':'First turn',
                                                    'l-row':0,
                                                    'l-col':1,
                                                    'text':'',
                                                    'values':sorted(['White','Black']),
                                                    'var':'White',
                                            }
                                        ]
                                    ],
                                    [
                                        'Assets',
                                        [
                                            {
                                                    'type':'Check',
                                                    'id':'flip',
                                                    'row':0,
                                                    'column':1,
                                                    'label':None,
                                                    'l-row':None,
                                                    'l-col':None,
                                                    'text':'auto flip',
                                                    'values':['True', 'False'],
                                                    'var':'False',
                                            }
                                        ]
                                    ]
                                ]
                        ]
                    ],
                    [
                        'Graphic', [
                                'LFs', [
                                    [
                                        '',
                                        [
                                            {
                                                    'type':'Check',
                                                    'id':'themes_or_colors',
                                                    'row':0,
                                                    'column':0,
                                                    'label':None,
                                                    'l-row':None,
                                                    'l-col':None,
                                                    'text':'Use themes (if not use colors).',
                                                    'values':['True', 'False'],
                                                    'var':'True',
                                            }
                                        ]
                                    ],
                                    [
                                        'Themes',
                                        [
                                            {
                                                    'type':'Cbox',
                                                    'id':'Themes',
                                                    'row':1,
                                                    'column':1,
                                                    'label':'Choose One :',
                                                    'l-row':0,
                                                    'l-col':1,
                                                    'text':'',
                                                    'values':["Wood","Ice","Space"],
                                                    'var':'Wood',
                                            }
                                        ]
                                    ],
                                    [
                                        'Colors',
                                        [
                                            {
                                                    'type':'Entry',
                                                    'id':'bsquare_color',
                                                    'row':1,
                                                    'column':0,
                                                    'label':'Black Square Color',
                                                    'l-row':0,
                                                    'l-col':0,
                                                    'text':'',
                                                    'values':None,
                                                    'var':'black',
                                            },
                                            {
                                                    'type':'Entry',
                                                    'id':'wsquare_color',
                                                    'row':1,
                                                    'column':1,
                                                    'label':'White Square Color',
                                                    'l-row':0,
                                                    'l-col':1,
                                                    'text':'',
                                                    'values':None,
                                                    'var':'white',
                                            },
                                            {
                                                    'type':'Entry',
                                                    'id':'text_color',
                                                    'row':1,
                                                    'column':2,
                                                    'label':'Numbers Color',
                                                    'l-row':0,
                                                    'l-col':2,
                                                    'text':'',
                                                    'values':None,
                                                    'var':'blue',
                                            }
                                        ]
                                    ],
                                    [
                                        'Pieces',
                                        [
                                            {
                                                    'type':'Cbox',
                                                    'id':'Peices',
                                                    'row':1,
                                                    'column':1,
                                                    'label':'Peices Theme :',
                                                    'l-row':0,
                                                    'l-col':1,
                                                    'text':'',
                                                    'values':["floo","normal"],
                                                    'var':'normal',
                                            }
                                        ]
                                    ]
                                ]
                            ]
                    ],
                    [
                        'Audio', [
                                'LFs', [
                                    [
                                        '',
                                        [
                                            {
                                                    'type':'Check',
                                                    'id':'audio',
                                                    'row':0,
                                                    'column':0,
                                                    'label':None,
                                                    'l-row':None,
                                                    'l-col':None,
                                                    'text':'turn audio.',
                                                    'values':['True', 'False'],
                                                    'var':'True',
                                            }
                                        ]
                                    ]
                                ]
                            ]
                    ]
                ]
            ]
        
        self.settings(True)
        
        self.create_menu()
        
        self.begin_app()
        
        self.mainloop()
    
    def settings(self, op = False):
        option_win = OptionWindow(self, 'Data Entry Form', self.tree,self.dict_, op)
        if op:
            self.after(10, lambda : self.func(option_win.dict))
        else :
            pre = self.play
            self.play = False
            self.wait_window(option_win)
            self.dict_ = option_win.dict
            self.play = pre
            if self.dict_['themes_or_colors'] in ('True', 'False'):
                self.themes_or_colors = False if self.dict_['themes_or_colors'] == 'False' else True
            for key, data in self.dict_.items():
                match key:
                    case 'turn':
                        if data in ('White', 'Black'):
                            self.begin_turn = data
                    case 'flip':
                        if data in ('True', 'False'):
                            self.auto_flip = False if data == 'False' else True
                    case 'Themes':
                        if self.themes_or_colors:
                            if data in ('Wood', 'Ice', 'Space'):
                                self.data['squares']['black'] = self.data[data]['black']
                                self.data['squares']['white'] = self.data[data]['white']
                                self.bsquare_color = False
                                self.wsquare_color = False
                    case 'bsquare_color':
                        if not self.themes_or_colors:
                            if (data.lower() in ('white', 'black', 'blue', 'red', 'green', 'light green', 'yellow')) or ((len(data) == 7) and (data[0] == '#') and (data[1:].is_digit())):
                                self.bsquare_color = True
                                print('hi')
                                self.data['squares']['black'] = data.lower()
                    case 'wsquare_color':
                        if not self.themes_or_colors:
                            if (data.lower() in ('white', 'black', 'blue', 'red', 'green', 'light green', 'yellow')) or ((len(data) == 7) and (data[0] == '#') and (data[1:].is_digit())):
                                self.wsquare_color = True
                                self.data['squares']['white'] = data.lower()
                    case 'text_color':
                        if not self.themes_or_colors:
                            if (data.lower() in ('white', 'black', 'blue', 'red', 'green', 'light green', 'yellow')) or ((len(data) == 7) and (data[0] == '#') and (data[1:].is_digit())):
                                self.data['text_color'] = data.lower()
                    case 'audio':
                        if data in ('True', 'False'):
                            self.audio = False if data == 'False' else True
                    case 'Peices':
                        if data in ('floo', 'normal'):
                            self.data['pieces'] = self.data[data]
            if self.in_game:
                self.create_board_begin()
    
    def sound(self, path):
        if self.audio:
            sound = mixer.Sound(path)
            sound.play()
    
    def func(self, d):
        self.dict_ = d
    
    def documentation(self):
        webbrowser.open("documentation\\index.html")
        
    def save_active(self, *_):
        if self.with_moves.get():
            self.game_menu.entryconfig("Save Game",state='normal')
            self.can_save = True
            self.game_menu.entryconfig("Back and Save",state='normal')
            self.edit_menu.entryconfig("Undo",state='normal')
            self.game_menu.entryconfig("New Game",state='normal')
        else :
            self.game_menu.entryconfig("Save Game",state='disabled')
            self.can_save = False
            self.game_menu.entryconfig("Back and Save",state='disabled')
            self.edit_menu.entryconfig("Undo",state='disabled')
            if self.in_game:
                self.game_menu.entryconfig("New Game",state='disabled')
            else :
                self.game_menu.entryconfig("New Game",state='normal')
    
    def begin_app(self):
        self.hello_frame = ctk.CTkFrame(self, corner_radius=0, border_width=0, fg_color='transparent')
        self.hello_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.sub_frame = ctk.CTkFrame(self.hello_frame, corner_radius=0, border_width=0, fg_color='transparent')
        ctk.CTkLabel(self.sub_frame, text='Chess 2P', font=('Arial Rounded MT Bold', 100)).pack(pady=70)
        ctk.CTkButton(self.sub_frame, command=self.new_game,text='New Game', width=200, height=50, font=('Arial Rounded MT Bold', 30), fg_color='white', text_color='black', hover_color='#C8C8C7', corner_radius=15).pack(pady=5)
        ctk.CTkButton(self.sub_frame, command=self.load_game,text='Load Game', width=200, height=50, font=('Arial Rounded MT Bold', 30), fg_color='white', text_color='black', hover_color='#C8C8C7', corner_radius=15).pack(pady=5)
        ctk.CTkButton(self.sub_frame, command=self.settings,text='Settings', width=200, height=50, font=('Arial Rounded MT Bold', 30), fg_color='white', text_color='black', hover_color='#C8C8C7', corner_radius=15).pack(pady=5)
        ctk.CTkButton(self.sub_frame, command=self.show_about,text='About', width=200, height=50, font=('Arial Rounded MT Bold', 30), fg_color='white', text_color='black', hover_color='#C8C8C7', corner_radius=15).pack(pady=5)
        ctk.CTkButton(self.sub_frame, command=self.documentation,text='Documentation', width=200, height=50, font=('Arial Rounded MT Bold', 30), fg_color='white', text_color='black', hover_color='#C8C8C7', corner_radius=15).pack(pady=5)
        ctk.CTkButton(self.sub_frame, command=self.destroy,text='Exit', width=200, height=50, font=('Arial Rounded MT Bold', 30), fg_color='white', text_color='black', hover_color='#C8C8C7', corner_radius=15).pack(pady=5)
        ctk.CTkLabel(self.sub_frame, text='by OUAZENE Abdelmohsen', font=('Arial Rounded MT Bold', 20)).pack(pady=10)
        self.sub_frame.pack(expand=True)
        
    def create_init_board(self):
        self.board = Board(turn=self.begin_turn)
        
    def new_game(self):
        self.create_init_board()
        self.in_game = True
        self.checked = False
        self.with_moves.set(False)
        self.current_time = -1
        self.play = True
        self.begin_game()
    
    def restart(self):
        if self.in_game:
            if self.with_moves.get():
                if self.can_save:
                    pre = self.play
                    self.play = False
                    if messagebox.askyesno("Save Game", "Do you want to save the current game before creating a new one?"):
                        self.save_game()
                    self.play = pre
                self.with_moves.set(False)
                self.board.load_()
                self.current_time = -1
                self.play = True
                self.checked = False
                self.create_board_begin()
                self.update_history()
        else :
            self.new_game()
    
    def save_game(self):
        # new_game = True, board = None, pre_in_game = [], end_data = None
        # , killed_pieces = None, dame_info = None, history = None, turn = 'White'
        # , custom_game = False, in_game = True
        # , end_game = False, dame_event = False, event = False
        pre = self.play
        self.play = False
        file_path = filedialog.asksaveasfilename(defaultextension=".Chs",
                                                 filetypes=[("Chess Game", "*.Chs")])
        self.play = pre
        if file_path:
            data = {
                'pre_in_game' : self.board.pre_in_game,
                'end_data' : self.board.end_data,
                'end_game' : self.board.end_game,
                'dame_info' : self.board.dame_info,
                'dame_event' : self.board.dame_event,
                'event' : self.board.event,
                'in_game' : self.in_game,
                'board' : self.board.board,
                'custom_game' : self.board.custom_game,
                'kill' : self.board.killed_pieces,
                'history' : self.board.history,
                'turn' : self.board.turn,
                'time' : self.current_time
            }
            with open(file_path, 'w') as file:
                dump(data, file, indent=4)
    
    def load_game(self):
        if not(self.in_game) or (self.in_game and self.play):
            pre = self.play
            self.play = False
            file_path = filedialog.askopenfilename(defaultextension=".Chs",
                                                    filetypes=[("Chess Game", "*.Chs")])
            self.play = pre
            if file_path:
                with open(file_path, 'r') as file:
                    data = load(file)
                if not self.in_game:
                    self.create_init_board()
                else: 
                    if self.with_moves.get() and self.can_save:
                        if messagebox.askyesno("Save Game", "Do you want to save the current game before creating a new one?"):
                            self.save_game()
                self.board.load_(
                    new_game=False,
                    board={int(key) : {int(key1) : value1 for key1 , value1 in value.items()} for key , value in data['board'].items()},
                    pre_in_game=data['pre_in_game'],
                    end_data=data['end_data'],
                    killed_pieces={'White' : {int(key) : value for key , value in data['kill']['White'].items()},'Black' : {int(key) : value for key , value in data['kill']['Black'].items()}},
                    dame_info=data['dame_info'],
                    history=data['history'],
                    turn=data['turn'],
                    custom_game=data['custom_game'],
                    in_game=data['in_game'],
                    end_game=data['end_game'],
                    dame_event=data['dame_event'],
                    event=data['event']
                )
                """( Board({int(key) : {int(key1) : value1 for key1 , value1 in value.items()} for key , value in data['board'].items()},
                            {'White' : {int(key) : value for key , value in data['kill']['White'].items()},
                                'Black' : {int(key) : value for key , value in data['kill']['Black'].items()}},
                            data['history'],
                            data['turn']))"""
                self.with_moves.set(True)
                self.current_time = data['time']
                self.play = True
                self.checked = False
                if not self.in_game:
                    self.in_game = True
                    self.begin_game()
                else :
                    self.create_board_begin()
                self.tests()
    
    def back(self):
        if self.with_moves.get() and self.can_save:
            if messagebox.askyesno("Save Game", "Do you want to save the current game before Back?"):
                self.save_game()
        self.in_game = False
        self.with_moves.set(False)
        self.menu_bar_config('disabled')
        self.game_frame.destroy()
        self.board.reset()
        del self.board
   
    def back_no_save(self):
        self.in_game = False
        self.with_moves.set(False)
        self.menu_bar_config('disabled')
        self.game_frame.destroy()
        self.board.reset()
        del self.board
    
    def create_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.show_history = tk.BooleanVar()
        self.show_kill = tk.BooleanVar()
        # Game menu
        self.game_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.game_menu.add_command(label="New Game", command=self.restart)
        self.game_menu.add_command(label="Load Game", command= self.load_game)
        self.game_menu.add_command(label="Save Game", command= self.save_game, state='disabled')
        self.game_menu.add_separator()
        self.game_menu.add_command(label="Settings", command=self.settings)
        self.game_menu.add_command(label="Back", command=self.back_no_save, state='disabled')
        self.game_menu.add_command(label="Back and Save", command=self.back, state='disabled')
        self.game_menu.add_separator()
        self.game_menu.add_command(label="Exit", command=self.exit)
        self.menu_bar.add_cascade(label="Game", menu=self.game_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.Undo)
        self.edit_menu.add_checkbutton(label="Show history", variable=self.show_history)
        self.edit_menu.add_checkbutton(label="Show token pieces", variable=self.show_kill)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu, state='disabled')

        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="Flip board", command=self.flip_board)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu, state='disabled')

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.help_menu.add_command(label="Documentation", command=self.documentation)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        
        # VARS
        self.show_history.set(True)
        self.show_kill.set(True)
        
        self.show_history.trace('w', self.show_history_and_kill_func)
        self.show_kill.trace('w', self.show_history_and_kill_func)
    
    def show_about(self):
        messagebox.showinfo("About", "Chess 2P - A chess game between 2 player\n\n      created by OUAZENE Abdelmohsen")
    
    def show_history_and_kill_func(self, *_):
        if not self.show_history.get():
            self.history.configure(state="normal")
            self.history.delete('0.0', 'end')
            self.history.configure(state="disabled")
        if not self.show_kill.get():
            self.kill.configure(state="normal")
            self.kill.delete('0.0', 'end')
            self.kill.configure(state="disabled")
        self.update_history()
    
    def Undo(self):
        self.board.Undo()
        for action in self.temp_images['actions']:
                self.canvas.delete(action)
        self.temp_images['actions'].clear()
        if len(self.board.history) == 0:
            if self.with_moves.get():
                self.with_moves.set(False)
        self.create_board()
        self.tests()
    
    def flip_board(self):
        self.flip = False if self.flip else True
        for action in self.temp_images['actions']:
                self.canvas.delete(action)
        self.temp_images['actions'].clear()
        self.create_board_begin()
        self.tests()
    
    def import_data(self):
        self.temp_images['background'] = ImageTk.PhotoImage(Image.open(self.data['background']).resize((self.data['min_height'], self.data['min_height'])))
        
        self.minsize(self.data['min_width'], self.data['min_height'])
        self.geometry(f'{self.winfo_width()}x{self.winfo_height()}')
        self.square_width = self.data['min_height'] // 8
        
        self.temp_images['squares'].clear()
        for item, value in self.data['squares'].items():
            if (item == 'black') and self.bsquare_color and not(self.themes_or_colors):
                self.temp_images['squares'][item] = ImageTk.PhotoImage(Image.new('RGB', (self.square_width, self.square_width), value))
            elif (item == 'white') and self.wsquare_color and not(self.themes_or_colors):
                self.temp_images['squares'][item] = ImageTk.PhotoImage(Image.new('RGB', (self.square_width, self.square_width), value))
            else :
                self.temp_images['squares'][item] = ImageTk.PhotoImage(Image.open(value).resize((self.square_width, self.square_width)))
        
        self.temp_images['pieces'].clear()
        self.temp_images['pieces']['White'] = {}
        for item, value in self.data['pieces']['White'].items():
            self.temp_images['pieces']['White'][item] = ImageTk.PhotoImage(Image.open(value).resize((self.square_width, self.square_width)))
        self.temp_images['pieces']['Black'] = {}
        for item, value in self.data['pieces']['Black'].items():
            self.temp_images['pieces']['Black'][item] = ImageTk.PhotoImage(Image.open(value).resize((self.square_width, self.square_width)))
    
    def create_board(self, op = True):
        if self.auto_flip and op:
            self.flip = True if self.board.turn == 'Black' else False
            self.create_board_begin(False)
        else :
            for piece in self.pieces.values():
                self.canvas.delete(piece)
            self.pieces.clear()
            for i in range(8, 0, -1):
                for j in range(1, 9):
                    if self.board[i, j]['name'] != None:
                        if not self.flip:
                            new_coor = ((j - 1) * self.square_width + (self.square_width // 2), (9 - i - 1) * self.square_width + (self.square_width // 2))
                        else :
                            new_coor = ((9 - j - 1) * self.square_width + (self.square_width // 2), (i - 1) * self.square_width + (self.square_width // 2))
                        self.pieces[f'{i}-{j}'] = self.canvas.create_image(new_coor, image=self.temp_images['pieces'][self.board[i, j]['color']][self.board[i, j]['name']], anchor='center')
            self.update_history()
    
    def create_board_begin(self, op = True):
        self.import_data()
        
        for square in self.squares.values():
            self.canvas.delete(square)
        self.squares.clear()
        self.squares['back'] = self.canvas.create_image((0, 0), image=self.temp_images['background'], anchor='nw')
        for i in range(8, 0, -1):
            for j in range(1, 9):
                if not self.flip:
                    new_coor = ((j - 1) * self.square_width, (9 - i - 1) * self.square_width)
                else :
                    new_coor = ((9 - j - 1) * self.square_width, (i - 1) * self.square_width)
                self.squares[f'{i}-{j}'] = self.canvas.create_image(new_coor, image=self.temp_images['squares']['white' if (i + j) % 2 == 1 else 'black' ], anchor='nw')
        
        for j in range(1, 9):
            self.squares[self.NUMTOALPHA[9 - j if self.flip else j]] = self.canvas.create_text(((j - 1) * self.square_width+ (self.square_width // 2), (8) * self.square_width), text=self.NUMTOALPHA[9 - j if self.flip else j], font=('Consolas', 12), fill=self.data['text_color'], anchor='s')
            self.squares[f'{9 - j if self.flip else j}'] = self.canvas.create_text((0, (9 - j - 1) * self.square_width+ (self.square_width // 2)), text=f'{9 - j if self.flip else j}', font=('Consolas', 12), fill=self.data['text_color'], anchor='w')
        self.create_board(op)
        
    def dame_select(self):
        def func(piece):
            self.sou_frame2.destroy()
            self.play = True
            self.board.dame_func(piece)
            self.create_board()
            self.tests()
            self.menu_bar_config('normal')
        self.sou_frame2 = ctk.CTkFrame(self.dame_turn, corner_radius=0, fg_color='black')
        self.sou_frame2.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.turn_label2 = ctk.CTkLabel(self.sou_frame2, text_color='white', fg_color='black',font=('Consolas', 17), text=f'Choose Piece')
        self.turn_label2.pack()
        
        self.info2 = ctk.CTkFrame(self.sou_frame2, corner_radius=0, fg_color='black')
        self.info2.pack(expand=True, fill='both')
        
        ctk.CTkButton(self.info2, command=lambda : func('Queen'), fg_color='black', bg_color='black', border_color='white', text_color='white',font=('Consolas', 15), hover_color='#333333', border_width=1, text='Queen').place(relx=0, y=0, relheight=1, relwidth=0.25, anchor='nw')
        ctk.CTkButton(self.info2, command=lambda : func('Rock'), fg_color='black', bg_color='black', border_color='white', text_color='white',font=('Consolas', 15), hover_color='#333333', border_width=1, text='Rock').place(relx=0.25, y=0, relheight=1, relwidth=0.25, anchor='nw')
        ctk.CTkButton(self.info2, command=lambda : func('Bishop'), fg_color='black', bg_color='black', border_color='white', text_color='white',font=('Consolas', 15), hover_color='#333333', border_width=1, text='Bishop').place(relx=0.5, y=0, relheight=1, relwidth=0.25, anchor='nw')
        ctk.CTkButton(self.info2, command=lambda : func('Knight'), fg_color='black', bg_color='black', border_color='white', text_color='white',font=('Consolas', 15), hover_color='#333333', border_width=1, text='Knight').place(relx=0.75, y=0, relheight=1, relwidth=0.25, anchor='nw')

    def tests(self):
        if self.board.end_game:
            self.play = False
            self.sound(self.data['sound']['checkmate'])
            for action in self.temp_images['actions']:
                self.canvas.delete(action)
            self.temp_images['actions'].clear()
            if self.board.end_data['mode'] == 'Draw':
                self.info.configure(text=f"Draw\n{self.board.end_data['info']}")
            elif self.board.end_data['info'] != 'Resign':
                self.info.configure(text=f"CheckMate\n{self.board.end_data['winner']} Win")
                if not self.flip:
                        new_coor = ((self.board.end_data['king_place'][1] - 1) * self.square_width, (9 - self.board.end_data['king_place'][0] - 1) * self.square_width)
                else :
                        new_coor = ((9 - self.board.end_data['king_place'][1] - 1) * self.square_width, (self.board.end_data['king_place'][0] - 1) * self.square_width)
                self.temp_images['actions'].append(self.canvas.create_image(new_coor, image=self.temp_images['squares']['Check'], anchor='nw'))
                if f"{self.board.end_data['king_place'][0]}-{self.board.end_data['king_place'][1]}" in self.pieces.keys():
                    self.canvas.tag_raise(self.pieces[f"{self.board.end_data['king_place'][0]}-{self.board.end_data['king_place'][1]}"])
                Tboard = SubBoard()
                Tboard._copy_(self.board.board)
                self.temp_images['CheckMate'].clear()
                for coor in self.board.get_check_pieces(Tboard, 'Black' if self.board.end_data['winner'] == 'White' else 'White'):
                    if not self.flip:
                            new_coor = ((coor[1] - 1) * self.square_width, (9 - coor[0] - 1) * self.square_width)
                    else :
                            new_coor = ((9 - coor[1] - 1) * self.square_width, (coor[0] - 1) * self.square_width)
                    self.temp_images['CheckMate'].append(self.canvas.create_image(new_coor, image=self.temp_images['squares']['Red'], anchor='nw'))
                    if f"{coor[0]}-{coor[1]}" in self.pieces.keys():
                        self.canvas.tag_raise(self.pieces[f"{coor[0]}-{coor[1]}"])
            else :
                self.info.configure(text=f"Resign\n{self.board.end_data['winner']} Win")
        elif self.board.event:
            if not self.checked:
                self.sound(self.data['sound']['check'])
            self.checked = True
            if not self.flip:
                    new_coor = ((self.board.end_data['king_place'][1] - 1) * self.square_width, (9 - self.board.end_data['king_place'][0] - 1) * self.square_width)
            else :
                    new_coor = ((9 - self.board.end_data['king_place'][1] - 1) * self.square_width, (self.board.end_data['king_place'][0] - 1) * self.square_width)
            self.temp_images['actions'].append(self.canvas.create_image(new_coor, image=self.temp_images['squares']['Check'], anchor='nw'))
            if f"{self.board.end_data['king_place'][0]}-{self.board.end_data['king_place'][1]}" in self.pieces.keys():
                self.canvas.tag_raise(self.pieces[f"{self.board.end_data['king_place'][0]}-{self.board.end_data['king_place'][1]}"])
            self.info.configure(text=f"Check\nIn {'Black' if self.board.end_data['winner'] == 'White' else 'White'} King")
        else :
            self.checked = False
            self.info.configure(text='')

    def click(self, event):
        if self.play:
            i = 9 - ((event.y // self.square_width) + 1)
            j = (event.x // self.square_width) + 1
            if self.flip:
                i = 9 - i
                j = 9 - j
            if (1 <= i <= 8) and (1 <= j <= 8):
                for action in self.temp_images['actions']:
                    self.canvas.delete(action)
                self.temp_images['actions'].clear()
                actions : list = self.board.choose_square((i, j))
                if actions:
                    cpt = 0
                    for action in actions:
                        if action[0] == 'Move':
                            cpt += 1
                    for action in actions:
                        if action[0] in ('Yellow', 'Blue', 'Red', 'Purple'):
                            if not self.flip:
                                new_coor = ((action[1][1] - 1) * self.square_width, (9 - action[1][0] - 1) * self.square_width)
                            else :
                                new_coor = ((9 - action[1][1] - 1) * self.square_width, (action[1][0] - 1) * self.square_width)
                            self.temp_images['actions'].append(self.canvas.create_image(new_coor, image=self.temp_images['squares'][action[0]], anchor='nw'))
                            if f'{action[1][0]}-{action[1][1]}' in self.pieces.keys():
                                self.canvas.tag_raise(self.pieces[f'{action[1][0]}-{action[1][1]}'])
                        elif action[0] == 'Move':
                            if not self.with_moves.get():
                                self.with_moves.set(True)
                            self.canvas.tag_raise(self.pieces[f'{action[1][0]}-{action[1][1]}'])
                            speedX = action[2][1] - action[1][1]
                            speedY = -(action[2][0] - action[1][0])
                            if self.flip:
                                speedX *= -1
                                speedY *= -1
                            self.sound(self.data['sound']['move'])
                            for z in range(self.square_width):
                                self.canvas.move(self.pieces[f'{action[1][0]}-{action[1][1]}'],speedX,speedY)
                                self.update()
                                time.sleep(self.square_width/50000)
                            if cpt == 2:
                                cpt = 1
                            elif not(self.board.dame_event):
                                self.create_board()
                            else :
                                if f'{action[2][0]}-{action[2][1]}' in self.pieces.keys():
                                    self.canvas.delete(self.pieces[f'{action[2][0]}-{action[2][1]}'])
                        elif action[0] == 'Dame':
                            self.menu_bar_config('disabled')
                            self.play = False
                            self.dame_select()
                self.tests()
                #self.board.write(True)
    
    def update_history(self):
        if self.show_history.get():
            self.history.configure(state="normal")
            self.history.delete('0.0', 'end')
            for num, journney in enumerate(self.board.history):
                text = f"{self.NUMTOALPHA[journney[1][1]]}{journney[1][0]} - {self.NUMTOALPHA[journney[2][1]]}{journney[2][0]}"
                if (journney[0] == 'king_rock'):
                    if (journney[3][1] == 1):
                        text = "O-O-O"
                    else :
                        text = "O-O"
                if num % 2 == 0:
                    self.history.insert('end', text=f"{num // 2 + 1}# {text}\n")
                else :
                    self.history.insert('end', text=f"       {text}\n")
            self.history.configure(state="disabled")
        if self.show_kill.get():
            self.kill.configure(state="normal")
            self.kill.delete('0.0', 'end')
            if self.board.killed_pieces['White'] != {}:
                self.kill.insert('end', text="White lose:\n")
                for value in self.board.killed_pieces['White'].values():
                    self.kill.insert('end', text=f"   {value['name']}\n")
            if self.board.killed_pieces['Black'] != {}:
                self.kill.insert('end', text="Black lose:\n")
                for value in self.board.killed_pieces['Black'].values():
                    self.kill.insert('end', text=f"   {value['name']}\n")
            self.kill.configure(state="disabled")
        white_point = 0
        black_point = 0
        for i in range(1, 9):
            for j in range(1, 9):
                if not(self.board[i, j]['name'] in (None, 'King')):
                    if self.board[i, j]['color'] == 'White':
                        white_point += self.POINTS[self.board[i, j]['name']]
                    else :
                        black_point += self.POINTS[self.board[i, j]['name']]
        if white_point == black_point:
            self.white_score.configure(text='')
            self.black_score.configure(text='')
        elif white_point > black_point:
            self.white_score.configure(text=f'+{white_point-black_point}')
            self.black_score.configure(text='')
        else :
            self.white_score.configure(text='')
            self.black_score.configure(text=f'+{black_point-white_point}')
        self.turn_label.configure(text=f'{self.board.turn} turn')
    
    def update_time(self):
        if self.in_game and self.play and self.with_moves.get():
            self.current_time += 1
            sec = self.current_time % 60
            min_ = (self.current_time // 60) % 60
            h = ((self.current_time // 60) // 60) % 24
            d = ((self.current_time // 60) // 60) // 24
            text = ''
            if d != 0:
                text += f'{d} day '
            if h != 0:
                text += f'{h:02}:{min_:02}:{sec:02}'
            elif min_ != 0:
                text += f'{min_:02}:{sec:02}'
            else :
                text += f'{sec:02}'
            self.time.configure(text=text)
        self.players_data_frame.after(1000, self.update_time)
    
    def create_widgets(self):
        width = self.data['width'] - self.data['min_height']
        height = self.data['min_height']
        self.history_frame = ctk.CTkFrame(self.game_frame, width=width, height=height // 2, corner_radius=0, border_color='white', bg_color='transparent', border_width=2)
        self.history_frame.place(x=height, y=height // 2)
        self.history = ctk.CTkTextbox(self.history_frame, width=width // 2, height=height // 2, border_color='white', border_width=1, corner_radius=0, font=('Consolas', 15), text_color='white', bg_color='transparent', fg_color='black')
        self.history.place(x=0, y=0)
        self.history.configure(state="disabled")
        self.kill = ctk.CTkTextbox(self.history_frame, width=width // 2, height=height // 2, border_color='white', border_width=1, corner_radius=0, font=('Consolas', 15), text_color='white', bg_color='transparent', fg_color='black')
        self.kill.place(x=width // 2, y=0)
        self.kill.configure(state="disabled")
        self.players_data_frame = ctk.CTkFrame(self.game_frame, width=width, height=height // 4, corner_radius=0, border_color='white', fg_color='black', border_width=2)
        self.players_data_frame.place(x=height, y=0)
        
        self.white_ = ctk.CTkFrame(self.players_data_frame, corner_radius=0, fg_color='black')
        self.white_.place(x=0, y=0, relwidth=0.5, relheight=1)
        self.white = ctk.CTkFrame(self.white_, corner_radius=0, fg_color='black')
        self.white.pack(expand=True)
        ctk.CTkLabel(self.white, text_color='white', fg_color='black', text='White' ,font=('Consolas', 25)).pack(pady=1)
        self.white_score = ctk.CTkLabel(self.white, text_color='white', fg_color='black',font=('Consolas', 15), text='')
        self.white_score.pack(pady=1)
        
        self.black_ = ctk.CTkFrame(self.players_data_frame, corner_radius=0, fg_color='black')
        self.black_.place(relx=0.5, y=0, relwidth=0.5, relheight=1)
        self.black = ctk.CTkFrame(self.black_, corner_radius=0, fg_color='black')
        self.black.pack(expand=True)
        ctk.CTkLabel(self.black, text_color='white', fg_color='black', text='Black' ,font=('Consolas', 25)).pack(pady=1)
        self.black_score = ctk.CTkLabel(self.black, text_color='white', fg_color='black',font=('Consolas', 15), text='')
        self.black_score.pack(pady=1)
        
        self.time = ctk.CTkLabel(self.players_data_frame, text_color='white', fg_color='black',font=('Consolas', 17), text='00')
        self.time.place(relx=0.5, rely=0.1, anchor='n')
        ctk.CTkButton(self.players_data_frame, command=self.resign, fg_color='black', bg_color='black', border_color='white', text_color='white',font=('Consolas', 15), hover_color='#333333', border_width=1, text='Resign').place(relx=0.5, rely=0.7, anchor='s')
        ctk.CTkButton(self.players_data_frame, command=self.draw, fg_color='black', bg_color='black', border_color='white', text_color='white',font=('Consolas', 15), hover_color='#333333', border_width=1, text='Draw').place(relx=0.5, rely=0.9, anchor='s')
        
        self.update_time()
        
        self.dame_turn = ctk.CTkFrame(self.game_frame, width=width, height=height // 4, corner_radius=0, border_color='white', fg_color='black', border_width=2)
        self.dame_turn.place(x=height, y=height // 4)
        self.sou_frame = ctk.CTkFrame(self.dame_turn, corner_radius=0, fg_color='black')
        self.sou_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.turn_label = ctk.CTkLabel(self.sou_frame, text_color='white', fg_color='black',font=('Consolas', 17), text=f'{self.board.turn} turn')
        self.turn_label.pack()
        
        self.info = ctk.CTkLabel(self.sou_frame, text_color='white', fg_color='black',font=('Consolas', 17), text=f'')
        self.info.pack(expand=True)
    
    def draw(self):
        if self.play and self.with_moves.get():
            self.board.end_game = True
            self.board.end_data['mode'] = 'Draw'
            self.board.end_data['info'] = 'Cancel'
            self.tests()
    
    def resign(self):
        if self.play and self.with_moves.get():
            color = self.board.turn
            self.board.end_game = True
            self.board.end_data['mode'] = 'CheckMate'
            self.board.end_data['winner'] = 'White' if color == 'Black' else 'Black'
            self.board.end_data['info'] = 'Resign'
            self.tests()
    
    def begin_game(self):
        self.game_frame = ctk.CTkFrame(self, corner_radius=0, border_width=0, fg_color='transparent')
        self.game_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.canvas = ctk.CTkCanvas(self.game_frame, width= self.data['min_height'], height=self.data["min_height"], highlightthickness=0)
        self.canvas.place(x=0, y=0)
        
        self.create_widgets()
        
        self.create_board_begin()
        
        self.play = True

        self.menu_bar_config('normal')
        
        self.canvas.bind('<Button-1>', self.click)
        
    def menu_bar_config(self, mode):
        self.menu_bar.entryconfig("Edit",state=mode)
        self.menu_bar.entryconfig("View",state=mode)
        if self.with_moves.get():
            self.game_menu.entryconfig("Save Game",state=mode)
            self.game_menu.entryconfig("Back and Save",state=mode)
            if mode == 'normal':
                self.can_save = True
            else :
                self.can_save = False
        self.game_menu.entryconfig("Back",state=mode)

    def exit(self):
        if self.in_game and self.with_moves.get() and self.can_save:
            if messagebox.askyesno("Save Game", "Do you want to save the current game before exit?"):
                self.save_game()
        super().destroy()
    
    def destroy(self):
        self.exit()

class SubBoard:
    def __init__(self) -> None:
        self.board = {}
        
    def _reset_(self):
        self.board.clear()
    
    def __getitem__(self, args : tuple):
        return self.board[args[0]][args[1]]
    
    def _set_(self, pos, data):
        self.board[pos[0]][pos[1]] = data
    
    def _copy_(self, data):
        self._reset_()
        self.board = deepcopy(data)

class Board:
    def __init__(self, new_game = True, board = None, pre_in_game = [], end_data = None, killed_pieces = None, dame_info = None, history = None, turn = 'White', custom_game = False, in_game = True, end_game = False, dame_event = False, event = False) -> None:
        
        # CONST
        self.VOID = {
                    'name' : None,
                    'color' : None, # Black or White
                    'option' : None # Can, Imp, wait
                }
        self.ENDVOID = {
            'mode' : None,
            'winner' : None,
            'king_place' : None,
            'info' : None
        }
        self.PATTERN = {
            'Rock' : [[0,1],[1,0],[0,-1],[-1,0]],
            'Knight' : [[2,1],[1,2],[-1,2],[2,-1],[1,-2],[-2,1],[-1,-2],[-2,-1]],
            'Bishop' : [[1,1],[1,-1],[-1,-1],[-1,1]],
            'Queen' : [[1,1],[1,-1],[-1,-1],[-1,1],[0,1],[1,0],[0,-1],[-1,0]],
            'King' : [[1,1],[1,-1],[-1,-1],[-1,1],[0,1],[1,0],[0,-1],[-1,0]]
        }
        
        self.board = {}
        self.killed_pieces = {}
        self.history = []
        # VAR
        self.load_(new_game ,board, pre_in_game, end_data, killed_pieces, dame_info, history, turn, custom_game, in_game, end_game, dame_event, event)
    
    def load_(self, new_game = True, board = None, pre_in_game = [], end_data = None, killed_pieces = None, dame_info = None, history = None, turn = 'White', custom_game = False, in_game = True, end_game = False, dame_event = False, event = False):
        if new_game:
            self.turn = turn
            self.custom_game = custom_game
            self.in_game = True
            self.end_game = False
            self.event = False
            self.dame_event = False
            self.dame_info = None
            self.end_data = deepcopy(self.ENDVOID)
            self.pre_in_game = []
            self.current_choosen = []
            if board == None:
                self.board.clear()
                for i in range(1, 9):
                    self.board[i] = {}
                    for j in range(1, 9):
                        self.board[i][j] = deepcopy(self.VOID)
                for i in range(1, 9):
                    self[1,i]['color'] = 'White'
                    self[2,i]['color'] = 'White'
                    self[7,i]['color'] = 'Black'
                    self[8,i]['color'] = 'Black'
                    self[2,i]['name'] = 'Pawn'
                    self[7,i]['name'] = 'Pawn'
                    self[2,i]['option'] = 'Wait'
                    self[7,i]['option'] = 'Wait'
                    if (i == 1) or (i == 8):
                        self[1,i]['name'] = 'Rock'
                        self[8,i]['name'] = 'Rock'
                        self[1,i]['option'] = 'Can'
                        self[8,i]['option'] = 'Can'
                    elif (i == 2) or (i == 7):
                        self[1,i]['name'] = 'Knight'
                        self[8,i]['name'] = 'Knight'
                    elif (i == 3) or (i == 6):
                        self[1,i]['name'] = 'Bishop'
                        self[8,i]['name'] = 'Bishop'
                    elif i == 4: 
                        self[1,i]['name'] = 'Queen'
                        self[8,i]['name'] = 'Queen'
                    else :
                        self[1,i]['name'] = 'King'
                        self[8,i]['name'] = 'King'
                        self[1,i]['option'] = 'Can'
                        self[8,i]['option'] = 'Can'
                self.killed_pieces.clear()
                self.killed_pieces = {
                    'Black' : {},
                    'White' : {}
                }
                self.history.clear()
            else :
                self.board = board
                self.killed_pieces = killed_pieces
                self.history = history
        else :
            self.turn = turn
            self.custom_game = custom_game
            self.in_game = in_game
            self.end_game = end_game
            self.event = event
            self.dame_event = dame_event
            self.dame_info = dame_info
            if end_data:
                self.end_data = end_data
            else :
                self.end_data = deepcopy(self.ENDVOID)
            self.pre_in_game = pre_in_game
            self.current_choosen = []
            self.board.clear()
            self.killed_pieces.clear()
            self.history.clear()
            self.board = board
            self.killed_pieces = killed_pieces
            self.history = history
    
    def dame_func(self, new_piece):
        self.select_dame_peice(self.dame_info[0], self.dame_info[1], new_piece)
        self.dame_event = False
        self.dame_info = None
    
    def __getitem__(self, args : tuple):
        return self.board[args[0]][args[1]]

    def write(self, op = False):
        for i in range(8, 0, -1):
            for j in range(1, 9):
                print(f"{self[i, j]['name'] + '_' + self[i, j]['color'][0] + (self[i, j]['option'][0] if self[i, j]['option'] != None else '') if self[i, j]['name'] != None else 'None':10}", end='   ')
            print()
        if op:
            print('History :')
            for id_, item in enumerate(self.history):
                print(id_, item)
            print('Killed :')
            print('  White :')
            for item, value in self.killed_pieces['White'].items():
                print('   ',item, value)
            print('  Black :')
            for item, value in self.killed_pieces['Black'].items():
                print('   ',item, value)
        print()
    
    def _set_(self, pos, data):
        self.board[pos[0]][pos[1]] = data
    
    # in history pawn option after move
    def move(self, pos1, pos2, kill= True, history = True):
        if history:
            if self[pos2]['name'] == None:
                self.history.append(['normal', pos1, pos2, self[pos1]['option']])
                if (self[pos1]['name'] == 'King') or (self[pos1]['name'] == 'Rock') or ((self[pos1]['name'] == 'Pawn') and ((pos2[0] > 5) and (self.turn == 'White')) or ((pos2[0] < 4) and (self.turn == 'Black'))):
                    self[pos1]['option'] = 'Imp'
            else :
                self.history.append(['kill', pos1, pos2, self[pos1]['option']])
                if (self[pos1]['name'] == 'Pawn') or (self[pos1]['name'] == 'King') or (self[pos1]['name'] == 'Rock'):
                    self[pos1]['option'] = 'Imp'
        if kill:
            if self[pos2]['name'] != None:
                self.killed_pieces[self[pos2]['color']][len(self.history)-1] = self[pos2]
        self._set_(pos2, self[pos1])
        self._set_(pos1, deepcopy(self.VOID))
        
    def move_king_rock(self, pos1_king, pos2_king, pos1_rock, pos2_rock, history = True):
        if history:
            self.history.append(['king_rock', pos1_king, pos2_king, pos1_rock, pos2_rock])
        self.move(pos1_king, pos2_king, False, False)
        self.move(pos1_rock, pos2_rock, False, False)
        if history:
            self[pos2_king]['option'] = 'Imp'
            self[pos2_rock]['option'] = 'Imp'
        
    def move_pawn_in_midle(self, pos1, pos2, pos_of_enemy):
        self.history.append(['pawn_center', pos1, pos2, pos_of_enemy])
        self.killed_pieces[self[pos_of_enemy]['color']][len(self.history)-1] = self[pos_of_enemy]
        self.move(pos1, pos2, False, False)
        self[pos2]['option'] = 'Imp'
        self._set_(pos_of_enemy, deepcopy(self.VOID))
        
    def move_pawn_dame(self, pos1, pos2, new_piece):
        self.history.append(['dame', pos1, pos2, new_piece])
        self.move(pos1, pos2, True, False)
        self[pos2]['name'] = new_piece
        self[pos2]['option'] = None
        
    def Undo(self):
        if not(self.end_game) and self.in_game:
            if len(self.history) > 0:
                self.current_choosen.clear()
                self.turn = 'White' if self.turn == 'Black' else 'Black'
                current_move = self.history.pop()
                if (current_move[0] == 'kill') or (current_move[0] == 'pawn_center') or (current_move[0] == 'dame'):
                    if len(self.history) in self.killed_pieces['Black']:
                        killed_piece = self.killed_pieces['Black'].pop(len(self.history))
                    elif len(self.history) in self.killed_pieces['White']:
                        killed_piece = self.killed_pieces['White'].pop(len(self.history))
                    else :
                        killed_piece = None
                taille = 4
                match current_move[0]:
                    case 'normal':
                        self.move(current_move[2], current_move[1], False, False)
                        self[current_move[1]]['option'] = current_move[3]
                    case 'kill':
                        self.move(current_move[2], current_move[1], False, False)
                        self._set_(current_move[2], killed_piece)
                        self[current_move[1]]['option'] = current_move[3]
                    case 'king_rock':
                        self.move_king_rock(current_move[2], current_move[1], current_move[4], current_move[3], False)
                        self[current_move[1]]['option'] = 'Can'
                        self[current_move[3]]['option'] = 'Can'
                        taille += 1
                    case 'pawn_center':
                        self.move(current_move[2], current_move[1], False, False)
                        self._set_(current_move[3], killed_piece)
                        self[current_move[1]]['option'] = 'Can'
                    case 'dame':
                        self.move(current_move[2], current_move[1], False, False)
                        if killed_piece:
                            self._set_(current_move[2], killed_piece)
                        self[current_move[1]]['name'] = 'Pawn'
                        self[current_move[1]]['option'] = 'Imp'
                if len(current_move) > taille:
                    self[current_move[-1]]['option'] = current_move[-2]
                self.tests()
    
    def select_piece_(self, pos, turn, board_ : SubBoard):
        peice = board_[pos]
        moves = []
        Tboard = SubBoard()
        if peice['name'] in ('Rock', 'Bishop', 'Queen'):
            for position in self.PATTERN[peice['name']]:
                i = 1
                while True:
                    if pos[0]+position[0]*i>8 or pos[0]+position[0]*i<1 or pos[1]+position[1]*i>8 or pos[1]+position[1]*i<1:
                        break
                    elif board_[pos[0]+position[0]*i, pos[1]+position[1]*i]['color'] == turn:
                        break
                    elif board_[pos[0]+position[0]*i, pos[1]+position[1]*i]['name'] != None:
                        moves.append(['Red', (pos[0]+position[0]*i, pos[1]+position[1]*i)])
                        break
                    else :
                        moves.append(['Blue', (pos[0]+position[0]*i, pos[1]+position[1]*i)])
                        i += 1
        elif peice['name'] in ('King', 'Knight'):
            for position in self.PATTERN[peice['name']]:
                if pos[0]+position[0]>8 or pos[0]+position[0]<1 or pos[1]+position[1]>8 or pos[1]+position[1]<1:
                    continue
                elif board_[pos[0]+position[0], pos[1]+position[1]]['color'] == turn:
                    continue
                elif board_[pos[0]+position[0], pos[1]+position[1]]['name'] != None:
                    moves.append(['Red', (pos[0]+position[0], pos[1]+position[1])])
                else :
                    moves.append(['Blue', (pos[0]+position[0], pos[1]+position[1])])
            if (peice['name'] == 'King') and (peice['option'] == 'Can'):
                if not self.check(board_, turn):
                    if (board_[pos[0],8]['name'] == 'Rock') and (board_[pos[0],8]['option'] == 'Can') and (board_[pos[0],6]['name'] == None) and (board_[pos[0],7]['name'] == None):
                        m = [6, 7]
                        op = True
                        for i in m:
                            Tboard._copy_(board_.board)
                            Tboard[pos[0],5].clear()
                            Tboard._set_((pos[0],5), deepcopy(self.VOID))
                            Tboard[pos[0],i].clear()
                            Tboard._set_((pos[0],i) , {'name':'King', 'color': turn, 'option':'Imp'})
                            if self.check(Tboard,turn):
                                op = False
                        if op:
                            moves.append(['Purple',(pos[0],7)])
                    if (board_[pos[0],1]['name'] == 'Rock') and (board_[pos[0],1]['option'] == 'Can') and (board_[pos[0],4]['name'] == None) and (board_[pos[0],3]['name'] == None) and (board_[pos[0],2]['name'] == None):
                        m = [2, 3, 4]
                        op = True
                        for i in m:
                            Tboard._copy_(board_.board)
                            Tboard[pos[0],5].clear()
                            Tboard._set_((pos[0],5), deepcopy(self.VOID))
                            Tboard[pos[0],i].clear()
                            Tboard._set_((pos[0],i) , {'name':'King', 'color': turn, 'option':'Imp'})
                            if self.check(Tboard,turn):
                                op = False
                        if op:
                            moves.append(['Purple',(pos[0],3)])
        else : # Pawn
            if turn == 'White':
                step = 1
                event_line = 5
                dame_line = 8
            else :
                event_line = 4
                step = -1
                dame_line = 1
            if 1 <= (pos[0] + step) <= 8:
                if board_[pos[0]+step, pos[1]]['name'] == None:
                    moves.append(['Blue', (pos[0]+step, pos[1])])
                    if ((pos[0] == 2) and (turn=='White')) or ((pos[0] == 7) and (turn=='Black')) :
                        if board_[pos[0]+2*step, pos[1]]['name'] == None:
                            moves.append(['Blue', (pos[0]+2*step, pos[1])])
                if pos[1] + 1 <= 8:
                    if not(board_[pos[0]+step, pos[1]+1]['color'] in (None,turn)):
                        moves.append(['Red',(pos[0]+step,pos[1]+1)])
                    elif (pos[0] == event_line) and (not(board_[pos[0], pos[1]+1]['color'] in (None,turn))) and (board_[pos[0]+step, pos[1]+1]['name'] == None) and (board_[pos[0], pos[1]+1]['name'] == 'Pawn') and (board_[pos[0], pos[1]+1]['option'] == 'Wait') and (board_[pos]['option'] == 'Can'):
                        moves.append(['Purple',(pos[0]+step,pos[1]+1)])
                if pos[1] - 1 >= 1:
                    if not(board_[pos[0]+step, pos[1]-1]['color'] in (None,turn)):
                        moves.append(['Red',(pos[0]+step,pos[1]-1)])
                    elif (pos[0] == event_line) and (not(board_[pos[0], pos[1]-1]['color'] in (None,turn))) and (board_[pos[0]+step, pos[1]-1]['name'] == None) and (board_[pos[0], pos[1]-1]['name'] == 'Pawn') and (board_[pos[0], pos[1]-1]['option'] == 'Wait') and (board_[pos]['option'] == 'Can'):
                        moves.append(['Purple',(pos[0]+step,pos[1]-1)])
                for move in moves:
                    if move[1][0] == dame_line:
                        move[0] = 'Purple'
        return moves
    
    def select_piece(self, pos, turn, board_ : SubBoard):
        moves = self.select_piece_(pos, turn, board_)
        Tboard = SubBoard()
        moves_temp = deepcopy(moves)
        for move in moves_temp:
            Tboard._copy_(board_.board)
            self.psudo_move(Tboard,turn,pos,move[1], move[0])
            if self.check(Tboard,turn):
                moves.remove(move)
            Tboard._reset_()
        return moves
           
    def no_move_centre(self, board_ : SubBoard, turn, op = False):
        i = 4 if turn == 'White' else 5
        for j in range(1, 9):
            if (board_[i, j]['name'] == 'Pawn') and (board_[i, j]['color'] == turn) and (board_[i, j]['option'] == 'Wait'):
                board_[i, j]['option'] = 'Can'
                if op:
                    self.history[-1].append('Wait')
                    self.history[-1].append((i, j))
            
    def psudo_move(self, board_ : SubBoard, turn, old_pos, new_pos, mode):
        temp = board_[old_pos]
        if (temp['name'] == 'King') or (temp['name'] == 'Rock') or ((temp['name'] == 'Pawn') and ((mode == 'Red') or (mode == 'Purple') or ((new_pos[0] > 5) and (turn == 'White')) or ((new_pos[0] < 4) and (turn == 'Black')))):
            temp['option'] = 'Imp'
        self.no_move_centre(board_, 'White' if turn=='Black' else 'Black')
        if mode == 'Purple':
            if (temp['name'] == 'Pawn') and (((turn == 'White') and (old_pos[0] == 5)) or ((turn == 'Black') and (old_pos[0] == 4))):
                board_._set_((old_pos[0], new_pos[1]), deepcopy(self.VOID))
            else :
                if new_pos[1] == 7:
                    rock_position = (old_pos[0],8)
                    new_rock_position = (old_pos[0],6)
                else :
                    rock_position = (old_pos[0],1)
                    new_rock_position = (old_pos[0],4)
                self.psudo_move(board_,turn,rock_position,new_rock_position, 'Blue')
        board_._set_(new_pos, temp)
        board_._set_(old_pos, deepcopy(self.VOID))
    
    def tests(self):
        self.no_move_centre(self, self.turn, True)
        Tboard = SubBoard()
        Tboard._copy_(self.board)
        data_ = self.get_check_or_draw_or_ckeckmate(Tboard, self.turn)
        match data_[0]:
            case 'CheckMate':
                self.end_game = True
                self.event = True
                self.end_data['mode'] = 'CheckMate'
                self.end_data['winner'] = 'White' if self.turn == 'Black' else 'Black'
                c = False
                for i in range(1,9):
                    for j in range(1,9):
                        if (self[i,j]['name'] == 'King') and (self[i,j]['color'] == self.turn):
                            king_place = (i,j)
                            c=True
                            break
                    if c==True:
                        break
                self.end_data['king_place'] = king_place
            case 'Check':
                self.event = True
                self.end_data['mode'] = 'Check'
                self.end_data['winner'] = 'White' if self.turn == 'Black' else 'Black'
                c = False
                for i in range(1,9):
                    for j in range(1,9):
                        if (self[i,j]['name'] == 'King') and (self[i,j]['color'] == self.turn):
                            king_place = (i,j)
                            c=True
                            break
                    if c==True:
                        break
                self.end_data['king_place'] = king_place
            case 'Draw':
                self.end_game = True
                self.event = True
                self.end_data['mode'] = 'Draw'
                self.end_data['info'] = data_[1]
            case _:
                self.end_data.clear()
                self.event = False
                self.end_data = deepcopy(self.ENDVOID)
        Tboard._reset_()
    
    def select_dame_peice(self, pos1, pos2, new_piece):
        self.move_pawn_dame(pos1, pos2, new_piece)
        self.in_game = self.pre_in_game.pop()
        self.turn = 'White' if self.turn == 'Black' else 'Black'
        self.tests()
    
    def choose_square(self, pos):
        if not self.end_game:
            if not self.dame_event:
                if self.in_game:
                    if ((self.current_choosen != []) and (self.current_choosen[0][1] == pos)):
                        self.current_choosen.clear()
                    else :
                        tr = False
                        if self.current_choosen != []:
                            for item in self.current_choosen[1]:
                                if pos == item[1]:
                                    piece = deepcopy(self.current_choosen[0])
                                    move = deepcopy(item)
                                    tr = True
                                    break
                            self.current_choosen.clear()
                        if not tr:
                            moves = [['Yellow', pos]]
                            if self[pos]['color'] == self.turn:
                                Tboard = SubBoard()
                                Tboard._copy_(self.board)
                                moves.extend(self.select_piece(pos, self.turn, Tboard))
                                self.current_choosen.append([self[pos], pos])
                                self.current_choosen.append(moves)
                                return moves
                            else :
                                self.current_choosen.append([None, pos])
                                self.current_choosen.append(moves)
                                return moves
                        else :
                            match move[0]:
                                case 'Blue':
                                    self.move(piece[1], pos)
                                    self.turn = 'White' if self.turn == 'Black' else 'Black'
                                    self.tests()
                                    return [['Move',piece[1] ,pos]]
                                case 'Red':
                                    self.move(piece[1], pos)
                                    self.turn = 'White' if self.turn == 'Black' else 'Black'
                                    self.tests()
                                    return [['Move',piece[1] ,pos]]
                                case 'Purple':
                                    if piece[0]['name'] == 'King':
                                        self.move_king_rock(piece[1], pos, (pos[0], 8 if pos[1] == 7 else 1), (pos[0], 6 if pos[1] == 7 else 4))
                                        self.turn = 'White' if self.turn == 'Black' else 'Black'
                                        self.tests()
                                        return [['Move',piece[1] ,pos], ['Move', (pos[0], 8 if pos[1] == 7 else 1), (pos[0], 6 if pos[1] == 7 else 4)]]
                                    else :
                                        if ((piece[1][0] == 5) and (self.turn == 'White')) or ((piece[1][0] == 4) and (self.turn == 'Black')):
                                            self.move_pawn_in_midle(piece[1], pos, (piece[1][0], pos[1]))
                                            self.turn = 'White' if self.turn == 'Black' else 'Black'
                                            self.tests()
                                            return [['Move',piece[1] ,pos]]
                                        else :
                                            self.pre_in_game.append(self.in_game)
                                            self.in_game = False
                                            self.end_game = False
                                            self.event = False
                                            self.dame_event = True
                                            self.dame_info = [piece[1], pos]
                                            return [['Move',piece[1] ,pos], ['Dame', pos]]
    
    def check(self, board_ : SubBoard, turn) -> bool:
        check = False
        c = False
        for i in range(1,9):
            for j in range(1,9):
                if (board_[i,j]['name'] == 'King') and (board_[i,j]['color'] == turn):
                    king_place = (i,j)
                    c=True
                    break
            if c==True:
                break
        for i in range(1, 9):
            for j in range(1, 9):
                if not(board_[i,j]['color'] in [turn , None]):
                    if (board_[i,j]['name'] == 'King') and (board_[i,j]['option'] == 'Can') and (board_[king_place]['option'] == 'Can'):
                        continue
                    moves = self.select_piece_((i, j), 'White' if turn=='Black' else 'Black', board_)
                    for move in moves:
                        if move[1] == king_place :
                            check = True
                            break
                    if check:
                        break
            if check:
                break
        return check
    
    def get_check_pieces(self, board_2 : SubBoard, turn) -> list:
        c = False
        for i in range(1,9):
            for j in range(1,9):
                if (board_2[i,j]['name'] == 'King') and (board_2[i,j]['color'] == turn):
                    king_place_ = (i,j)
                    c=True
                    break
            if c==True:
                break
        moves = self.select_piece_(king_place_, turn, board_2)
        moves.append([None ,king_place_])
        pieces = []
        board_ = SubBoard()
        for move in moves:
            king_place = move[1]
            board_._reset_()
            board_._copy_(board_2.board)
            if king_place != king_place_:
                self.psudo_move(board_, turn, king_place_, king_place, move[0])
            for i in range(1, 9):
                for j in range(1, 9):
                    if not(board_[i,j]['color'] in [turn , None]):
                        if (board_[i,j]['name'] == 'King') and (board_[i,j]['option'] == 'Can') and (board_[king_place]['option'] == 'Can'):
                            continue
                        moves = self.select_piece_((i, j), 'White' if turn=='Black' else 'Black', board_)
                        for move in moves:
                            if move[1] == king_place :
                                pieces.append((i, j))
                                break
        return pieces
    
    def draw(self, board_ : SubBoard,turn):
        draw = True
        for i in range(1,9):
            for j in range(1,9):
                if board_[i, j]['color'] == turn:
                    moves = self.select_piece((i,j),turn,board_)
                    if moves:
                        draw = False
                        break
            if draw == False:
                break
        if draw:
            return True, 'normal'
        else :
            if len(self.history) >= 12:
                for i in range(1, 4):
                    if self.history[-i] == self.history[-i-4] == self.history[-i-8]:
                        return True, 'repeat'
            cpt = 0
            for i in range(1, 9):
                for j in range(1, 9):
                    if self[i, j]['name'] != None:
                        cpt += 1
            if not(self.custom_game) and (cpt == 2):
                return True, 'kings'
            else :
                return False, None

    def get_check_or_draw_or_ckeckmate(self, board_ : SubBoard, turn):
        draw, draw_data = self.draw(board_, turn)
        check = self.check(board_, turn)
        if check and draw:
            return 'CheckMate', None
        elif check:
            return 'Check', None
        elif draw:
            return 'Draw', draw_data
        else :
            return False, None

    def reset(self):
        self.board.clear()
        self.killed_pieces.clear()
        self.history.clear()

class VarOSS:
    def __init__(self, data):
        self.data = data
    def set(self, v):
        self.data = v
    def get(self):
        return self.data

if __name__ == '__main__':
    x = ''
    while not(x.lower() in ('console', 'ui', 'c', 'u')):
        x = input('Console | UI ? (enter all word or C/U) : ')
    if x.lower() in ('console', 'c'):
        board1 = Board()
        while True:
            option = input('>> ').split()
            if option:
                match option[0]:
                    case 'write':
                        if len(option) == 1:
                            board1.write()
                        else :
                            board1.write(True)
                    case 'click':
                        if len(option) == 3:
                            if option[1].isdigit() and option[2].isdigit():
                                if (1 <= int(option[1]) <= 8) and (1 <= int(option[2]) <= 8):
                                    result = board1.choose_square((int(option[1]), int(option[2])))
                                    if result:
                                        for item in result:
                                            print(item)
                                    print()
                    case 'back':
                        board1.Undo()
                    case 'help':
                        list_ = ['write', 'click', 'back', 'help']
                        for i in list_:
                            print('-', i)
                    case 'save':
                        data = {
                            'board' : board1.board,
                            'kill' : board1.killed_pieces,
                            'history' : board1.history,
                            'turn' : board1.turn
                        }
                        with open('game', 'w') as file:
                            dump(data, file, indent=4)
                    case 'load':
                        with open('game', 'r') as file:
                            data = load(file)
                        board1.reset()
                        board1 = Board({int(key) : {int(key1) : value1 for key1 , value1 in value.items()} for key , value in data['board'].items()},
                                    {'White' : {int(key) : value for key , value in data['kill']['White'].items()},
                                        'Black' : {int(key) : value for key , value in data['kill']['Black'].items()}},
                                    data['history'],
                                    data['turn'])
                    case _:
                        print('Unknown option')
                if board1.end_game:
                    print(board1.end_data)
                    break
                elif board1.event:
                    print(board1.end_data)
                if board1.dame_event:
                    board1.dame_func(input('New Piece : '))
    else :
        App()