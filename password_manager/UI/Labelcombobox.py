import tkinter as tk
from tkinter import ttk


class Label_combobox:
    def __init__(
        self,
        widget_master: tk.Frame,
        text: str,
        combobx_values: list,
        default,
        height: float,
        y_pos: float,
    ) -> None:
        # height is relative as such integer division is not neccesary
        label_height = height / 3
        combobx_height = 2 * height / 3
        combobx_ypos = y_pos + label_height
        tk.Label(master=widget_master, text=text).place(
            rely=y_pos, relheight=label_height, relwidth=1
        )

        self.combobox = ttk.Combobox(master=widget_master, values=combobx_values)
        self.combobox.set(default)
        self.combobox.place(relheight=combobx_height, rely=combobx_ypos, relwidth=1)
