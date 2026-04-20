import json
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from typing import Callable
from tkinter import messagebox
from tkinter import filedialog
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
        self.selected_vault =""
        self.render_pages(0, self.vault_names, self.subframe_1, self.open_vault)

    def render_pages(
        self, page: int, items: list, frame: ttk.Frame, function: Callable
    ):
        self.clear_subframes(frame)
        start = page * self.items_per_page
        end = start + self.items_per_page
        btn_size = 1/ (self.items_per_page +2)
        current_items = items[start:end]
        if page == 0:
            match frame:
                case self.subframe_1:
                    new_vault_button = tk.Button(
                        self.subframe_1, text="Add vault", command=self.new_vault
                    )
                    new_vault_button.place(relx=0, rely=0, relwidth=1, relheight=btn_size)
                case self.subframe_2:
                    add_service_button = tk.Button(
                        self.subframe_2, text="Add Service", command=self.add_service
                    )
                    add_service_button.place(relx=0, rely=0, relwidth=1, relheight=btn_size)
                case self.subframe_3:
                    add_mail_button = tk.Button(
                        self.subframe_3,text="add Mail",command=self.add_mail
                    )
                    add_mail_button.place(relx=0, rely=0, relwidth=1, relheight=btn_size)
                case _:
                    print("error wrong subframe in render_pages")
        else:
            up_button = tk.Button(
                frame,
                text="page up",
                command=lambda new_page = page-1: self.render_pages(new_page, items, frame, function),
            )
            up_button.place(relx=0, rely=0, relwidth=1, relheight=btn_size)
        for i, name in enumerate(current_items):
            button = tk.Button(frame, text=name, command=lambda temp_name = name: function(temp_name))
            button.place(relheight=0.05, relx=0, relwidth=1, rely=btn_size + btn_size * i)
        if len(current_items )> len(items):
            down_button = tk.Button(
                frame,
                text="page down",
                command=lambda new_page = page+1: self.render_pages(new_page,items,frame,function)
            )
            down_button.place(relx=0,relheight=btn_size,rely=1-btn_size,relwidth=1)


    def clear_subframes(self, subframe: ttk.Frame):
        for widget in subframe.winfo_children():
            widget.destroy()

    def new_vault(self):
        new_vault_popup = tk.Toplevel(self.root)
        new_vault_popup.title("New Vault")
        new_vault_popup.configure(bg='gray74')
        self.scale_toplevel(new_vault_popup,0.5)
        
        tk.Label(new_vault_popup,text="New vault Name").place(relheight=0.1,relx=0,rely=0)
        vault_name_entry = tk.Entry(new_vault_popup)
        
        vault_name_entry.place(relheight=0.15,relwidth=1,relx=0,rely=0.1)
        
        vault_type =tk.StringVar(value="local")
        
        tk.Label(new_vault_popup,text="vault type").place(relheight=0.1,relx=0,rely=0.27)
        tk.Radiobutton(new_vault_popup,text="Local",value="local",variable=vault_type).place(relheight=0.1,relx=0,rely=0.4)
        tk.Radiobutton(new_vault_popup,text="server",value="server",variable=vault_type).place(relheight=0.1,relx=0.5,rely=0.4)
        
        def add_vault():
            if vault_type.get() == "server":
                messagebox.showerror("Error","Server saving not yet implemented")
                return
            vault_name = vault_name_entry.get()
            if vault_name in self.vault_names:
                messagebox.showerror("Error","Vault name already exists choose another")
                return
            save_dir = filedialog.askopenfilename(initialdir="/",
                                                 title="select save directory",
                                                 filetypes = (("json files",
                                                        "*.json*"),))
            key_dir = filedialog.askopenfilename(initialdir="/",
                                                 title="select key directory",
                                                 filetypes = (("Text files",
                                                        "*.txt*"),))
            if not save_dir or not key_dir:
                messagebox.showerror("Error", "No directory selected")
                return
            with open("config.json")as config:
                data = json.load(config)
            data["Vaults"][vault_name] = {"directories":
                                    [
                                        key_dir,
                                        save_dir
                                    ],
                                    "type":"local"
                                }
            with open("config.json", "w") as file:
                json.dump(data,file,indent=2)
            
            new_vault_popup.destroy()
            self.vault_names.append(vault_name)
            self.load_vaults(0)
        
        tk.Button(new_vault_popup,text="choose locations",command=add_vault).place(relheight=0.1,rely=0.5,relx=0)
        
        
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
        new_service_popup = tk.Toplevel(self.root,)
        self.scale_toplevel(new_service_popup,0.5)
        
        name_entry = tk.Entry(new_service_popup)
        name_entry.place(relheight=0.1,relx=0,rely=0.1)
        tk.Label(new_service_popup,text="Name").place(relheight=0.1,relx=0,rely=0)
        
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
                with open(location,"w") as file:
                    json.dump(data,file,indent=2) 
                self.open_vault(self.selected_vault)

        
        tk.Button(new_service_popup,command=create_service,
                  text="create service").place(relheight=0.1,rely=0.3,relx=0)
        
        
        
        new_service_popup.transient(self.root)
        new_service_popup.grab_set
        
    def open_service(self,name:str):
        self.selected_service = name
        
        self.clear_subframes(self.subframe_3)

        vault = self.vaults[self.selected_vault]
        Mails:list[str] = []
        if vault["type"] == "local":
            location = vault["directories"][1]
            with open(location) as f:
                data = json.load(f)
            
            
            for ele in data["services"][name]:
                Mails.append(ele["Mail"])
            self.render_pages(0,Mails,self.subframe_3,self.open_mail)
        
    def open_mail(self,name:str):
        mail_popup = tk.Toplevel(self.root)
        
        
        self.scale_toplevel(mail_popup,0.5)
        mail_popup.title(name)
        
        tk.Label(mail_popup,
                 text=f"service: {self.selected_service}"
                 ).place(relx=0,rely=0,relheight=0.15)
        password_Label =tk.Label(mail_popup,text="password: ****")
        password_Label.place(relx=0,relheight=0.15,rely=0.15)
        tk.Button(mail_popup,text="decrypt Password").place(relx=0.3,rely=0.15,relheight=0.15)
        
        mail_popup.transient(self.root)
        mail_popup.grab_set
    def scale_toplevel(self,window:tk.Toplevel,size:float):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        width = int(screen_width * size)
        height = int(screen_height * size)
        x = int((screen_width - width) *size)
        y = int((screen_height - height) *size)
        window.geometry(f"{width}x{height}+{x}+{y}")
    def add_mail(self):
        pass
            
            

if __name__ == "__main__":
    App()
