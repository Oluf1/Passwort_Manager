import tkinter as tk
from typing import Callable
from tkinter import messagebox
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from.UI_handler import UI_handler


def render_pages(
        ui_handler:"UI_handler",
        page: int,
        items: list[str],
        frame: tk.Frame,
        function: Callable,
        add_command: Callable,
        filter_str=None,
        
    ): # move (UI handler)
        ui_handler.frame_handler.clear_subframes(frame)
        start = page * ui_handler.config.items_per_page
        end = start + ui_handler.config.items_per_page
        btn_size = 1 / (ui_handler.config.items_per_page + 3)
        filtered_items = []
        if filter_str:
            for item in items:
                if filter_str in item:
                    filtered_items.append(item)
        else:
            filtered_items = items
        print(filtered_items)
        current_items = filtered_items[start:end]

        if page == 0:
            match add_command:
                case ui_handler.new_vault:
                    btn_text = "Add vault"
                case ui_handler.app.add_mail:
                    btn_text = "add mail"
                case ui_handler.add_service:
                    btn_text = "add service"
                case _:
                    messagebox.showerror("Error", f"wrong add_command function given: {add_command}")
                    return
            new_x_button = tk.Button(frame, text=btn_text, command=add_command)
            new_x_button.place(relx=0, rely=0, relwidth=1, relheight=btn_size)

        else:
            up_button = tk.Button(
                frame,
                text="page up",
                command=lambda new_page=page - 1: render_pages(
                    ui_handler,new_page, items, frame, function, add_command
                ),
            )
            up_button.place(relx=0, rely=0, relwidth=1, relheight=btn_size)

        search_entry = tk.Entry(frame)
        if filter_str:
            search_entry.insert(0, filter_str)
        search_entry.place(relx=0, rely=btn_size, relheight=btn_size, relwidth=0.8)

        def filtered_search():
            render_pages(
                ui_handler,page, items, frame, function, add_command, search_entry.get()
            )

        tk.Button(frame, command=filtered_search, text="Search").place(
            relx=0.8, rely=btn_size, relheight=btn_size, relwidth=0.2
        )
        for i, item in enumerate(current_items):
            if frame == ui_handler.frame_handler.subframe_3:
                text_name = f"{item[0]} {str(item[1])}"
            else:
                text_name = item
            button = tk.Button(
                frame, text=str(text_name), command=lambda it=item: function(it)
            )
            button.place(
                relheight=btn_size, relx=0, relwidth=1, rely=2 * btn_size + btn_size * i
            )

        if end < len(filtered_items):
            down_button = tk.Button(
                frame,
                text="page down",
                command=lambda new_page=page + 1: render_pages(
                    ui_handler,new_page, items, frame, function, add_command
                ),
            )
            down_button.place(relx=0, relheight=btn_size, rely=1 - btn_size, relwidth=1)

        ui_handler.apply_fonts(frame)