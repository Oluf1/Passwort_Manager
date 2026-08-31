import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path
from tkinter import messagebox, simpledialog
from typing import TYPE_CHECKING

from .Labelcombobox import Label_combobox

if TYPE_CHECKING:
    from .UI_handler import UI_handler


class ConfigUI:
    def __init__(self, ui_handler: "UI_handler"):
        self.ui_handler = ui_handler
        self.temp_items_per_page = ui_handler.config.items_per_page

    def load_config(self):
        self.temp_items_per_page = self.ui_handler.config.items_per_page

        self.ui_handler.frame_handler.clear_subframes(
            self.ui_handler.frame_handler.subframe_1
        )

        parent = self.ui_handler.frame_handler.subframe_1
        fonts = list(tkfont.families())
        themes = list(self.ui_handler.theme_manager.theme_keys)

        fonts_combolabel = Label_combobox(
            parent,
            "Fonts",
            fonts,
            self.ui_handler.config.font_family,
            0.15,
            0.1,
        )

        themes_combolabel = Label_combobox(
            parent,
            "Theme",
            themes,
            self.ui_handler.config.theme_name,
            0.15,
            0.35,
        )

        kdf_combolabel = Label_combobox(
            parent,
            "Default Kdf",
            self.ui_handler.config.supported_kdfs,
            self.ui_handler.config.default_kdf,
            0.15,
            0.5,
        )

        items_per_page_label = tk.Label(parent)
        items_per_page_label.place(
            relheight=0.1,
            relwidth=0.8,
            relx=0,
            rely=0.25,
        )

        self._update_items_per_page_label(items_per_page_label)

        for symbol, change, rely in (
            ("+", 1, 0.25),
            ("-", -1, 0.3),
        ):
            tk.Button(
                parent,
                text=symbol,
                command=lambda c=change, lbl=items_per_page_label: self._change_items_per_page(
                    c, lbl
                ),
            ).place(
                rely=rely,
                relheight=0.05,
                relx=0.8,
                relwidth=0.2,
            )

        tk.Button(
            parent,
            text="Apply",
            command=lambda: self._apply_changes(
                fonts,
                themes,
                fonts_combolabel,
                themes_combolabel,
                kdf_combolabel,
                parent,
            ),
        ).place(
            relheight=0.1,
            relwidth=1,
            relx=0,
            rely=0,
        )

        self.ui_handler.render_pages(
            0,
            self.ui_handler.vault_manager.get_vault_names(),
            self.ui_handler.frame_handler.subframe_2,
            self.open_vault_config,
            self.ui_handler.new_vault,
        )

        self.ui_handler.apply_fonts(parent)

    def _update_items_per_page_label(self, label: tk.Label):
        label.config(
            text=f"items per page: {self.temp_items_per_page + 3}"
        )

    def _change_items_per_page(self, change: int, label: tk.Label):
        self.temp_items_per_page = max(
            3,
            min(self.temp_items_per_page + change, 20),
        )
        self._update_items_per_page_label(label)

    def _apply_changes(
        self,
        fonts,
        themes,
        fonts_combolabel,
        themes_combolabel,
        kdf_combolabel,
        parent,
    ):
        selected_font = fonts_combolabel.combobox.get()
        selected_theme = themes_combolabel.combobox.get()

        if selected_font not in fonts:
            self.ui_handler.messagebox_error("Not a font")
            return

        if selected_theme not in themes:
            self.ui_handler.messagebox_error("Not a Theme")
            return

        self.ui_handler.config.items_per_page = self.temp_items_per_page
        self.ui_handler.config.font_family = selected_font
        self.ui_handler.config.theme_name = selected_theme
        self.ui_handler.config.default_kdf = kdf_combolabel.combobox.get()
        self.ui_handler.config.save()

        self.ui_handler.theme_manager.change_theme(
            self.ui_handler.config.theme_name
        )
        self.ui_handler.frame_handler.apply_theme_on_frames()
        self.ui_handler.apply_fonts(parent)
        self.ui_handler.load_main_menu()

        self.load_config()

    def open_vault_config(self, vault_name: str):
        vault = self.ui_handler.vault_manager.vaults[vault_name]
        key_location = vault.key_path

        if vault.vault_type == "local":
            save_file_location = vault.data_path
        elif vault.vault_type == "server":
            self.ui_handler.messagebox_error("server not yet implemented")
            return
        else:
            return

        def delete_vault():
            if (
                simpledialog.askstring(
                    "confirm deletion",
                    "type vault name to delete",
                )
                != vault_name
            ):
                messagebox.showerror(
                    "Deletion canceled",
                    "Vault name not matching",
                )
                return

            Path(save_file_location).unlink()
            Path(key_location).unlink()

            self.ui_handler.vault_manager.delete_vault(vault_name)
            self.load_config()

        tk.Button(
            self.ui_handler.frame_handler.subframe_3,
            text="delete",
            command=delete_vault,
        ).place(
            relheight=0.1,
            relwidth=1,
            relx=0,
            rely=0,
        )

        self.ui_handler.apply_fonts(
            self.ui_handler.frame_handler.subframe_3
        )