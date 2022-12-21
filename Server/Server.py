import DatabaseHandler
import Sockets
# Main is our initializer for general usage
def Main():
    db = DatabaseHandler.Database("Accounts.json")
    Sock = Sockets.Sockets()
    Sock.Start()
    db.CreateTable("Users",["Username","Password"])
    Username = Sock.RecieveMessage()
    Password = ""
    if(db.Search(db.Tables.get("Users"),{"Username":Username}) == None): # User Isn't Found
        db.Insert("Users",[Username,Password])
        Sock.SendMessage("User Successfully Created")
    elif(db.Search(db.Tables.get("Users"),{"Username":Username,"Password":Password}) != None): # User and password is found
        Sock.SendMessage("Successful Login")
    elif(db.Search(db.Tables.get("Users"),{"Username":Username,"Password":Password}) == None): # User has been found but password hasn't
        Sock.SendMessage("Incorrect Password")
        db.save()
        #Sock.Close()

Main() # Execute Main
