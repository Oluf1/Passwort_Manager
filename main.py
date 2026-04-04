import json
import tkinter as tk
from tkinter import ttk

from encrypt import encrypt
from decrypt import decrypt


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x400")

        with open("exampledata.json") as f:
            self.database = json.load(f)

        self.existing_services = [
            (entry["Service"], entry["Mail"], entry["count"])
            for entry in self.database["Entries"]
        ]

        self.load_start_ui()
        self.root.mainloop()

    def remove_widgets(self):
        for widget in self.root.winfo_children():
            widget.place_forget()  # type: ignore

        return_button = tk.Button(self.root, command=self.load_start_ui, text="Return")
        return_button.place(x=0, y=0)

    def load_start_ui(self):
        self.remove_widgets()

        encryption_button = tk.Button(self.root, text="Encryption", command=self.load_encryption_ui)
        decryption_button = tk.Button(self.root, text="Decryption", command=self.load_decryption_ui)

        encryption_button.place(x=300, y=200)
        decryption_button.place(x=200, y=200)

    def load_encryption_ui(self):
        self.remove_widgets()

        password_entry = tk.Entry(self.root)
        master_password_entry = tk.Entry(self.root)
        service_entry = tk.Entry(self.root)
        mail_entry = tk.Entry(self.root)

        mail_label = tk.Label(self.root, text="Email")
        service_label = tk.Label(self.root, text="Service")
        password_label = tk.Label(self.root, text="Password")
        master_password_label = tk.Label(self.root, text="Master Password")

        def get_entry_values():
            password = password_entry.get()
            master_password = master_password_entry.get()
            mail = mail_entry.get()
            service = service_entry.get()
            count = 1

            for entry in self.database["Entries"]:
                if entry["Service"] == service and entry["Mail"] == mail:
                    count += 1

            self.existing_services.append((service, mail, count))
            encrypt(master_password.encode(), password.encode(), service, mail, count, False)

        update_existing_button = tk.Button(self.root, text="Update Existing", command=self.load_update_existing_ui)
        encrypt_button = tk.Button(self.root, text="Encrypt", command=get_entry_values)

        update_existing_button.place(x=275, y=250)
        master_password_entry.place(x=250, y=175, width=100)
        master_password_label.place(x=250, y=200, height=25)
        mail_entry.place(x=250, y=150, width=100)
        mail_label.place(x=250, y=125, height=25)
        service_entry.place(x=150, y=150, width=100)
        service_label.place(x=150, y=125, height=25)
        password_entry.place(x=350, y=150, width=100)
        password_label.place(x=350, y=125, height=25)
        encrypt_button.place(x=275, y=225, height=25)

    def load_update_existing_ui(self):
        self.remove_widgets()

        service_combobox = ttk.Combobox(self.root, values=self.existing_services)
        new_password_entry = tk.Entry(self.root)
        master_password_entry = tk.Entry(self.root)
        new_password_label = tk.Label(self.root, text="New Password")
        master_password_label = tk.Label(self.root, text="Master Password")

        def get_entry_values():
            index = service_combobox.current()
            service, mail, count = self.existing_services[index]
            password = new_password_entry.get()
            master_password = master_password_entry.get()
            encrypt(master_password.encode(), password.encode(), service, mail, count, True)

        update_button = tk.Button(self.root, text="Update", command=get_entry_values)

        update_button.place(x=250, y=225)
        new_password_label.place(x=350, y=125)
        new_password_entry.place(x=350, y=150)
        master_password_label.place(x=250, y=175)
        master_password_entry.place(x=250, y=200)
        service_combobox.place(x=150, y=150, width=180)

    def load_decryption_ui(self):
        self.remove_widgets()

        service_combobox = ttk.Combobox(self.root, values=self.existing_services)
        master_password_entry = tk.Entry(self.root)
        service_label = tk.Label(self.root, text="Service")
        master_password_label = tk.Label(self.root, text="Master Password")

        def get_entry_values():
            master_password = master_password_entry.get()
            index = service_combobox.current()
            service, mail, count = self.existing_services[index]
            decrypt(master_password.encode(), service, mail, count)

        decrypt_button = tk.Button(self.root, command=get_entry_values, text="Decrypt")

        master_password_entry.place(x=350, y=150, width=100)
        master_password_label.place(x=350, y=125, height=25)
        service_combobox.place(x=150, y=150, width=180)
        service_label.place(x=150, y=125, height=25)
        decrypt_button.place(x=275, y=175)


if __name__ == "__main__":
    App()