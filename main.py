import json
import random
import secrets
import string
import tkinter as tk
from pathlib import Path 
from tkinter import messagebox, simpledialog

from decrypt import decrypt
from encrypt import encrypt
import managers
from UI.UI_handler import UI_handler



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
        
        self.root = self.ui_handler.root #unsure of wether this should be moved to setup
        
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


    def open_mail(self, name: str): #KEEP UI
        mail_popup = self.ui_handler.create_popup(name)


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


    def add_mail(self): # KEEP UI
        add_mail_popup = self.ui_handler.create_popup("add mail")

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
            self.ui_handler.open_service(self.selected_service)

        tk.Button(add_mail_popup, text="add", command=add_entry).place(
            relx=0, rely=0.9, relheight=0.1
        )


    

if __name__ == "__main__":
    App()
