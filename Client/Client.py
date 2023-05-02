import Sockets
from GUIConstants import LoginWindow
from GUIConstants import TxtLoginPassword
from GUIConstants import TxtLoginUsername
from GUIConstants import TxtRegisterPassword
from GUIConstants import TxtRegisterConfirmPassword
from GUIConstants import TxtRegisterUsername
from GUIConstants import TxtResetPasswordPassword
from GUIConstants import TxtResetPasswordTwoFactor
from GUIConstants import TxtResetPasswordUsername
from GUIConstants import BtnLogin
from GUIConstants import BtnRegister
from GUIConstants import BtnResetPassword
from GUIConstants import MSGReason
from GUIConstants import DrawMessageBox
from GUIConstants import ServerListBox
from GUIConstants import LblSelectedServerName
from GUIConstants import LblSelectedServerPassword
from GUIConstants import TxtInputServerName
from GUIConstants import TxtInputServerUsername
from GUIConstants import TxtInputServerPassword
from GUIConstants import BtnInputServer
from GUIConstants import BtnSelectedRemove
from GUIConstants import ProductWindow
from GUIConstants import BtnCopyServerPassword
from GUIConstants import BtnCopyServerName
import time
import Server
import string
import random
import threading
# Main is our initializer for general usage

Sock = Sockets.Sockets()

ServerList = []

def Main():
    ProductWindow.withdraw()
    ServerListBox.bind("<<ListboxSelect>>",RefreshSelected)
    i = 0
    for server in ServerList:
        ServerListBox.insert(i,server.ServerName)
        i+=1
    if(len(ServerList)>0):
        CurrentSelectedServer = ServerList[0]
        ServerListBox.selection_set(0)

    Sock.Start()
    BtnLogin.config(command = Login) # Set login button functional
    BtnRegister.config(command = Register) # Set Register button functional
    BtnResetPassword.config(command = ResetPassword) # Set Reset Password button functional
    BtnInputServer.config(command = AddAccount)
    BtnSelectedRemove.config(command = RemoveAccount)
    BtnCopyServerPassword.config(command = CopyPassword)
    BtnCopyServerName.config(command = CopyUsername)

    LoginWindow.mainloop() # Draw the window
    ProductWindow.mainloop() # Draw the product window
# on lets say changing the password on the button of changing the password lets send the server a message to update the password
def RefreshSelected(event):
        if(len(ServerList)>0):
            CurrentSelectedServer = ServerList[ServerListBox.curselection()[0]]
            LblSelectedServerPassword.config(text="Server Password: " + CurrentSelectedServer.Password)
            LblSelectedServerName.config(text="Username: " + CurrentSelectedServer.Username)
def AddAccount():
    addserver = None
    addserver = Server.Server(str("".join(random.choices(string.ascii_letters + string.digits, k=12))))
    addserver.SetServerName(TxtInputServerName.get("1.0", "end-1c"))
    addserver.SetUsername(TxtInputServerUsername.get("1.0", "end-1c"))
    addserver.SetPassword(TxtInputServerPassword.get("1.0", "end-1c"))
    ServerList.append(addserver)
    ServerListBox.insert(len(ServerList) +1,addserver.ServerName)
    Sock.SendMessage("Create Server")
    time.sleep(1)
    Sock.SendMessage(addserver.ServerID)
    time.sleep(1)
    Sock.SendMessage(addserver.ServerName)
    time.sleep(1)
    Sock.SendMessage(addserver.Username)
    time.sleep(1)
    Sock.SendMessage(addserver.Password)
def RemoveAccount():
    if(ServerListBox.curselection()[0] == None):
        return
    Sock.SendMessage("Delete Server")
    time.sleep(1)
    Sock.SendMessage(ServerList[ServerListBox.curselection()[0]].ServerID)
    del ServerList[ServerListBox.curselection()[0]]
    ServerListBox.delete(ServerListBox.curselection()[0])

def RecieveServers():
    Sock.SendMessage("Send Servers")
    count = Sock.RecieveMessage();
    # Divide by 4 as there are 4 instances in each server
    for i in range(0,int(int(count)/4)): # recieve server details, store in instance
        tempserver = Server.Server(Sock.RecieveMessage())
        tempserver.SetServerName(Sock.RecieveMessage())
        tempserver.SetUsername(Sock.RecieveMessage())
        tempserver.SetPassword(Sock.RecieveMessage())
        ServerList.append(tempserver) # add instance to the list
        tempserver = None
    BubbleSort(ServerList)
    j = 0
    for server in ServerList:
        ServerListBox.insert(j,server.ServerName)
        j+=1
def ResetPassword():
    Sock.SendMessage("Resetting Password") # Tell the server we are resetting a password
    time.sleep(1)
    Sock.SendMessage(TxtResetPasswordUsername.get("1.0", "end-1c")) # Send the reading of the textbox from start to end
    time.sleep(1)
    Sock.SendMessage(TxtResetPasswordPassword.get("1.0", "end-1c")) # Send the reading of the textbox from start to end
    time.sleep(1)
    Sock.SendMessage(TxtResetPasswordTwoFactor.get("1.0", "end-1c"))# Send the reading of the textbox from start to end
    Response = Sock.RecieveMessage()
    DrawMessageBox(MSGReason.Info,"Login Response",Response) # Display the respsonse from the server to the client
def BubbleSort(arr):
    n = len(arr)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j].ServerName > arr[j + 1].ServerName:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
         
        if not swapped:
            return

def BubbleSortListbox(lb):
    # Get the number of items in the listbox
    n = lb.size()
    
    # Perform bubble sort on the listbox items
    for i in range(n-1):
        for j in range(0, n-i-1):
            # Compare adjacent items and swap them if they are out of order
            if lb.get(j) > lb.get(j+1):
                lb.delete(j)
                lb.insert(j+1, lb.get(j))
                lb.delete(j+1)
                lb.insert(j, lb.get(j+1))

def Login():
    Sock.SendMessage("Login") # Tell the server we are logging in
    time.sleep(1)
    Sock.SendMessage(TxtLoginUsername.get("1.0", "end-1c")) # Send the reading of the textbox from start to end
    time.sleep(1)
    Sock.SendMessage(TxtLoginPassword.get("1.0", "end-1c")) # Send the reading of the textbox from start to end
    Response = Sock.RecieveMessage()
    DrawMessageBox(MSGReason.Info,"Login Response",Response) # Display the respsonse from the server to the client
    if(Response != "Login Success"):
        return
    RecieveServers()
    ProductWindow.deiconify()
    LoginWindow.withdraw()
    
def CopyUsername():
    LoginWindow.clipboard_append(ServerList[ServerListBox.curselection()[0]].Username)
    
def CopyPassword():
    LoginWindow.clipboard_append(ServerList[ServerListBox.curselection()[0]].Password)
def Register():
    if(TxtRegisterPassword.get("1.0", "end") !=  TxtRegisterConfirmPassword.get("1.0", "end")):
        DrawMessageBox(MSGReason.Error,"Password Mistmatch", "Password Mistmatch")
        return

    Sock.SendMessage("Register") # Tell the server we are registering
    time.sleep(1)
    Sock.SendMessage(TxtRegisterUsername.get("1.0", "end-1c")) # Send the reading of the textbox from start to end
    time.sleep(1)
    Sock.SendMessage(TxtRegisterPassword.get("1.0", "end-1c")) # Send the reading of the textbox from start to end
    Response = Sock.RecieveMessage()
    DrawMessageBox(MSGReason.Info,"Register Response",Response) # Display the response from the server to the client
Main() # Execute Main
