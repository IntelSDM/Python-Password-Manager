import tkinter as tk
from tkinter import ttk
import enum
from tkinter import messagebox
#from Client import Login
LoginWindow = tk.Tk()

End = tk.END

LoginWindow.title("Login")
LoginWindow.geometry("400x225")
style = ttk.Style()
style.configure('TNotebook.Tab', padding=(6, 2), font=('Segoe UI', 9))
notebook = ttk.Notebook(LoginWindow,width=400, height=225)

ProductWindow = tk.Tk()
ProductWindow.title("Manage Products")
ProductWindow.geometry("600x750")
ProductStyle = ttk.Style()
ProductStyle.configure('TNotebook.Tab', padding=(6, 2), font=('Segoe UI', 9))
ProductNotebook = ttk.Notebook(ProductWindow,width=600, height=750)
#ProductWindow.withdraw()
#Change this to save a password. then we auto read it
def RememberPasswordToggle():
    if UseSymbols.get() == True:
        print("Checkbox is checked")
    else:
        print("Checkbox is unchecked")
class MSGReason(enum.Enum):
    Warning = 1
    Info = 2
    Error = 3

def DrawMessageBox(reason:MSGReason,header: str, information: str):
    # Check the reason for the message and then create a different messagebox for different reasons
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
BtnLogin.place(x=190,y = 130)

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
LblRegisterConfirmPassword = tk.Label(TabRegister, text="Confirm Password:",font=("Segoe UI", 10))
LblRegisterConfirmPassword.place(x=128,y=100)
TxtRegisterConfirmPassword = tk.Text(TabRegister, width=25, height=1)
TxtRegisterConfirmPassword.place(x=85, y = 125)
BtnRegister = tk.Button(TabRegister, text="Register", command=LoginWindow.withdraw,font=("Segoe UI", 10))
BtnRegister.place(x=150,y = 150)

TabResetPassword = ttk.Frame(notebook)
notebook.add(TabResetPassword, text="Reset Password")
LblResetPasswordUsername = tk.Label(TabResetPassword, text="Username:",font=("Segoe UI", 10))
LblResetPasswordUsername.place(x=150,y=0)
TxtResetPasswordUsername = tk.Text(TabResetPassword, width=25, height=1)
TxtResetPasswordUsername.place(x=85, y = 25)
LblResetPasswordPassword = tk.Label(TabResetPassword, text="Password:",font=("Segoe UI", 10))
LblResetPasswordPassword.place(x=150,y=50)
TxtResetPasswordPassword = tk.Text(TabResetPassword, width=25, height=1)
TxtResetPasswordPassword.place(x=85, y = 75)
LblResetPasswordTwoFactor = tk.Label(TabResetPassword, text="Two Factor Code:",font=("Segoe UI", 10))
LblResetPasswordTwoFactor.place(x=128,y=100)
TxtResetPasswordTwoFactor = tk.Text(TabResetPassword, width=25, height=1)
TxtResetPasswordTwoFactor.place(x=85, y = 125)
BtnResetPassword = tk.Button(TabResetPassword, text="Reset Password", command=LoginWindow.withdraw,font=("Segoe UI", 10))
BtnResetPassword.place(x=130,y = 150)

TabServers = ttk.Frame(ProductNotebook)
ProductNotebook.add(TabServers, text="Server")
ServerListBox = tk.Listbox(TabServers,width = 50,height = 30)
ServerListBox.place(x=0,y = 5)
TabSupport = ttk.Frame(ProductNotebook)
BtnSelectedRemove = tk.Button(TabServers, text="Remove Account", command=ProductWindow.withdraw,font=("Segoe UI", 10))
BtnSelectedRemove.place(x=310,y=0)
LblSelectedServerName = tk.Label(TabServers, text="Username:",font=("Segoe UI", 10))
LblSelectedServerName.place(x=310,y=35)
BtnCopyServerName = tk.Button(TabServers, text="Copy Name", command=ProductWindow.withdraw,font=("Segoe UI", 10))
BtnCopyServerName.place(x=310,y = 55)
LblSelectedServerPassword = tk.Label(TabServers, text="Server Password:",font=("Segoe UI", 10))
LblSelectedServerPassword.place(x=310,y=85)
BtnCopyServerPassword = tk.Button(TabServers, text="Copy Password", command=ProductWindow.withdraw,font=("Segoe UI", 10))
BtnCopyServerPassword.place(x=310,y = 105)

LblInputServerName = tk.Label(TabServers, text="Server Name:",font=("Segoe UI", 10))
LblInputServerName.place(x=0,y=490)
TxtInputServerName = tk.Text(TabServers, width=25, height=1)
TxtInputServerName.place(x=0,y=510)

LblInputServerUsername = tk.Label(TabServers, text="Username:",font=("Segoe UI", 10))
LblInputServerUsername.place(x=0,y=530)
TxtInputServerUsername = tk.Text(TabServers, width=25, height=1)
TxtInputServerUsername.place(x=0,y=550)

LblInputServerPassword = tk.Label(TabServers, text="Password:",font=("Segoe UI", 10))
LblInputServerPassword.place(x=0,y=570)
TxtInputServerPassword = tk.Text(TabServers, width=25, height=1)
TxtInputServerPassword.place(x=0,y=590)
BtnRandomPassword = tk.Button(TabServers, text="Randomise Password",width=25, height=1)
BtnRandomPassword.place(x=240,y=588)

BtnInputServer = tk.Button(TabServers, text="Add Account", command=ProductWindow.withdraw,font=("Segoe UI", 10))
BtnInputServer.place(x=0,y = 620)

ProductNotebook.add(TabSupport, text="Support")

TabSettings = ttk.Frame(ProductNotebook)
ProductNotebook.add(TabSettings, text="Settings")
def NumInput(value):
    if value.isdigit() or value == "":
        return True
    else:
        return False


UseSymbols = tk.IntVar()
CBUseSymbols = tk.Checkbutton(TabSettings, text="Use Symbols In Password Randomisation", variable=UseSymbols, command=RememberPasswordToggle)
CBUseSymbols.place(x=5, y = 0)

UseNumbers = tk.IntVar()
CBUseNumbers = tk.Checkbutton(TabSettings, text="Use Numbers In Password Randomisation", variable=UseNumbers, command=RememberPasswordToggle)
CBUseNumbers.place(x=5, y = 20)

UseRussian = tk.IntVar()
CBUseRussian= tk.Checkbutton(TabSettings, text="Use Russian Characters In Password Randomisation", variable=UseRussian, command=RememberPasswordToggle)
CBUseRussian.place(x=5, y = 40)

UseChinese = tk.IntVar()
CBUseChinese= tk.Checkbutton(TabSettings, text="Use Chinese Characters In Password Randomisation", variable=UseChinese, command=RememberPasswordToggle)
CBUseChinese.place(x=5, y = 60)

UseHindi = tk.IntVar()
CBUseHindi= tk.Checkbutton(TabSettings, text="Use Hindi Characters In Password Randomisation", variable=UseHindi, command=RememberPasswordToggle)
CBUseHindi.place(x=5, y = 80)

UseAmharic = tk.IntVar()
CBUseAmharic = tk.Checkbutton(TabSettings, text="Use Amharic Characters In Password Randomisation", variable=UseAmharic, command=RememberPasswordToggle)
CBUseAmharic.place(x=5, y = 100)

notebook.place(x=0, y=0)
ProductNotebook.place(x=0,y=0)


#DrawMessageBox(MSGReason.Error,"header","Info")


