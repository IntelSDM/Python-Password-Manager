import tkinter as tk
from tkinter import ttk
import enum
from tkinter import messagebox
#from Client import Login
LoginWindow = tk.Tk()

LoginWindow.title("My Window")
LoginWindow.geometry("400x225")
style = ttk.Style()
style.configure('TNotebook.Tab', padding=(6, 2), font=('Segoe UI', 9))
notebook = ttk.Notebook(LoginWindow,width=400, height=225)

#Change this to save a password. then we auto read it
def RememberPasswordToggle():
    if RememberPassword == True:
        print("Checkbox is checked")
    else:
        print("Checkbox is unchecked")
class MSGReason(enum.Enum):
    Warning = 1
    Info = 2
    Error = 3
def DrawMessageBox(reason:MSGReason,header: str, information: str):
    if(reason == MSGReason.Error):
         messagebox.showerror(header, information)
    if(reason == MSGReason.Info):
         messagebox.showinfo(header, information)
    if(reason == MSGReason.Warning):
         messagebox.showwarning(header, information)

TabLogin = ttk.Frame(notebook)
notebook.add(TabLogin, text="Login")
LblLoginUsername = tk.Label(TabLogin, text="Username:",font=("Segoe UI", 10))
LblLoginUsername.place(x=150,y=0)
TxtLoginUsername = tk.Text(TabLogin, width=25, height=1)
TxtLoginUsername.place(x=85, y = 25)
LblLoginPassword = tk.Label(TabLogin, text="Password:",font=("Segoe UI", 10))
LblLoginPassword.place(x=150,y=50)
TxtLoginPassword = tk.Text(TabLogin, width=25, height=1)
TxtLoginPassword.place(x=85, y = 75)
RememberPassword = tk.IntVar()
CBRememberPassword = tk.Checkbutton(TabLogin, text="Remember Password", variable=RememberPassword, command=RememberPasswordToggle)
CBRememberPassword.place(x=85, y = 100)
BtnLogin = tk.Button(TabLogin, text="Login", command=LoginWindow.withdraw,font=("Segoe UI", 10))
BtnLogin.place(x=160,y = 130)

TabRegister = ttk.Frame(notebook)
notebook.add(TabRegister, text="Register")

LblRegisterUsername = tk.Label(TabRegister, text="Username:",font=("Segoe UI", 10))
LblRegisterUsername.place(x=150,y=0)
TxtRegisterUsername = tk.Text(TabRegister, width=25, height=1)
TxtRegisterUsername.place(x=85, y = 25)
LblRegisterPassword = tk.Label(TabRegister, text="Password:",font=("Segoe UI", 10))
LblRegisterPassword.place(x=150,y=50)
TxtRegisterPassword = tk.Text(TabRegister, width=25, height=1)
TxtRegisterPassword.place(x=85, y = 75)
BtnRegister = tk.Button(TabRegister, text="Register", command=LoginWindow.withdraw,font=("Segoe UI", 10))
BtnRegister.place(x=150,y = 100)

notebook.place(x=0, y=0)
#DrawMessageBox(MSGReason.Error,"header","Info")


