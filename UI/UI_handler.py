import tkinter as tk
#from tkinter import messagebox, simpledialog
from typing import Callable
class UI_handler:
    def __init__(self,apply_fonts:Callable) -> None:
        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.background = "F3F3F3" #Default bg color to avoid Errors
        self.apply_fonts = apply_fonts
        
        
        
        
    def setup(self):
        self.create_frames()
    def create_frames(self): 
        border_width = 2

        self.main_frame =   tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.main_frame.place(relheight=1, relwidth=0.2, relx=0, rely=0)
        self.subframe_1 = tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_1.place(relheight=1, relwidth=0.15, relx=0.2, rely=0)
        self.subframe_2 = tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_2.place(relheight=1, relwidth=0.25, relx=0.35, rely=0)
        self.subframe_3 = tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_3.place(relheight=1, relwidth=0.4, relx=0.6)

        self.subframe_list = [self.subframe_1, self.subframe_2, self.subframe_3]
    def apply_theme_on_frames(self):
        for frame in self.subframe_list:
            frame.configure(bg=self.background)
        self.main_frame.config(bg=self.background)