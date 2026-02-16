import tkinter as tk
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
        Encrypt_Entry = tk.Button(self.root,text="Submit Password")
        
        Password_Entry.place(x=225,y=150,width=200)#Feels not to be centred very Well too lazy to adjust
        Encrypt_Entry.place(x=275,y=175,height=50)
        retun_Button.place(x=0,y=0)   

if __name__ == "__main__":
    App()