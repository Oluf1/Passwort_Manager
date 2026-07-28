import tkinter as tk
import tkinter.font as tkfont
from .UI_handler import UI_handler
from .Labelcombobox import Label_combobox
from tkinter import messagebox


def load_config(ui_handler:UI_handler):  # move (config UI manager)
    temp_items_per_page = ui_handler.config.items_per_page
    ui_handler.frame_handler.clear_subframes(ui_handler.frame_handler.subframe_1)

    parent = ui_handler.frame_handler.subframe_1
    fonts = list(tkfont.families())
    themes = list(ui_handler.theme_manager.theme_keys)

    fonts_combolabel = Label_combobox(parent, "Fonts", fonts, ui_handler.config.font_family, 0.15, 0.1)
    themes_combolabel = Label_combobox(parent, "Theme", themes, ui_handler.config.theme_name, 0.15, 0.35)
    kdf_combolabel = Label_combobox(
        parent, "Default Kdf", ui_handler.config.supported_kdfs, ui_handler.config.default_kdf, 0.15, 0.5
    )

    items_per_page_label = tk.Label(parent)
    items_per_page_label.place(relheight=0.1, relwidth=0.8, relx=0, rely=0.25)

    def update_items_per_page_label():
        items_per_page_label.config(
            text=f"items per page: {temp_items_per_page + 3}"
        )

    def change_items_per_page(change: int):
        nonlocal temp_items_per_page
        temp_items_per_page = max(3, min(temp_items_per_page + change, 20))
        update_items_per_page_label()

    update_items_per_page_label()

    for symbol, change, rely in (("+", 1, 0.25), ("-", -1, 0.3)):
        tk.Button(
            parent, text=symbol, command=lambda c=change: change_items_per_page(c)
        ).place(rely=rely, relheight=0.05, relx=0.8, relwidth=0.2)

    def apply_changes():
        selected_font = fonts_combolabel.combobox.get()
        selected_theme = themes_combolabel.combobox.get()

        if selected_font not in fonts:
            messagebox.showerror("Error", "Not a font")
            return
        if selected_theme not in themes:
            messagebox.showerror("Error", "Not a Theme")
            return

        ui_handler.config.items_per_page = temp_items_per_page
        ui_handler.config.font_family = selected_font
        ui_handler.config.theme_name = selected_theme
        ui_handler.config.default_kdf = kdf_combolabel.combobox.get()
        ui_handler.config.save()

        ui_handler.theme_manager.change_theme(ui_handler.config.theme_name)
        ui_handler.frame_handler.apply_theme_on_frames()
        ui_handler.font_manager.apply_fonts(parent)
        ui_handler.load_main_menu()
        load_config(ui_handler)
        

    tk.Button(parent, text="Apply", command=apply_changes).place(
        relheight=0.1, relwidth=1, relx=0, rely=0
    )

    ui_handler.render_pages(
        0, ui_handler.vault_manager.get_vault_names(), ui_handler.frame_handler.subframe_2,
        ui_handler.app.open_vault_config, ui_handler.app.new_vault
    )

    ui_handler.font_manager.apply_fonts(parent)