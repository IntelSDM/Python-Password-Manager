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
from GUIConstants import UseSymbols
from GUIConstants import UseRussian
from GUIConstants import UseNumbers
from GUIConstants import End
from GUIConstants import UseChinese
from GUIConstants import UseHindi
from GUIConstants import UseAmharic
from GUIConstants import BtnRandomPassword
from string import ascii_lowercase, ascii_uppercase, digits
import time
import Server
import string
import random
import threading
# Main is our initializer for general usage

Sock = Sockets.Sockets()

ServerList = []
Russian = "БГДЁЖИЙЛПФфЦЧШЩЪЫЬЭЮЯ"
Symbols = "!=<>'@#$%^&*()[\],.;:-_/+?{|}`~"
Numbers = digits
Letters = ascii_uppercase + ascii_uppercase
Chinese = "诶比西迪伊尺杰大水开勒哦屁吉吾儿诶比西迪伊弗吉尺艾弗吉杰屁吉吾儿八九十开勒马娜哦月人马娜口"
Hindi = "ऄअआइईउऊऋऌऍऎएऐऑऒओऔकखगघङचछजझञटठडढणतथदधनऩपफबभमयरऱलळऴवशषसहऽॐॠॡ।॥०१२३४५६७८९॰ॲॳॴॵॶॷॹॺॻॼॽॾॿೱೲऀँंःऺऻ़ािीुूृॄॅॆेैॉॊोौ्ॎॏ॒॑॓॔ॕॖॗॢॣ"
Amharic = "ሀሁሂሃሄህሆሎልሌላሊሉለሐሑሒሓሔሕሖሞምሜማሚሙመሠሡሢሣሤሥሦሮርሬራሪሩረሰሱሲሳሴስሶሾሽሼሻሺሹሸቀቁቂቃቄቅቆቦብቤባቢቡበቨቩቪቫቬቭቮቶትቴታቲቱተቸቹቺቻቼችቾኆኅኄኃኂኁኀነኑኒናኔንኖኞኝኜኛኚኙኘአኡኢኣኤእኦኮክኬካኪኩከኸኹኺኻኼኽኾዎውዌዋዊዉወዐዑዒዓዔዕዖዞዝዜዛዚዙዘዠዡዢዣዤዥዦዮይዬያዪዩየደዱዲዳዴድዶጆጅጄጃጂጁጀገጉጊጋጌግጎጦጥጤጣጢጡጠጨጩጪጫጬጭጮጶጵጴጳጲጱጰጸጹጺጻጼጽጾፆፅፄፃፂፁፀፈፉፊፋፌፍፎፖፕፔፓፒፑፐ፩፪፫፬፭፮፯፰፱፲፳፴፵፶፷፸፹፺፻፼፡።፣፤፥"
def GetRandChars():
    """
    I use this to select through the user's input through the customizable password generator
    Letters are used by default but the other options have to be selelcted by the user in order to be used.
    After it has found and added all selected elements to the final string it returns it
    We try and catch any errors that may occur from a lack of user input or from tkinter
    """
    try:
        result = Letters
        if(UseSymbols.get()):
            result+= Symbols
        if(UseNumbers.get()):
            result+= Numbers
        if(UseChinese.get()):
            result+= Chinese
        if(UseHindi.get()):
            result+= Hindi
        if(UseAmharic.get()):
            result+= Amharic
        if(UseRussian.get()):
            result+= Russian
        return result
    except:
        DrawMessageBox(MSGReason.Error,"Password Generation","Error Generating Password Characters") 
        return Letters
def Randomise():
    """
    Use random in order to generate an int between 9 and 35 that can be used as the max character size.
    We then use the max character size in order to select random chars from the string of characters
    We then compile the final string in the string builder containing all the random chars.
    We also try and catch any possible exceptions from math issues in the random library
    """
    try:
        num = random.randint(9, 35)
        rand = ''.join(random.choice(GetRandChars()) for i in range(num))
        return str(rand)
    except:
        DrawMessageBox(MSGReason.Error,"Password Generation","Error Generating Password. Make sure you configure the password randomiser")
        return ""
def RandomPassword():
    """
    We clear the password textbox in order to fully write to it without overwriting existing data
    We then open a function to write to the password textbox and then get the randomly generated password and insert it into the textbox

    """
    TxtInputServerPassword.delete("1.0", End)
    TxtInputServerPassword.insert("1.0",Randomise())
def Main():
    """
    Ensure that the server/product window is closed
    Set the event action of the server list box to use the refresh function
    Start setting all button functionality
    Set the values of the serverlist
    Start the main loops
    """
    ProductWindow.withdraw() # hide the product window
    ServerListBox.bind("<<ListboxSelect>>",RefreshSelected) # set the server reefresh function
    i = 0
    for server in ServerList: # loop the list to get instances and add them to the serverlist box, debug purposes
        ServerListBox.insert(i,server.ServerName)
        i+=1
    if(len(ServerList)>0):# Setup the serverlist
        CurrentSelectedServer = ServerList[0]
        ServerListBox.selection_set(0)

    Sock.Start() # start connectoiing to the server
    BtnLogin.config(command = Login) # Set login button functional
    BtnRegister.config(command = Register) # Set Register button functional
    BtnResetPassword.config(command = ResetPassword) # Set Reset Password button functional
    BtnInputServer.config(command = AddAccount)
    BtnSelectedRemove.config(command = RemoveAccount)
    BtnCopyServerPassword.config(command = CopyPassword)
    BtnCopyServerName.config(command = CopyUsername)
    BtnRandomPassword.config(command = RandomPassword)
    LoginWindow.mainloop() # Draw the window
    ProductWindow.mainloop() # Draw the product window
# on lets say changing the password on the button of changing the password lets send the server a message to update the password
def RefreshSelected(event):
        if(len(ServerList)>0): # check if the server list is valid
            CurrentSelectedServer = ServerList[ServerListBox.curselection()[0]] # set the serverlist valid to the selected instance
            LblSelectedServerPassword.config(text="Server Password: " + CurrentSelectedServer.Password) # refresh the values
            LblSelectedServerName.config(text="Username: " + CurrentSelectedServer.Username)
def AddAccount():
    """
    Create a blank server instance
    Make a random key
    Set the username,password,servername
    Add the server  to the serverlist
    Tell the server that we will be adding a server
    Sync with server with a sleep
    Send the server instance details
    """
    addserver = None
    addserver = Server.Server(str("".join(random.choices(string.ascii_letters + string.digits, k=12)))) # create a random primary key
    addserver.SetServerName(TxtInputServerName.get("1.0", "end-1c")) # set the server name
    addserver.SetUsername(TxtInputServerUsername.get("1.0", "end-1c")) # set the username
    addserver.SetPassword(TxtInputServerPassword.get("1.0", "end-1c")) # set the password
    ServerList.append(addserver)
    ServerListBox.insert(len(ServerList) +1,addserver.ServerName) # add to the next instance of the list
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
    """
    Check if the serverlistbox has a valid server
    Tell the server we will delete a server
    sync with sleep
    tell the server which serverid we will delete
    Delete from local list and serverlistbox
    """
    if(ServerListBox.curselection()[0] == None): # Check if the instane is valid
        return
    Sock.SendMessage("Delete Server") # tell the server we are deleting
    time.sleep(1)
    Sock.SendMessage(ServerList[ServerListBox.curselection()[0]].ServerID) # send the server id we will delete
    del ServerList[ServerListBox.curselection()[0]] # remove from local list
    ServerListBox.delete(ServerListBox.curselection()[0]) # remove from listbox

def RecieveServers():
    """
    Tell the server to send the servers
    Wait for it to tell us the amount of server data
    Divide the server data by 4 as there are 4 fields
    Loop through the amount of servers and recieve all the data
    add the temporary server instance to the list
    Null the temporary server  object
    Sort the server list using bubble sort
    """
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
    """
    Tells the server we are resetting the password
    Sync with the server using sleep
    Send off the text box data to the server
    Wait for the server to respond
    Print the response.
    """
    Sock.SendMessage("Resetting Password") # Tell the server we are resetting a password
    time.sleep(1)
    Sock.SendMessage(TxtResetPasswordUsername.get("1.0", "end-1c")) # Send the reading of the textbox from start to end
    time.sleep(1)
    Sock.SendMessage(TxtResetPasswordPassword.get("1.0", "end-1c")) # Send the reading of the textbox from start to end
    time.sleep(1)
    Sock.SendMessage(TxtResetPasswordTwoFactor.get("1.0", "end-1c"))# Send the reading of the textbox from start to end
    Response = Sock.RecieveMessage() # The server response
    DrawMessageBox(MSGReason.Info,"Login Response",Response) # Display the respsonse from the server to the client
def BubbleSort(arr):
    """
    Bubble sorting the array/list
    Take the middle point and check if the alphabetical value
    If the alphabetical value exceeds then checks the next middle point and restructures the array
    This is done till every element is swapped
    """
    n = len(arr)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j].ServerName > arr[j + 1].ServerName:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
         
        if not swapped:
            return


def Login():
    """
    Tell the server that we are logging in
    sleep the let the server sync.
    Send over the user data from the username and password textbox
    Check if the server finds it to be a correct login
    Inform the user on their login
    If the login is successful then search for the servers
    Open the product window
    Hide the login window.
    """
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
    """
    Access the cliboard object which is a pointer from the tkinter library
    We then set then set the clipboard to the username by getting it through the serverlist object.
    We catch ant errors and print our to the user so they can report it
    """
    try:
        LoginWindow.clipboard_append(ServerList[ServerListBox.curselection()[0]].Username)
    except:
        DrawMessageBox(MSGReason.Error,"Username Copy","Error Copying Username")
    
def CopyPassword():
    """
    Access the cliboard object which is a pointer from the tkinter library
    We then set then set the clipboard to the password by getting it through the serverlist object.
    We catch ant errors and print our to the user so they can report it
    """
    try:
        LoginWindow.clipboard_append(ServerList[ServerListBox.curselection()[0]].Password)
    except:
        DrawMessageBox(MSGReason.Error,"Password Copy","Error Copying Password")
def Register():
    """
    Get the text of the password and confirm password textboxes. Compare both of the strings
    If the values aren't the same return the function and show an error box
    Then it tells the server we are registering and then send details to the server to be logged
    After we are done we tell the client the response that the server has. 
    """
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
