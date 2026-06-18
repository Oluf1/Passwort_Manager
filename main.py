import binascii
import json
import os
import random
import secrets
import string
import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Callable

from decrypt import decrypt
from encrypt import encrypt
from managers import ConfigManager, ThemeManager


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


class App:
    CONFIG = ConfigManager()
    THEME_MANAGER = ThemeManager()

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.setup()

        with open("config.json") as f:
            self.vaults = json.load(f)["Vaults"]
        self.vault_names = []
        for name in self.vaults:
            self.vault_names.append(name)
        self.selected_vault = ""
        self.selected_service = ""

        self.supported_kdfs = ["Argon2", "PBKDF2"]
        self.THEME_MANAGER.change_theme(self.CONFIG.theme_name)

        self.root.configure(bg=self.THEME_MANAGER.background)

        self.apply_theme()
        self.load_start_ui()
        self.root.mainloop()

    def setup(self):
        self.create_frames()

    def create_frames(self):
        border_width = 2

        self.main_frame = tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.main_frame.place(relheight=1, relwidth=0.2, relx=0, rely=0)
        self.subframe_1 = tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_1.place(relheight=1, relwidth=0.15, relx=0.2, rely=0)
        self.subframe_2 = tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_2.place(relheight=1, relwidth=0.25, relx=0.35, rely=0)
        self.subframe_3 = tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_3.place(relheight=1, relwidth=0.4, relx=0.6)

        self.subframe_list = [self.subframe_1, self.subframe_2, self.subframe_3]

    def apply_theme(self):
        for frame in self.subframe_list:
            frame.configure(bg=self.THEME_MANAGER.background)
        self.main_frame.config(bg=self.THEME_MANAGER.background)

    def fit_font(self, widget, text: str):
        try:
            widget.update_idletasks()
            widget_width = widget.winfo_width()
            widget_height = widget.winfo_height()

            max_size = 100
            min_size = 1
            low = min_size
            high = max_size
            best = min_size

            font = tkfont.Font(family=self.CONFIG.font_family, size=1)

            while low <= high:
                middle = (low + high) // 2
                font.config(size=middle)
                text_width = font.measure(text)
                text_height = font.metrics("linespace")
                usable_width = widget_width * 0.8

                if text_width <= usable_width and text_height <= widget_height:
                    best = middle
                    low = middle + 1
                else:
                    high = middle - 1

            font.configure(size=best)

            if "text" in widget.keys():
                widget.config(
                    font=font, text=text, fg=self.THEME_MANAGER.text, bg=self.THEME_MANAGER.button_color
                )

        except Exception as e:
            messagebox.showerror("Error in fit_font", str(e))

    def apply_fonts(self, parent):
        for widget in parent.winfo_children():
            if "text" in widget.keys():
                self.fit_font(widget, widget["text"])

    def load_start_ui(self):
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)

        name_label = tk.Label(self.main_frame, text="Password Manager")
        open_vaults_button = tk.Button(
            self.main_frame,
            text="Vaults",
            bg="royalblue",
            command=lambda: self.load_vaults(0),
        )
        name_label.place(relx=0, rely=0, relwidth=0.95, relheight=0.1)
        config_button = tk.Button(
            self.main_frame, text="config", bg="lightgrey", command=self.Load_config
        )
        open_vaults_button.place(
            relx=0,
            rely=0.1,
            relwidth=1,
            relheight=0.1,
        )
        config_button.place(relx=0, rely=0.21, relwidth=1, relheight=0.1)
        self.root.after(10, lambda: self.apply_fonts(self.main_frame))

    def Load_config(self):
        self.temp_items_per_page = self.CONFIG.items_per_page
        self.temp_font_family = self.CONFIG.font_family
        self.clear_subframes(self.subframe_1)

        fonts = list(tkfont.families())
        fonts_combolabel_obj = Label_combobox(
            self.subframe_1, "Fonts", fonts, self.CONFIG.font_family, 0.15, 0.1
        )
        change_fonts_combolabel = fonts_combolabel_obj.combobox

        items_per_page_label = tk.Label(
            self.subframe_1, text=f"items per page: {self.CONFIG.items_per_page + 3}"
        )
        tk.Button(
            self.subframe_1,
            text="+",
            command=lambda change=1: change_items_per_page(change),
        ).place(rely=0.25, relheight=0.05, relx=0.8, relwidth=0.2)
        tk.Button(
            self.subframe_1,
            text="-",
            command=lambda change=-1: change_items_per_page(change),
        ).place(rely=0.3, relheight=0.05, relx=0.8, relwidth=0.2)
        themes = list(self.THEME_MANAGER.theme_keys)

        themes_combolabel = Label_combobox(
            self.subframe_1, "Theme", themes, self.CONFIG.theme_name, 0.15, 0.35
        )

        defualt_kdf_combolabel = Label_combobox(
            self.subframe_1,
            "Default Kdf",
            self.supported_kdfs,
            self.CONFIG.default_kdf,
            0.15,
            0.5,
        )

        def change_items_per_page(change: int):
            self.temp_items_per_page += change
            self.temp_items_per_page = max(3, min(self.temp_items_per_page, 20))
            items_per_page_label.config(
                text=f"items per page: {self.temp_items_per_page + 2}"
            )
            items_per_page_label.update_idletasks()

        def change_font():
            selected_font = change_fonts_combolabel.get()
            if selected_font not in fonts:
                messagebox.showerror("Error", "Not a font")
                return
            self.temp_font_family = selected_font

        def change_theme():
            selected_theme = themes_combolabel.combobox.get()
            if selected_theme not in themes:
                messagebox.showerror("Error", "Not a Theme")
            self.CONFIG.theme_name = selected_theme
            self.THEME_MANAGER.change_theme(self.CONFIG.theme_name)
            self.apply_theme()

        def apply_changes():
            change_font()
            change_theme()
            new_kdf = defualt_kdf_combolabel.combobox.get()

            self.CONFIG.items_per_page = self.temp_items_per_page
            self.CONFIG.font_family = self.temp_font_family
            self.CONFIG.default_kdf = new_kdf
            
            self.CONFIG.save
            self.apply_fonts(self.subframe_1)
            self.Load_config()
            self.load_start_ui()

        tk.Button(self.subframe_1, text="Apply", command=apply_changes).place(
            relheight=0.1, relwidth=1, relx=0, rely=0
        )

        self.render_pages(
            0, self.vault_names, self.subframe_2, self.open_vault_config, self.new_vault
        )

        items_per_page_label.place(relheight=0.1, relwidth=0.8, relx=0, rely=0.25)

        self.apply_fonts(self.subframe_1)

    def open_vault_config(self, vault_name: str):
        vault = self.vaults[vault_name]
        key_location = vault["directories"][0]

        if vault["type"] == "local":
            save_file_location = vault["directories"][1]
        elif vault["type"] == "server":
            messagebox.showerror("Error", "server not yet implemented")
            return
        else:
            return

        def delete_vault():
            if (
                simpledialog.askstring("confirm deletion", "type vault name to delete")
                != vault_name
            ):
                messagebox.showerror("Deletion canceled", "Vault name not matching")
                return
            Path(save_file_location).unlink()
            Path(key_location).unlink()
            with open("config.json", "r") as file:
                config = json.load(file)
            del config["Vaults"][vault_name]
            self.vaults = config["Vaults"]
            self.vault_names.remove(vault_name)
            with open("config.json", "w") as file:
                json.dump(config, file, indent=2)
            self.Load_config()

        tk.Button(self.subframe_3, text="delete", command=delete_vault).place(
            relheight=0.1, relwidth=1, relx=0, rely=0
        )

        self.apply_fonts(self.subframe_3)

    def load_vaults(self, page: int):
        self.selected_vault = ""
        self.render_pages(
            0, self.vault_names, self.subframe_1, self.open_vault, self.new_vault
        )

    def render_pages(
        self,
        page: int,
        items: list[str],
        frame: tk.Frame,
        function: Callable,
        add_command: Callable,
        filter_str=None,
    ):
        self.clear_subframes(frame)
        start = page * self.CONFIG.items_per_page
        end = start + self.CONFIG.items_per_page
        btn_size = 1 / (self.CONFIG.items_per_page + 3)
        filtered_items = []
        if filter_str:
            for item in items:
                if filter_str in item:
                    filtered_items.append(item)
        else:
            filtered_items = items
        current_items = filtered_items[start:end]
        if page == 0:
            match add_command:
                case self.new_vault:
                    btn_text = "Add vault"
                case self.add_mail:
                    btn_text = "add mail"
                case self.add_service:
                    btn_text = "add service"
                case _:
                    messagebox.showerror("Error", "wrong add_command function given ")
                    return
            new_x_button = tk.Button(frame, text=btn_text, command=add_command)
            new_x_button.place(relx=0, rely=0, relwidth=1, relheight=btn_size)
            self.fit_font(new_x_button, text=btn_text)
        else:
            up_button = tk.Button(
                frame,
                text="page up",
                command=lambda new_page=page - 1: self.render_pages(
                    new_page, items, frame, function, add_command
                ),
            )
            up_button.place(relx=0, rely=0, relwidth=1, relheight=btn_size)
            self.fit_font(up_button, "page up")
        search_entry = tk.Entry(frame)
        if filter_str:
            search_entry.insert(0, filter_str)
        search_entry.place(relx=0, rely=btn_size, relheight=btn_size, relwidth=0.8)

        def filtered_search():
            self.render_pages(
                page, items, frame, function, add_command, search_entry.get()
            )

        tk.Button(frame, command=filtered_search, text="Search").place(
            relx=0.8, rely=btn_size, relheight=btn_size, relwidth=0.2
        )
        for i, item in enumerate(current_items):
            if frame == self.subframe_3:
                text_name = f"{item[0]} {str(item[1])}"
            else:
                text_name = item
            button = tk.Button(
                frame, text=str(text_name), command=lambda it=item: function(it)
            )
            button.place(
                relheight=btn_size, relx=0, relwidth=1, rely=2 * btn_size + btn_size * i
            )
            self.fit_font(button, text_name)
        if end < len(items):
            down_button = tk.Button(
                frame,
                text="page down",
                command=lambda new_page=page + 1: self.render_pages(
                    new_page, items, frame, function, add_command
                ),
            )
            down_button.place(relx=0, relheight=btn_size, rely=1 - btn_size, relwidth=1)
            self.fit_font(down_button, "page down")

    def clear_subframes(self, subframe: tk.Frame):
        index = self.subframe_list.index(subframe)
        for frame in self.subframe_list[index:]:
            for widget in frame.winfo_children():
                widget.destroy()

    def new_vault(self):
        new_vault_popup = tk.Toplevel(self.root)
        new_vault_popup.title("New Vault")
        new_vault_popup.configure(bg="gray74")
        self.scale_toplevel(new_vault_popup, 0.5)

        tk.Label(new_vault_popup, text="New vault Name").place(
            relheight=0.1, relx=0, rely=0, relwidth=0.4
        )
        vault_name_entry = tk.Entry(new_vault_popup)

        vault_name_entry.place(relheight=0.15, relwidth=1, relx=0, rely=0.1)

        vault_type = tk.StringVar(value="local")

        tk.Label(new_vault_popup, text="vault type").place(
            relheight=0.1, relx=0, rely=0.27, relwidth=0.4
        )
        tk.Radiobutton(
            new_vault_popup, text="Local", value="local", variable=vault_type
        ).place(relheight=0.1, relx=0, rely=0.4, relwidth=0.4)
        tk.Radiobutton(
            new_vault_popup, text="server", value="server", variable=vault_type
        ).place(relheight=0.1, relx=0.5, rely=0.4, relwidth=0.4)

        def add_vault():
            if vault_type.get() == "server":
                messagebox.showerror("Error", "Server saving not yet implemented")
                return
            vault_name = vault_name_entry.get()
            if vault_name in self.vault_names:
                messagebox.showerror(
                    "Error", "Vault name already exists choose another"
                )
                return
            save_dir = filedialog.askopenfilename(
                initialdir="/",
                title="select save directory",
                filetypes=(("json files", "*.json*"),),
            )
            key_dir = filedialog.askopenfilename(
                initialdir="/",
                title="select key directory",
                filetypes=(("Text files", "*.txt*"),),
            )
            if not save_dir or not key_dir:
                messagebox.showerror("Error", "No directory selected")
                return
            with open("config.json") as config:
                data = json.load(config)
            data["Vaults"][vault_name] = {
                "directories": [key_dir, save_dir],
                "type": "local",
            }
            with open("config.json", "w") as file:
                json.dump(data, file, indent=2)
            save_path = Path(save_dir)
            try:
                if save_path.stat().st_size > 0:
                    with open(save_path, "r", encoding="utf-8") as file:
                        save = json.load(file)
                else:
                    save = {}

            except json.JSONDecodeError:
                save = {}
            save.setdefault("services", {})
            with open(save_path, "w", encoding="utf-8") as file:
                json.dump(save, file, indent=2)

            key_path = Path(key_dir)
            content = key_path.read_text().strip()
            try:
                key = binascii.unhexlify(content)
                if len(key) != 32:
                    key = os.urandom(32)
                    key_path.write_text(key.hex())
            except binascii.Error:
                messagebox.showerror("Error", "not a valid hex string")

            new_vault_popup.destroy()
            self.vaults[vault_name] = {
                "directories": [key_dir, save_dir],
                "type": "local",
            }
            self.vault_names.append(vault_name)
            self.load_vaults(0)

        tk.Button(new_vault_popup, text="choose locations", command=add_vault).place(
            relheight=0.1, rely=0.5, relx=0, relwidth=0.3
        )
        new_vault_popup.after(10, self.apply_fonts, new_vault_popup)
        new_vault_popup.transient(self.root)
        new_vault_popup.grab_set()

    def open_vault(self, name: str):
        self.selected_vault = name
        self.clear_subframes(self.subframe_2)

        vault = self.vaults[name]
        services: list[str] = []

        if vault["type"] == "local":
            location = vault["directories"][1]

            with open(location) as f:
                data = json.load(f)

                services = list(data["services"].keys())

        elif vault["type"] == "server":
            messagebox.showerror("Error", "server not yet implemented")
        else:
            messagebox.showerror("Error", f"{vault[type]} is not a valid save type.")

        self.render_pages(
            0, services, self.subframe_2, self.open_service, self.add_service
        )

    def add_service(self):
        new_service_popup = tk.Toplevel(
            self.root,
        )
        self.scale_toplevel(new_service_popup, 0.5)

        name_entry = tk.Entry(new_service_popup)
        name_entry.place(relheight=0.1, relx=0, rely=0.1, relwidth=1)
        tk.Label(new_service_popup, text="Name").place(
            relheight=0.1, relx=0, rely=0, relwidth=0.5
        )

        def create_service():
            new_name = name_entry.get()

            services: list[str] = []
            vault = self.vaults[self.selected_vault]
            if vault["type"] == "local":
                location = vault["directories"][1]
                with open(location) as f:
                    data = json.load(f)

                    services = list(data["services"].keys())
                if new_name in services:
                    messagebox.showerror("Error", "Service already exists")
                    return
                new_service_popup.destroy()
                data["services"][new_name] = []
                with open(location, "w") as file:
                    json.dump(data, file, indent=2)
                self.open_vault(self.selected_vault)

        tk.Button(
            new_service_popup, command=create_service, text="create service"
        ).place(relheight=0.1, rely=0.3, relx=0, relwidth=0.5)

        new_service_popup.after(10, self.apply_fonts, new_service_popup)
        new_service_popup.transient(self.root)
        new_service_popup.grab_set()

    def open_service(self, name: str):
        self.selected_service = name

        self.clear_subframes(self.subframe_3)

        vault = self.vaults[self.selected_vault]
        Mails: list = []
        if vault["type"] == "local":
            location = vault["directories"][1]
            with open(location) as f:
                data = json.load(f)

            for ele in data["services"][name]:
                Mails.append((ele["Mail"], ele["count"]))
            self.render_pages(0, Mails, self.subframe_3, self.open_mail, self.add_mail)

    def open_mail(self, name: str):
        mail_popup = tk.Toplevel(self.root)

        self.scale_toplevel(mail_popup, 0.5)
        mail_popup.title(name)

        tk.Label(mail_popup, text=f"service: {self.selected_service}").place(
            relx=0, rely=0, relheight=0.15
        )
        password_Label = tk.Label(mail_popup, text="password: ****")
        password_Label.place(relx=0, relheight=0.15, rely=0.15)

        def decrypt_password():
            master_password = simpledialog.askstring(
                "enter Masterpassword", "Masterpassword:"
            )
            if master_password is not None:
                master_password = master_password.encode("utf-8")
            else:
                messagebox.showerror("Error", "Masterpassword can not be empty")
                return
            Mail = name[0]
            count = int(name[1])
            decrypted_password = decrypt(
                master_password, self.selected_service, Mail, count, self.selected_vault
            )
            password_Label.configure(text=f"Password: {decrypted_password}")
            self.root.clipboard_clear()
            self.root.clipboard_append(decrypted_password)
            self.root.after(
                30000,
                lambda: (self.root.clipboard_clear(), self.root.clipboard_append("")),
            )

        tk.Button(mail_popup, text="decrypt Password", command=decrypt_password).place(
            relx=0.3, rely=0.15, relheight=0.15
        )

        def update_password():
            new_data_popup = tk.Toplevel(self.root)
            self.scale_toplevel(new_data_popup, 0.3)
            mail = name[0]
            new_name_entry = tk.Entry(new_data_popup)
            new_name_entry.insert(0, mail)
            new_name_entry.place(relx=0, relheight=0.1, rely=0.1, relwidth=1)
            tk.Label(new_data_popup, text="new_mail").place(
                relx=0, rely=0, relheight=0.1
            )
            new_password_entry = tk.Entry(new_data_popup)
            tk.Label(new_data_popup, text="new Password").place(
                relx=0, relheight=0.1, rely=0.2
            )

            def generate_password():
                length = random.randint(0, 8) + 30
                alphabet = string.ascii_letters + string.digits + string.punctuation
                password = "".join(secrets.choice(alphabet) for _ in range(length))
                new_password_entry.delete(0, tk.END)
                new_password_entry.insert(0, password)

            tk.Button(
                new_data_popup, text="generate password", command=generate_password
            ).place(relx=0.5, relheight=0.1, rely=0.2)
            new_password_entry.place(relx=0, relheight=0.1, rely=0.3, relwidth=1)

            new_master_entry = tk.Entry(new_data_popup)
            tk.Label(new_data_popup, text="new Master password").place(
                relx=0, relheight=0.1, rely=0.4
            )
            new_master_entry.place(relx=0, rely=0.5, relheight=0.1, relwidth=1)

            def call_encryption():
                new_master = new_master_entry.get()
                new_name = new_name_entry.get()
                new_password = new_password_entry.get()

                if not new_master or not new_name or not new_password:
                    messagebox.showerror("Error", "No field can be left empty")
                    return
                encrypt(
                    new_master.encode(),
                    new_password.encode(),
                    self.selected_service,
                    self.selected_vault,
                    name[0],
                    int(name[1]),
                    True,
                    new_name,
                )
                new_data_popup.destroy()

            tk.Button(new_data_popup, command=call_encryption, text="continue").place(
                relx=0, rely=0.6, relheight=0.1
            )

            new_data_popup.transient(self.root)
            new_data_popup.grab_set()

        tk.Button(mail_popup, text="change Password", command=update_password).place(
            relx=0.6, rely=0.15, relheight=0.15
        )

        mail_popup.transient(self.root)
        mail_popup.grab_set()

    def add_mail(self):
        add_mail_popup = tk.Toplevel(self.root)
        self.scale_toplevel(add_mail_popup, 0.5)

        name_entry = tk.Entry(add_mail_popup)
        tk.Label(add_mail_popup, text="Email").place(
            relx=0, rely=0, relheight=0.15, relwidth=0.2
        )
        name_entry.place(relheight=0.15, relx=0, rely=0.15, relwidth=0.4)

        password_entry = tk.Entry(add_mail_popup)

        def generate_password():
            length = random.randint(0, 8) + 16
            alphabet = string.ascii_letters + string.digits + string.punctuation
            password = "".join(secrets.choice(alphabet) for _ in range(length))
            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)

        tk.Button(
            add_mail_popup, text="generate password", command=generate_password
        ).place(relx=0.5, relheight=0.15, rely=0.3)
        tk.Label(add_mail_popup, text="Password").place(
            relx=0, relheight=0.15, rely=0.3
        )
        password_entry.place(relx=0, rely=0.45, relheight=0.15, relwidth=1)

        master_password_entry = tk.Entry(add_mail_popup)
        tk.Label(add_mail_popup, text="Masterpassword").place(
            relx=0, rely=0.6, relheight=0.1, relwidth=0.3
        )
        master_password_entry.place(relx=0, rely=0.7, relheight=0.1, relwidth=0.45)
        confirm_master_password_entry = tk.Entry(add_mail_popup)
        confirm_master_password_entry.place(
            relx=0.5, rely=0.7, relheight=0.1, relwidth=0.5
        )
        tk.Label(add_mail_popup, text="Confirm Masterpassword").place(
            relheight=0.1, relx=0.5, relwidth=0.3, rely=0.6
        )

        def add_entry():

            name = name_entry.get()
            service = self.selected_service
            vault = self.selected_vault
            password = password_entry.get()
            master = master_password_entry.get()
            confirmation_master = confirm_master_password_entry.get()
            if not all([name, password, vault, service, master, confirmation_master]):
                messagebox.showerror("Error", "All entrys must be filled to proceed")
                return
            elif master != confirmation_master:
                messagebox.showerror("Error", "Master passwords not matching")
                return

            encrypt(
                master.encode(), password.encode(), service, vault, name, 1, False, name
            )
            add_mail_popup.destroy()
            self.open_service(self.selected_service)

        tk.Button(add_mail_popup, text="add", command=add_entry).place(
            relx=0, rely=0.9, relheight=0.1
        )
        add_mail_popup.after(10, self.apply_fonts, add_mail_popup)
        add_mail_popup.transient(self.root)
        add_mail_popup.grab_set()

    def scale_toplevel(self, window: tk.Toplevel, size: float):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        width = int(screen_width * size)
        height = int(screen_height * size)
        x = int((screen_width - width) * 0.5)
        y = int((screen_height - height) * 0.5)
        window.geometry(f"{width}x{height}+{x}+{y}")
        window.config(bg=self.THEME_MANAGER.top_level_color)


if __name__ == "__main__":
    App()
