import tkinter as tk
from encrypt import encrypt
class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x400")
        
        self.Load_StartUI()
        self.root.mainloop()
    
    def Remove_Widgets(self):
        for widget in self.root.winfo_children():
            widget.place_forget()
    def Load_StartUI(self):
        self.Remove_Widgets()
        Select_encryption = tk.Button(self.root,text="encryption",command=self.Load_EncryptionUI)
        
        Select_encryption.place(x=300,y=200)
    def Load_EncryptionUI(self):
        self.Remove_Widgets() 
        retun_Button = tk.Button(self.root,command=self.Load_StartUI,text="return")
        Password_Entry = tk.Entry(self.root)
        Master_Password_Entry = tk.Entry(self.root)
        Service_Entry = tk.Entry(self.root)
        Mail_Entry = tk.Entry(self.root)
        Mail_Label = tk.Label(self.root,text="Email")
        Service_Label = tk.Label(self.root,text="Service")
        Password_Label = tk.Label(self.root,text="Password")
        Master_Password_Label = tk.Label(self.root,text="Master Password")
        def Get_EntryValues():
            Password = Password_Entry.get()
            Master_Password = Master_Password_Entry.get()
            Mail = Mail_Entry.get()
            Service = Service_Entry.get()
            self.Call_Encryption(Service,Mail,Password,Master_Password)
        
        Encrypt_Button = tk.Button(self.root,text="Encrypt",command=Get_EntryValues)
        
        Master_Password_Entry.place(x=250,y=175,width=100)
        Master_Password_Label.place(x=250,y=200,height=25)
        Mail_Entry.place(x=250,y=150,width=100)
        Mail_Label.place(x=250,y=125,height=25)
        Service_Entry.place(x=150,y=150,width=100)
        Service_Label.place(x=150,y=125,height=25)
        Password_Entry.place(x=350,y=150,width=100)
        Password_Label.place(x=350,y=125,height=25)
        Encrypt_Button.place(x=275,y=225,height=25)
        retun_Button.place(x=0,y=0)  
        
    def Call_Encryption(self,Service:str,Mail:str,Password:str,Master_Password:str): 
         encrypt(Master_Password.encode(),Password.encode(),Service.encode(),Mail.encode())

if __name__ == "__main__":
    App()