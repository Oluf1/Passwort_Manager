import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .UI_handler import UI_handler
def load_main_menu(ui_handler:"UI_handler"):
        

        name_label = tk.Label(ui_handler.frame_handler.main_frame, text="Password Manager")
        open_vaults_button = tk.Button(
            ui_handler.frame_handler.main_frame,
            text="Vaults",
            bg="royalblue",
            command=lambda: ui_handler.load_vaults(0),
        )
        
        name_label.place(relx=0, rely=0, relwidth=0.95, relheight=0.1)
        config_button = tk.Button(
            ui_handler.frame_handler.main_frame, text="config", bg="lightgrey", command=ui_handler.load_config
        )
        
        open_vaults_button.place(
            relx=0,
            rely=0.1,
            relwidth=1,
            relheight=0.1,
        )
        
        config_button.place(relx=0, rely=0.21, relwidth=1, relheight=0.1)
        ui_handler.root.after(10, lambda: ui_handler.apply_fonts(ui_handler.frame_handler.main_frame))