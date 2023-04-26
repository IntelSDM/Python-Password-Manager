import DatabaseHandler
import Sockets
import random

import random
import string

Sock = Sockets.Sockets()

def Login(db: DatabaseHandler.Database):
    Username = Sock.RecieveMessage() # Get username
    Password = Sock.RecieveMessage() # Get password
    Sock.SendMessage(db.CheckLogin(Username,Password))
  #  print(db.Search(db.Tables.get("Users"),{"Username":Username}))
  #  if(db.Search(db.Tables.get("Users"),{"Username":Username,"Password":sha256(Password.encode("utf-8")).hexdigest()}) != None): # User and password is found
 #       Sock.SendMessage("Successful Login")
 #   elif(db.Search(db.Tables.get("Users"),{"Username":Username,"Password":sha256(Password.encode("utf-8")).hexdigest()}) == None): # User has been found but password hasn't
   #     Sock.SendMessage("Incorrect Password")
   # db.Save()
    db.Close()
    Sock.Close()
def Register(db: DatabaseHandler.Database):
    Username = Sock.RecieveMessage()
    Password = Sock.RecieveMessage()
    TwoFactor =  str("".join(random.choices(string.ascii_letters + string.digits, k=12))) # Creates a 12 character long random string with numbers and chars
    Sock.SendMessage(db.AddUser(Username,Password,TwoFactor))
    db.Close()
    Sock.Close()


# Main is our initializer for general usage
def Main():
    
    db = DatabaseHandler.Database("Database.db") # New Db Instance
    Sock.Start()
   # db.CreateTable("Users",["Username","Password","2Factor"]) # If the table isn't created, create the table
    Message = Sock.RecieveMessage() # Lets check what message might be sent
    if(Message == "Login"):
        Login(db) # Client is logging in
    if(Message == "Register"):
        Register(db)# Client is registering

Main() # Execute Main
