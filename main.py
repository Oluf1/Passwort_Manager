import json
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from typing import Callable
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from decrypt import decrypt
from encrypt import encrypt

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
        with open("config.json") as file:
            config = json.load(file)["config"]
            self.items_per_page =  config["items_per_page"] 
            self.font_family = config["font_family"]
        border_width = 2
        
        
        self.main_frame = ttk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.main_frame.place(relheight=1, relwidth=0.2, relx=0, rely=0)
        self.subframe_1 = ttk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_1.place(relheight=1, relwidth=0.15, relx=0.2, rely=0)
        self.subframe_2 = ttk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_2.place(relheight=1, relwidth=0.25, relx=0.35, rely=0)
        self.subframe_3 = ttk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_3.place(relheight=1, relwidth=0.4, relx=0.6)
        
        
        self.subframe_list = [self.subframe_1,self.subframe_2,self.subframe_3]
        self.load_start_ui()
        self.root.mainloop()

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

            font = tkfont.Font(family=self.font_family, size=1)

            while low <= high:
                middle = (low + high) // 2
                font.config(size=middle)
                text_width = font.measure(text)
                text_height = font.metrics("linespace")
                usable_width = widget_width *0.8
                
                if text_width <= usable_width and text_height <= widget_height:
                    best = middle
                    low = middle + 1
                else:
                    high = middle - 1

            font.configure(size=best)

            if "text" in widget.keys():
                widget.config(font=font, text=text)

        except Exception as e:
            print("Error in fit_font:", e)
    def apply_fonts(self, parent):
        for widget in parent.winfo_children():
            if "text" in widget.keys():
                self.fit_font(widget, widget["text"])
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
        config_button = tk.Button(self.main_frame, text="config", bg="lightgrey",command= self.Load_config)
        open_vaults_button.place(
            relx=0,
            rely=0.1,
            relwidth=1,
            relheight=0.1,
        )
        config_button.place(relx=0, rely=0.21, relwidth=1, relheight=0.1)
        self.root.after(10, lambda: self.fit_font(name_label, "Password Manager"))

    def Load_config(self):
        self.temp_items_per_page = self.items_per_page
        self.temp_font_family = self.font_family
        self.clear_subframes(self.subframe_1)
        
        
        fonts = list(tkfont.families())
        change_fonts_combobox = ttk.Combobox(self.subframe_1,values=fonts)
        change_fonts_combobox.set(self.font_family)
        
        items_per_page_label = tk.Label(self.subframe_1,text=f"items per page: {self.items_per_page+2}")
        tk.Button(
            self.subframe_1,text="+",command= lambda change =1:change_items_per_page(change)
            ).place(rely=0.25,relheight=0.05,relx=0.8,relwidth=0.2)
        tk.Button(
            self.subframe_1,text="-",command= lambda change = -1:change_items_per_page(change)
            ).place(rely=0.3,relheight=0.05,relx=0.8,relwidth=0.2)
        def change_items_per_page(change:int):
            self.temp_items_per_page += change 
            self.temp_items_per_page = max(3,min(self.temp_items_per_page,20))
            items_per_page_label.config(text=f"items per page: {self.temp_items_per_page+2}")
            items_per_page_label.update_idletasks()
            
            
        def change_font():
            selected_font = change_fonts_combobox.get()
            if selected_font not in fonts:
                messagebox.showerror("Error","Not a font")
                return
            self.temp_font_family = selected_font
        
        
        def apply_changes():
            with open("config.json", "r") as file:
                data = json.load(file)
            self.items_per_page = self.temp_items_per_page
            self.font_family = self.temp_font_family
            data["config"]["items_per_page"] = self.items_per_page
            data["config"]["font_family"] = self.font_family
            with open("config.json", "w") as file:
                json.dump(data, file, indent=4)
                
                
        tk.Button(
            self.subframe_1,text="Apply",command=apply_changes
            ).place(relheight=0.1,relwidth=1,relx=0,rely=0)
        
        tk.Button(
            self.subframe_1,text="change font",command=change_font
            ).place(relheight=0.05,relwidth=1,rely=0.2)
        items_per_page_label.place(relheight=0.1,relwidth=0.8,relx=0,rely=0.25)
            
        
        change_fonts_combobox.place(rely=0.1,relx=0,relheight=0.1,relwidth=1)
        
        
            
        
        
        
    def load_vaults(self, page: int):
        self.selected_vault = ""
        self.render_pages(0, self.vault_names, self.subframe_1, self.open_vault)

    def render_pages(
        self, page: int, items: list, frame: ttk.Frame, function: Callable
    ):
        self.clear_subframes(frame)
        start = page * self.items_per_page
        end = start + self.items_per_page
        btn_size = 1 / (self.items_per_page + 2)
        current_items = items[start:end]
        if page == 0:
            match frame:
                case self.subframe_1:
                    new_vault_button = tk.Button(
                        self.subframe_1, text="Add vault", command=self.new_vault
                    )
                    new_vault_button.place(
                        relx=0, rely=0, relwidth=1, relheight=btn_size
                    )
                    self.fit_font(new_vault_button,text="Add vault")
                case self.subframe_2:
                    add_service_button = tk.Button(
                        self.subframe_2, text="Add Service", command=self.add_service
                    )
                    add_service_button.place(
                        relx=0, rely=0, relwidth=1, relheight=btn_size
                    )
                    self.fit_font(add_service_button,"Add Service")
                case self.subframe_3:
                    add_mail_button = tk.Button(
                        self.subframe_3, text="add Mail", command=self.add_mail
                    )
                    add_mail_button.place(
                        relx=0, rely=0, relwidth=1, relheight=btn_size
                    )
                    self.fit_font(add_mail_button,"add Mail")
                case _:
                    print("error wrong subframe in render_pages")
        else:
            up_button = tk.Button(
                frame,
                text="page up",
                command=lambda new_page=page - 1: self.render_pages(
                    new_page, items, frame, function
                ),
            )
            up_button.place(relx=0, rely=0, relwidth=1, relheight=btn_size)
            self.fit_font(up_button,"page up")
        
        for i, item in enumerate(current_items):
            if frame == self.subframe_3:
                text_name = f"{item[0]} {str(item[1])}"
            else:
                text_name = item
            button = tk.Button(
                frame, text=str(text_name), command=lambda it=item: function(it)
            )
            button.place(
                relheight=btn_size, relx=0, relwidth=1, rely=btn_size + btn_size * i
            )
            self.fit_font(button,text_name)
        if  end < len(items):
            down_button = tk.Button(
                frame,
                text="page down",
                command=lambda new_page=page + 1: self.render_pages(
                    new_page, items, frame, function
                ),
            )
            down_button.place(relx=0, relheight=btn_size, rely=1 - btn_size, relwidth=1)
            self.fit_font(down_button,"page down")

    def clear_subframes(self, subframe: ttk.Frame):
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
            relheight=0.1, relx=0, rely=0,relwidth=0.4
        )
        vault_name_entry = tk.Entry(new_vault_popup)

        vault_name_entry.place(relheight=0.15, relwidth=1, relx=0, rely=0.1)

        vault_type = tk.StringVar(value="local")

        tk.Label(new_vault_popup, text="vault type").place(
            relheight=0.1, relx=0, rely=0.27,relwidth=0.4
        )
        tk.Radiobutton(
            new_vault_popup, text="Local", value="local", variable=vault_type
        ).place(relheight=0.1, relx=0, rely=0.4,relwidth=0.4)
        tk.Radiobutton(
            new_vault_popup, text="server", value="server", variable=vault_type
        ).place(relheight=0.1, relx=0.5, rely=0.4,relwidth=0.4)

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
            with open(save_dir) as file:
                save = json.load(file)
            
            save.setdefault("services", {})
            with open(save_dir,"w") as file:
                json.dump(save,file,indent=2)
            new_vault_popup.destroy()
            self.vaults[vault_name] = {
                "directories":[key_dir,save_dir],
                "type":"local"
                
            }
            self.vault_names.append(vault_name)
            self.load_vaults(0)

        tk.Button(new_vault_popup, text="choose locations", command=add_vault).place(
            relheight=0.1, rely=0.5, relx=0,relwidth=0.3
        )
        new_vault_popup.after(10,self.apply_fonts,new_vault_popup)
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
                data = json.load(f)

                services = list(data["services"].keys())

        elif vault["type"] == "server":
            print("not yet implemented")
        else:
            print(f"{vault['type']} is not a valid save type.")

        self.render_pages(0, services, self.subframe_2, self.open_service)

    
    def add_service(self):
        new_service_popup = tk.Toplevel(
            self.root,
        )
        self.scale_toplevel(new_service_popup, 0.5)

        name_entry = tk.Entry(new_service_popup)
        name_entry.place(relheight=0.1, relx=0, rely=0.1,relwidth=1)
        tk.Label(new_service_popup, text="Name").place(relheight=0.1, relx=0, rely=0,relwidth=0.5)

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
        ).place(relheight=0.1, rely=0.3, relx=0,relwidth=0.5)
        
        new_service_popup.after(10,self.apply_fonts,new_service_popup)
        new_service_popup.transient(self.root)
        new_service_popup.grab_set

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
            self.render_pages(0, Mails, self.subframe_3, self.open_mail)

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
            password_Label.configure(text=decrypted_password)

        tk.Button(mail_popup, text="decrypt Password", command=decrypt_password).place(
            relx=0.3, rely=0.15, relheight=0.15
        )
        def update_password():
            new_data_popup = tk.Toplevel(self.root)
            self.scale_toplevel(new_data_popup,0.3)
            mail = name[0]
            new_name_entry = tk.Entry(new_data_popup)
            new_name_entry.insert(0,mail)
            new_name_entry.place(relx=0,relheight=0.1,rely=0.1,relwidth=1)
            tk.Label(
                new_data_popup,
                text="new_mail"
                ).place(relx=0,rely=0,relheight=0.1)
            new_password_entry = tk.Entry(new_data_popup)
            tk.Label(
                new_data_popup,
                text="new Password"
            ).place(relx=0,relheight=0.1,rely=0.2)
            new_password_entry.place(relx=0,relheight=0.1,rely=0.3,relwidth=1)
            
            new_master_entry = tk.Entry(new_data_popup)
            tk.Label(new_data_popup,text="new Master password").place(relx=0,relheight=0.1,rely=0.4)
            new_master_entry.place(relx=0,rely=0.5,relheight=0.1,relwidth=1)
            
            def call_encryption():
                new_master = new_master_entry.get()
                new_name = new_name_entry.get()
                new_password = new_password_entry.get()
                
                if not new_master or not new_name or not new_password:
                    messagebox.showerror("Error","No field can be left empty")
                    return
                encrypt(
                    new_master.encode(),
                    new_password.encode(),
                    self.selected_service,
                    self.selected_vault,
                    name[0],
                    int(name[1]),
                    True,
                    new_name)
                new_data_popup.destroy()

            tk.Button(new_data_popup,command=call_encryption,text="continue").place(relx=0,rely=0.6,relheight=0.1)
            
            
            new_data_popup.transient(self.root)
            new_data_popup.grab_set
        
        tk.Button(mail_popup, text="change Password",
                  command=update_password).place(
                      relx=0.6,rely=0.15,relheight=0.15
                  )

        
        mail_popup.transient(self.root)
        mail_popup.grab_set

    def add_mail(self):
        add_mail_popup = tk.Toplevel(self.root)
        self.scale_toplevel(add_mail_popup,0.5)
        
        name_entry = tk.Entry(add_mail_popup)
        tk.Label(add_mail_popup,text="Email").place(relx=0,rely=0,relheight=0.15)
        name_entry.place(relheight=0.15,relx=0,rely=0.15,relwidth=0.4)
        
        password_entry = tk.Entry(add_mail_popup)
        tk.Label(add_mail_popup,text="Password").place(relx=0,relheight=0.15,rely=0.3)
        password_entry.place(relx=0,rely=0.45,relheight=0.15,relwidth=1)
        
        master_password_entry = tk.Entry(add_mail_popup)
        tk.Label(add_mail_popup,text="Masterpassword").place(relx=0,rely=0.6,relheight=0.1)
        master_password_entry.place(relx=0,rely=0.7,relheight=0.1,relwidth=1)
        
        def add_entry():
            name= name_entry.get()
            service = self.selected_service
            vault = self.selected_vault
            password = password_entry.get()
            master = master_password_entry.get()
            encrypt(master.encode(),password.encode(),service,vault,name,1,False,name)
            add_mail_popup.destroy()
            self.open_service(self.selected_service)
            
                    
        tk.Button(add_mail_popup,text="add",command=add_entry).place(relx=0,rely=0.8,relheight=0.1)
        add_mail_popup.after(10,self.apply_fonts,add_mail_popup)
        add_mail_popup.transient(self.root)
        add_mail_popup.grab_set

    def scale_toplevel(self, window: tk.Toplevel, size: float):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        width = int(screen_width * size)
        height = int(screen_height * size)
        x = int((screen_width - width) * 0.5)
        y = int((screen_height - height) * 0.5)
        window.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    App()
