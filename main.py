import tkinter as tk
from encrypt import encrypt
from decrypt import decrypt
from tkinter import ttk
import json

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x400")
        with open("exampledata.json") as f:
            self.Database = json.load(f)
        self.Existing_Services = []
        for entry in self.Database["Entries"]:
            self.Existing_Services.append((entry["Service"],entry["Mail"],entry["count"]))

        self.Load_StartUI()
        
        self.root.mainloop()
    
    def Remove_Widgets(self):
        for widget in self.root.winfo_children():
            widget.place_forget()
        retun_Button = tk.Button(self.root,command=self.Load_StartUI,text="return")
        retun_Button.place(x=0,y=0) 
    def Load_StartUI(self):
        self.Remove_Widgets()
        Select_encryption = tk.Button(self.root,text="encryption",command=self.Load_EncryptionUI)
        Select_Decryption = tk.Button(self.root,text="decryption",command=self.Load_Decryption)
        Select_Decryption.place(x=200,y=200)
        Select_encryption.place(x=300,y=200)
    def Load_EncryptionUI(self):
        self.Remove_Widgets() 
        Password_Entry = tk.Entry(self.root)
        Master_Password_Entry = tk.Entry(self.root)
        Service_Entry = tk.Entry(self.root)
        Mail_Entry = tk.Entry(self.root)
        Mail_Label = tk.Label(self.root,text="Email")
        Service_Label = tk.Label(self.root,text="Service")
        Password_Label = tk.Label(self.root,text="Password")
        Master_Password_Label = tk.Label(self.root,text="Master_Password")
        
        def Get_EntryValues():
            Password = Password_Entry.get()
            Master_Password = Master_Password_Entry.get()
            Mail = Mail_Entry.get()
            Service = Service_Entry.get()
            count = 1
            for entry in self.Database["Entries"]:
                if entry["Service"] == Service and entry["Mail"]== Mail :    
                    count+=1
            self.Existing_Services.append(Service,Mail,count)
            encrypt(Master_Password.encode(),Password.encode(),Service,Mail,count,False,)

        Update_Existing_button = tk.Button(self.root,text="Update Existing", command=self.Load_EncryptionExisitingUi)
        Encrypt_Button = tk.Button(self.root,text="Encrypt",command=Get_EntryValues)
        
        Update_Existing_button.place(x=275,y=250)
        Master_Password_Entry.place(x=250,y=175,width=100)
        Master_Password_Label.place(x=250,y=200,height=25)
        Mail_Entry.place(x=250,y=150,width=100)
        Mail_Label.place(x=250,y=125,height=25)
        Service_Entry.place(x=150,y=150,width=100)
        Service_Label.place(x=150,y=125,height=25)
        Password_Entry.place(x=350,y=150,width=100)
        Password_Label.place(x=350,y=125,height=25)
        Encrypt_Button.place(x=275,y=225,height=25)
        
    def Load_EncryptionExisitingUi(self):
        self.Remove_Widgets()
        Service_combobox = ttk.Combobox(self.root,values=self.Existing_Services)
        new_Password_entry = tk.Entry(self.root)
        Master_Password_entry = tk.Entry(self.root)
        new_Password_Label = tk.Label(self.root,text="New Password")
        Master_Password_Label = tk.Label(self.root,text="Master password")
        
        
        
        def GetEntry_values():
            index = Service_combobox.current()
            Service = self.Existing_Services[index][0]
            Mail = self.Existing_Services[index][1]
            count = self.Existing_Services[index][2]
            password = new_Password_entry.get()
            Master_Password= Master_Password_entry.get()
            
            encrypt(Master_Password.encode(),password.encode(),Service,Mail,count,True)
        
        Update_existing_Button = tk.Button(self.root,text="update",command=GetEntry_values)
        
        Update_existing_Button.place(x=250,y=225)
        new_Password_Label.place(x=350,y=125)
        new_Password_entry.place(x=350,y=150)
        Master_Password_Label.place(x=250,y=175)
        Master_Password_entry.place(x=250,y=200)
        Service_combobox.place(x=150,y=150,width=180)
        
    def Load_Decryption(self):
        self.Remove_Widgets()
        Service_combobox = ttk.Combobox(self.root,values=self.Existing_Services)
        
        Master_password_Entry = tk.Entry(self.root)
        Service_Label = tk.Label(self.root,text="Service")
        Master_password_label = tk.Label(self.root,text="Master password")
        
        
        def Get_Entry_values():
            Master_pass = Master_password_Entry.get()
            index = Service_combobox.current()
            Service = self.Existing_Services[index][0]
            Mail = self.Existing_Services[index][1]
            count = self.Existing_Services[index][2]

            decrypt(Master_pass.encode(),Service,Mail,count)
        Decrypt_Button = tk.Button(self.root,command=Get_Entry_values,text="decrypt")
        
        Master_password_Entry.place(x=350,y=150,width=100)
        Master_password_label.place(x=350,y=125,height=25)
        Service_combobox.place(x=150,y=150,width=180)
        Service_Label.place(x=150,y=125,height=25)
        Decrypt_Button.place(x=275,y=175)
        

if __name__ == "__main__":
    App()