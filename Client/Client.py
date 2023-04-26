import Sockets
from GUIConstants import LoginWindow
from GUIConstants import TxtLoginPassword
from GUIConstants import TxtLoginUsername
from GUIConstants import TxtRegisterPassword
from GUIConstants import TxtRegisterUsername
from GUIConstants import BtnLogin
from GUIConstants import BtnRegister
from GUIConstants import MSGReason
from GUIConstants import DrawMessageBox
import time
# Main is our initializer for general usage

Sock = Sockets.Sockets()
def Main():
    Sock.Start()
    BtnLogin.config(command = Login) # Set login button functional
    BtnRegister.config(command = Register) # Set Register button functional
    LoginWindow.mainloop() # Draw the window

def Login():
    Sock.SendMessage("Login") # Tell the server we are logging in
    time.sleep(1)
    Sock.SendMessage(TxtLoginUsername.get("1.0", "end")) # Send the reading of the textbox from start to end
    time.sleep(1)
    Sock.SendMessage(TxtLoginPassword.get("1.0", "end")) # Send the reading of the textbox from start to end
    Response = Sock.RecieveMessage()
    DrawMessageBox(MSGReason.Info,"Login Response",Response) # Display the respsonse from the server to the client

def Register():
    Sock.SendMessage("Register") # Tell the server we are registering
    time.sleep(1)
    Sock.SendMessage(TxtRegisterUsername.get("1.0", "end")) # Send the reading of the textbox from start to end
    time.sleep(1)
    Sock.SendMessage(TxtRegisterPassword.get("1.0", "end")) # Send the reading of the textbox from start to end
    Response = Sock.RecieveMessage()
    DrawMessageBox(MSGReason.Info,"Register Response",Response) # Display the response from the server to the client
Main() # Execute Main
