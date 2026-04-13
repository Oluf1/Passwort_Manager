import json
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from encrypt import encrypt
from decrypt import decrypt


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x400")
        self.vaults ={}
        with open("config.json") as f:
            self.vaults = json.load(f)["Vaults"]
        #for ele in self.vaults:
         #   self.vaults[ele]["directories"][0]
          #  self.vaults[ele]["directories"][1]
        #with open("exampledata.json") as f:
        #    self.database = json.load(f)

        #self.existing_services = [
        #    (entry["Service"], entry["Mail"], entry["count"])
        #    for entry in self.database["Entries"]
        #]
        
        
        border_width = 2
        self.main_frame = ttk.Frame(self.root,borderwidth=border_width,relief="solid")
        self.main_frame.place(relheight=1,relwidth=0.2,relx=0,rely=0)
        self.subframe_1 = ttk.Frame(self.root,borderwidth=border_width,relief="solid")
        self.subframe_1.place(relheight=1,relwidth=0.15,relx=0.2,rely=0)
        self.subframe_2 = ttk.Frame(self.root,borderwidth=border_width,relief="solid")
        self.subframe_2.place(relheight=1,relwidth=0.25,relx=0.35,rely=0)
        self.subframe_3 = ttk.Frame(self.root,borderwidth=border_width,relief="solid")
        self.subframe_3.place(relheight=1,relwidth=0.4,relx=0.6)
        self.load_start_ui()
        self.root.mainloop()

    def fit_font(self,label: tk.Label,
                text: str):
        label.update_idletasks()
        label_width = label.winfo_width()
        max_size = 100
        min_size= 1
        low = min_size
        high = max_size
        best = min_size
        font = tkfont.Font(family="Arial", size=1,)
        while low <= high:
            middle = (low + high)//2
            font.config(size=middle)
            text_width = font.measure(text)
            if text_width <= label_width:
                best = middle
                low = middle+1
            else:
                high = middle-1
        font.configure(size=best)
        label.config(font=font,text=text)

    def load_start_ui(self):
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)
        
        name_label = tk.Label(self.main_frame)
        open_vaults_button = tk.Button(self.main_frame,
                                       text="Vaults",bg="royalblue",
                                       command=self.load_vaults)
        name_label.place(relx=0,rely=0,relwidth=0.95)
        config_button = tk.Button(self.main_frame,text="config",bg="lightgrey")
        open_vaults_button.place(relx=0,rely=0.1,relwidth=1,relheight=0.1,)
        config_button.place(relx=0,rely=0.21,relwidth=1,relheight=0.1)
        self.root.after(10, lambda: self.fit_font(name_label, "Password Manager"))
        
    def load_vaults(self):
        self.vault_buttons : list[tk.Button] = []
        counter = 0
        for vault in self.vaults:
            if counter ==0:
                new_vault_button = tk.Button(self.subframe_1,
                                             command=self.add_vault,
                                             text="New Vault")
                self.vault_buttons.append(new_vault_button)
                counter+=1
            elif counter%20 ==0:
                up_button = tk.Button(self.subframe_1,text="previous page",
                                      command= lambda page = counter//18 -1: self.place_Vaults(page))
                self.vault_buttons.append(up_button)
                counter+=1
            elif (counter+1) % 20 ==0 and counter/20 != len(self.vaults)/18:
                down_button = tk.Button(self.subframe_1,text="next page",
                                      command= lambda page = counter//18 +1: self.place_Vaults(page))
                self.vault_buttons.append(down_button)
                counter += 1
            vault_button = tk.Button(self.subframe_1,command= lambda name=vault: self.open_vault(name),text=vault)
            self.vault_buttons.append(vault_button)
            counter +=1 
        self.place_Vaults(0)
        
            
    def place_Vaults(self,page:int):
        self.clear_subframes(self.subframe_1)
        if page == len(self.vaults)//18:
            for i in range(len(self.vaults)+1):
                button = self.vault_buttons[i+20*page]
                button.place(rely=0.05*i,relwidth=1,relheight=0.045)
        else:
            for i in range(20):
                button = self.vault_buttons[i+20*page]
                button.place(rely=0.05*i,relwidth=1,relheight=0.045)
    def clear_subframes(self,subframe:ttk.Frame):
            for widget in subframe.winfo_children():
                widget.place_forget() #type: ignore
    def add_vault(self): 
        pass
    def open_vault(self,name:str):
        print(name)
        


if __name__ == "__main__":
    App()