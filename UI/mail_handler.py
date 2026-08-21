from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .UI_handler import UI_handler
import random
import secrets
import string
import tkinter as tk
from tkinter import messagebox, simpledialog

from decrypt import decrypt
from encrypt import encrypt


class MailManager:
    def __init__(self,ui_handler:"UI_handler"):
        self.ui_handler = ui_handler
    def open_mail(self, name: str):  # KEEP UI
        mail_popup = self.ui_handler.create_popup(name)

        big_font = ("Arial", 16)
        button_font = ("Arial", 14, "bold")

        tk.Label(
            mail_popup,
            text=f"service: {self.ui_handler.app.selected_service}",
            font=big_font
        ).place(
            relx=0, rely=0, relheight=0.15, relwidth=1
        )

        asterisk_str = "*" * (random.randint(0, 4) + 5)

        password_Label = tk.Label(
            mail_popup,
            text=f"password: {asterisk_str}",
            font=big_font
        )
        password_Label.place(
            relx=0, rely=0.15, relheight=0.15, relwidth=1
        )

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
            try:
                decrypted_password = decrypt(
                    master_password,
                    self.ui_handler.app.selected_service,
                    Mail,
                    count,
                    self.ui_handler.app.selected_vault,
                    self.ui_handler.app
                )
            except Exception as error:
                self.ui_handler.show_error(error)

            password_Label.configure(text=f"Password: {decrypted_password}")

            self.ui_handler.root.clipboard_clear()
            self.ui_handler.root.clipboard_append(decrypted_password)

            self.ui_handler.root.after(
                30000,
                lambda: (
                    self.ui_handler.root.clipboard_clear(),
                    self.ui_handler.root.clipboard_append("")
                ),
            )

        tk.Button(
            mail_popup,
            text="decrypt Password",
            font=button_font,
            command=decrypt_password
        ).place(
            relx=0.2,
            rely=0.35,
            relheight=0.15,
            relwidth=0.25
        )


        def update_password():
            new_data_popup = self.ui_handler.create_popup("new password",0.3)

            popup_font = ("Arial", 14) #?????
            mail = name[0]
            tk.Label(
                new_data_popup,
                text="new mail",
                font=popup_font
            ).place(
                relx=0, rely=0, relheight=0.1, relwidth=1
            )

            new_name_entry = tk.Entry(
                new_data_popup,
                font=popup_font
            )
            new_name_entry.insert(0, mail)
            new_name_entry.place(
                relx=0,
                rely=0.1,
                relheight=0.1,
                relwidth=1
            )

            tk.Label(
                new_data_popup,
                text="new Password",
                font=popup_font
            ).place(
                relx=0,
                rely=0.2,
                relheight=0.1,
                relwidth=1
            )

            new_password_entry = tk.Entry(
                new_data_popup,
                font=popup_font
            )

            def generate_password():
                length = random.randint(0, 8) + 30
                alphabet = string.ascii_letters + string.digits + string.punctuation
                password = "".join(
                    secrets.choice(alphabet)
                    for _ in range(length)
                )

                new_password_entry.delete(0, tk.END)
                new_password_entry.insert(0, password)

            tk.Button(
                new_data_popup,
                text="generate password",
                font=button_font,
                command=generate_password
            ).place(
                relx=0.5,
                rely=0.3,
                relheight=0.1,
                relwidth=0.5
            )

            new_password_entry.place(
                relx=0,
                rely=0.3,
                relheight=0.1,
                relwidth=0.5
            )

            tk.Label(
                new_data_popup,
                text="new Master password",
                font=popup_font
            ).place(
                relx=0,
                rely=0.45,
                relheight=0.1,
                relwidth=1
            )

            new_master_entry = tk.Entry(
                new_data_popup,
                font=popup_font
            )

            new_master_entry.place(
                relx=0,
                rely=0.55,
                relheight=0.1,
                relwidth=1
            )

            def call_encryption():
                new_master = new_master_entry.get()
                new_name = new_name_entry.get()
                new_password = new_password_entry.get()

                if not new_master or not new_name or not new_password:
                    messagebox.showerror(
                        "Error",
                        "No field can be left empty"
                    )
                    return
                try:
                    encrypt(
                        new_master.encode(),
                        new_password.encode(),
                        self.ui_handler.app.selected_service,
                        self.ui_handler.app.selected_vault,
                        name[0],
                        int(name[1]),
                        True,
                        new_name,
                        self.ui_handler.app
                    )
                except Exception as error:
                    self.ui_handler.show_error(error)
                new_data_popup.destroy()
                mail_popup.destroy()
                self.open_mail(name)

            tk.Button(
                new_data_popup,
                text="continue",
                font=button_font,
                command=call_encryption
            ).place(
                relx=0,
                rely=0.7,
                relheight=0.15,
                relwidth=1
            )



        tk.Button(
            mail_popup,
            text="change Password",
            font=button_font,
            command=update_password
        ).place(
            relx=0.55,
            rely=0.35,
            relheight=0.15,
            relwidth=0.3
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
            service = self.ui_handler.app.selected_service
            vault = self.ui_handler.app.selected_vault
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
                master.encode(), password.encode(), service, vault, name, 1, False, name,self.ui_handler.app
            )
            add_mail_popup.destroy()
            self.ui_handler.open_service(self.ui_handler.app.selected_service)

        tk.Button(add_mail_popup, text="add", command=add_entry).place(
            relx=0, rely=0.9, relheight=0.1
        )

