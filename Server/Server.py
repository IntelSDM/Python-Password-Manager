import DatabaseHandler
import Sockets
import random
from hashlib import sha256
import random
import string

Sock = Sockets.Sockets()

def Login(db: DatabaseHandler.Database):
    Username = Sock.RecieveMessage() # Get username
    Password = Sock.RecieveMessage() # Get password
    if(db.Search(db.Tables.get("Users"),{"Username":Username,"Password":sha256(Password.encode("utf-8")).hexdigest()}) != None): # User and password is found
        Sock.SendMessage("Successful Login")
    elif(db.Search(db.Tables.get("Users"),{"Username":Username,"Password":sha256(Password.encode("utf-8")).hexdigest()}) == None): # User has been found but password hasn't
        Sock.SendMessage("Incorrect Password")
    db.Save()
    Sock.Close()

def Register(db: DatabaseHandler.Database):
    Username = Sock.RecieveMessage()
    Password = Sock.RecieveMessage()
    TwoFactor =  "".join(random.choices(string.ascii_letters + string.digits, k=12)) # Creates a 12 character long random string with numbers and chars
    if(db.Search(db.Tables.get("Users"),{"Username":Username}) == None): # User Isn't Found
        db.Insert("Users",[Username,sha256(Password.encode("utf-8")).hexdigest(),TwoFactor]) # Add username, hashed password, twofactor code
        Sock.SendMessage("User Successfully Created")
    else:
        Sock.SendMessage("User Already Exists")
    Sock.Close()
    db.Save()


# Main is our initializer for general usage
def Main():
    
    db = DatabaseHandler.Database("Accounts.json")
    Sock.Start()
    db.CreateTable("Users",["Username","Password","2Factor"]) # If the table isn't created, create the table
    Message = Sock.RecieveMessage() # Lets check what message might be sent
    if(Message == "Login"):
        Login(db) # Client is logging in
    if(Message == "Register"):
        Register(db)# Client is registering

Main() # Execute Main
