import json
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from typing import Callable


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Manager")
        
        
        with open("config.json") as f:
            self.vaults = json.load(f)["Vaults"]
        self.vault_names = []
        for name in self.vaults:
            self.vault_names.append(name)
        self.selected_vault = ""
        self.selected_service = ""
        self.items_per_page = 18  # will be in config later
        border_width = 2
        self.main_frame = ttk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.main_frame.place(relheight=1, relwidth=0.2, relx=0, rely=0)
        self.subframe_1 = ttk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_1.place(relheight=1, relwidth=0.15, relx=0.2, rely=0)
        self.subframe_2 = ttk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_2.place(relheight=1, relwidth=0.25, relx=0.35, rely=0)
        self.subframe_3 = ttk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_3.place(relheight=1, relwidth=0.4, relx=0.6)
        self.load_start_ui()
        self.root.mainloop()

    def fit_font(self, label: tk.Label, text: str):
        label.update_idletasks()
        label_width = label.winfo_width()
        max_size = 100
        min_size = 1
        low = min_size
        high = max_size
        best = min_size
        font = tkfont.Font(
            family="Arial",
            size=1,
        )
        while low <= high:
            middle = (low + high) // 2
            font.config(size=middle)
            text_width = font.measure(text)
            if text_width <= label_width:
                best = middle
                low = middle + 1
            else:
                high = middle - 1
        font.configure(size=best)
        label.config(font=font, text=text)

    def load_start_ui(self):
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)

        name_label = tk.Label(self.main_frame)
        open_vaults_button = tk.Button(
            self.main_frame,
            text="Vaults",
            bg="royalblue",
            command=lambda: self.load_vaults(0),
        )
        name_label.place(relx=0, rely=0, relwidth=0.95)
        config_button = tk.Button(self.main_frame, text="config", bg="lightgrey")
        open_vaults_button.place(
            relx=0,
            rely=0.1,
            relwidth=1,
            relheight=0.1,
        )
        config_button.place(relx=0, rely=0.21, relwidth=1, relheight=0.1)
        self.root.after(10, lambda: self.fit_font(name_label, "Password Manager"))

    def load_vaults(self, page: int):
        self.render_pages(0, self.vault_names, self.subframe_1, self.open_vault)

    def render_pages(
        self, page: int, items: list, frame: ttk.Frame, function: Callable
    ):
        self.clear_subframes(frame)
        start = page * self.items_per_page
        end = start + self.items_per_page
        current_items = items[start:end]
        if page == 0:
            match frame:
                case self.subframe_1:
                    add_vault_button = tk.Button(
                        self.subframe_1, text="Add vault", command=self.add_vault
                    )
                    add_vault_button.place(relx=0, rely=0, relwidth=1, relheight=0.05)
                case self.subframe_2:
                    add_service_button = tk.Button(
                        self.subframe_2, text="Add Service", command=self.add_service
                    )
                    add_service_button.place(relx=0, rely=0, relwidth=1, relheight=0.05)
                case self.subframe_3:
                    pass
                case _:
                    print("error wrong subframe in render_pages")
        else:
            up_button = tk.Button(
                frame,
                text="page up",
                command=lambda: self.render_pages(page - 1, items, frame, function),
            )
            up_button.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        for i, name in enumerate(current_items):
            button = tk.Button(frame, text=name, command=lambda: function(name))
            button.place(relheight=0.05, relx=0, relwidth=1, rely=0.05 + 0.05 * i)

    def clear_subframes(self, subframe: ttk.Frame):
        for widget in subframe.winfo_children():
            widget.destroy()

    def add_vault(self):
        new_vault_popup = tk.Toplevel(self.root)
        new_vault_popup.title("New Vault")
        new_vault_popup.configure(bg='gray74')
        screen_width = new_vault_popup.winfo_screenwidth()
        screen_height = new_vault_popup.winfo_screenheight()
        
        width = int(screen_width * 0.5)
        height = int(screen_height * 0.5)
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        new_vault_popup.geometry(f"{width}x{height}+{x}+{y}")
        
        vault_name_label = tk.Label(new_vault_popup,text="New vault Name")
        vault_name_entry = tk.Entry(new_vault_popup)
        vault_name_label.place(relheight=0.1,relx=0,rely=0)
        vault_name_entry.place(relheight=0.15,relwidth=1,relx=0,rely=0.1)
        
        vault_type =tk.StringVar(value="local")
        
        vault_type_label = tk.Label(new_vault_popup,text="vault type")
        
        new_vault_popup.transient(self.root)
        new_vault_popup.grab_set
        
    def open_vault(self, name: str):
        self.selected_vault = name
        self.clear_subframes(self.subframe_2)
        vault = self.vaults[name]
        services: list[str] = []
        if vault["type"] == "local":
            location = vault["directories"][1]
            with open(location) as f:
                Entries = json.load(f)["Entries"]
                for entry in Entries:
                    services.append(entry["Service"])

        elif vault["type"] == "server":
            print("not yet implemented")
        else:
            print(f"{vault['type']} is not a valid save type.")
        self.render_pages(0,services,self.subframe_2,self.open_service)
    def add_service(self):
        pass
    def open_service(self,name:int):
        pass

if __name__ == "__main__":
    App()
