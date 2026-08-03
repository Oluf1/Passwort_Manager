import json
import random
import secrets
import string
import tkinter as tk
from pathlib import Path 
from tkinter import messagebox, simpledialog
from typing import Callable

from decrypt import decrypt
from encrypt import encrypt
#from managers import ConfigManager, ThemeManager,VaultManager,
import managers
from UI import  UI_handler



class App:
    CONFIG = managers.CONFIG
    THEME_MANAGER = managers.THEME_MANAGER
    VAULTMANAGER = managers.VAULT_MANAGER
    FONT_MANAGER = managers.FONT_MANAGER
    
    def __init__(self):
        self.ui_handler = UI_handler(self.FONT_MANAGER,
                                    self.THEME_MANAGER,
                                    self.CONFIG,
                                    self.VAULTMANAGER,
                                    self)
        
        self.root = self.ui_handler.root#unsure of wether this should be moved to setup
        
        self.frame_handler = self.ui_handler.frame_handler
        
        self.setup()


        self.root.mainloop()

    def setup(self): #KEEP
        
        
        self.VAULTMANAGER.load_vaults() 
        self.selected_vault = ""
        self.selected_service = ""
        self.supported_kdfs = ["Argon2", "PBKDF2"]
        self.THEME_MANAGER.change_theme(self.CONFIG.theme_name)
        
    
        self.ui_handler.load_main_menu()


    
    def open_vault_config(self, vault_name: str): #move (UI hanlder)
        vault = self.VAULTMANAGER.vaults[vault_name]
        key_location = vault.key_path
        
        if vault.vault_type == "local":
            save_file_location = vault.data_path
        elif vault.vault_type == "server":
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
            self.VAULTMANAGER.delete_vault(vault_name)
            self.ui_handler.load_config()

        tk.Button(self.frame_handler.subframe_3, text="delete", command=delete_vault).place(
            relheight=0.1, relwidth=1, relx=0, rely=0
        )

        self.FONT_MANAGER.apply_fonts(self.frame_handler.subframe_3)


    def new_vault(self): #move (UI handler)
        new_vault_popup = tk.Toplevel(self.root)
        new_vault_popup.title("New Vault")
        new_vault_popup.configure(bg="gray74")
        self.ui_handler.scale_toplevel(new_vault_popup, 0.5)

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

        def add_vault(): # move (vault_manager) partially done
            if vault_type.get() == "server":
                messagebox.showerror("Error", "Server saving not yet implemented")
                return
            vault_name = vault_name_entry.get()
            
            self.VAULTMANAGER.create_vault(vault_name)
            
            new_vault_popup.destroy()
            self.ui_handler.load_vaults(0)

        tk.Button(new_vault_popup, text="choose locations", command=add_vault).place(
            relheight=0.1, rely=0.5, relx=0, relwidth=0.3
        )
        new_vault_popup.after(10, self.FONT_MANAGER.apply_fonts, new_vault_popup)
        new_vault_popup.transient(self.root)
        new_vault_popup.grab_set()


    def add_service(self): #KEEP UI
        new_service_popup = tk.Toplevel(
            self.root,
        )
        self.ui_handler.scale_toplevel(new_service_popup, 0.5)

        name_entry = tk.Entry(new_service_popup)
        name_entry.place(relheight=0.1, relx=0, rely=0.1, relwidth=1)
        tk.Label(new_service_popup, text="Name").place(
            relheight=0.1, relx=0, rely=0, relwidth=0.5
        )

        def create_service():# move (password_data_manager)
            new_name = name_entry.get()

            services: list[str] = []
            vault = self.VAULTMANAGER.vaults[self.selected_vault]
            if vault.vault_type == "local":
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
                self.ui_handler.open_vault(self.selected_vault)

        tk.Button(
            new_service_popup, command=create_service, text="create service"
        ).place(relheight=0.1, rely=0.3, relx=0, relwidth=0.5)

        new_service_popup.after(10, self.FONT_MANAGER.apply_fonts, new_service_popup)
        new_service_popup.transient(self.root)
        new_service_popup.grab_set()

    def open_service(self, name: str):# KEEP
        self.selected_service = name

        self.frame_handler.clear_subframes(self.frame_handler.subframe_3)

        vault = self.VAULTMANAGER.vaults[self.selected_vault]
        Mails: list = []
        if vault.vault_type == "local":
            location = vault.data_path
            with open(location) as f:
                data = json.load(f)

            for ele in data["services"][name]:
                Mails.append((ele["Mail"], ele["count"]))
            self.ui_handler.render_pages(0, Mails, self.frame_handler.subframe_3, self.open_mail, self.add_mail)

    def open_mail(self, name: str): #KEEP UI
        mail_popup = tk.Toplevel(self.root)

        self.ui_handler.scale_toplevel(mail_popup, 0.5)
        mail_popup.title(name)

        tk.Label(mail_popup, text=f"service: {self.selected_service}").place(
            relx=0, rely=0, relheight=0.15
        )
        password_Label = tk.Label(mail_popup, text="password: *****")
        password_Label.place(relx=0, relheight=0.15, rely=0.15)

        def decrypt_password():# move (password_data_manager)
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
                master_password, self.selected_service, Mail, count, self.selected_vault,self
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

        def update_password():# move (password_data_manager)
            new_data_popup = tk.Toplevel(self.root)
            self.ui_handler.scale_toplevel(new_data_popup, 0.3)
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
                    self
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

    def add_mail(self): # KEEP UI
        add_mail_popup = tk.Toplevel(self.root)
        self.ui_handler.scale_toplevel(add_mail_popup, 0.5)

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

        def add_entry():# move (password_data_manager)

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
                master.encode(), password.encode(), service, vault, name, 1, False, name,self
            )
            add_mail_popup.destroy()
            self.open_service(self.selected_service)

        tk.Button(add_mail_popup, text="add", command=add_entry).place(
            relx=0, rely=0.9, relheight=0.1
        )
        add_mail_popup.after(10, self.FONT_MANAGER.apply_fonts, add_mail_popup)
        add_mail_popup.transient(self.root)
        add_mail_popup.grab_set()

    

if __name__ == "__main__":
    App()
