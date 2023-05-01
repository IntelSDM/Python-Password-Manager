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

import time
import Server
import string
import random
import threading
# Main is our initializer for general usage

Sock = Sockets.Sockets

ServerList = []

def Main():
    test1 = Server.Server("sfsafaw")
    ServerList.append(test1)
    test2 = Server.Server("sfsafaw1")
    ServerList.append(test2)
    test1.SetServerName("test1")
    test2.SetServerName("test2")
    test1.SetPassword("test1")
    test2.SetPassword("test2")
    test1.SetUsername("test1")
    test2.SetUsername("test2")
    ServerListBox.bind("<<ListboxSelect>>",RefreshSelected)
    i = 0
    for server in ServerList:
        ServerListBox.insert(i,server.ServerName)
        i+=1
    if(len(ServerList)>0):
        CurrentSelectedServer = ServerList[0]
        ServerListBox.selection_set(0)

    # Sock.Start()
    BtnLogin.config(command = Login) # Set login button functional
    BtnRegister.config(command = Register) # Set Register button functional
    BtnResetPassword.config(command = ResetPassword) # Set Reset Password button functional
    BtnInputServer.config(command = AddAccount)
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


def RecieveServers():
    Sock.SendMessage("Send Servers")
    count = Sock.RecieveMessage();
    for i in range(0,count):
        tempserver = Server.Server(Sock.RecieveMessage())
        tempserver.SetServerName(Sock.RecieveMessage())
        tempserver.SetUsername(Sock.RecieveMessage())
        tempserver.SetPassword(Sock.RecieveMessage())
        ServerList.append(tempserver)
        tempserver = None

        
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

def Login():
    Sock.SendMessage("Login") # Tell the server we are logging in
    time.sleep(1)
    Sock.SendMessage(TxtLoginUsername.get("1.0", "end-1c")) # Send the reading of the textbox from start to end
    time.sleep(1)
    Sock.SendMessage(TxtLoginPassword.get("1.0", "end-1c")) # Send the reading of the textbox from start to end
    Response = Sock.RecieveMessage()
    DrawMessageBox(MSGReason.Info,"Login Response",Response) # Display the respsonse from the server to the client

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
