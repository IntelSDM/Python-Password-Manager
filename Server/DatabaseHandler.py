
from enum import Enum
import re
import sqlite3
from hashlib import sha256
import os
import random
import string



class Format(Enum):
    Date = 0,
    Time = 1,
    
class Validation:
    '''
    This is a static class and can be referenced like a namespace requiring no instance
    '''
    @staticmethod
    def RangeCheck(minvalue, maxvalue, value):
        if(value >= minvalue and value <= maxvalue):
            return True
        return False
    @staticmethod
    def PresenceCheck(value):
        if(id(value) != None and value != None): #id converts value to a pointer and checks if the address isn't null, also checks if value isn't null
            return True
        return False
    @staticmethod
    def LengthCheckStr(value, maxvalue, allowunder):
        '''Prototype function of lengthcheck to allow for it to process strings'''
        allowunder = bool(allowunder)  # cant trust python, lets make sure we get a bool
        if(allowunder):
            if(len(value) <= maxvalue):
                return True
        else:
            if(len(value) == maxvalue):
                return True
        return False
    @staticmethod
    def TypeCheck(data, datatype):
        if(isinstance(data,datatype)): # isinstance returns a bool if the data type matches the data
            return True
        return False
    @staticmethod
    def LengthCheck(value, maxvalue, allowunder):
        if(Validation.TypeCheck(value,str)):
            return Validation.LengthCheckStr(value,maxvalue,allowunder)
        allowunder = bool(allowunder)  # cant trust python, lets make sure we get a bool
        if(allowunder):
            if(value <= maxvalue):
                return True
        else:
            if(value == maxvalue):
                return True
        return False
    
    @staticmethod
    def FormatCheck(data,form):
        if(not Validation.TypeCheck(form,Enum)):
            # we are raising an exception to prevent further execution, This works the same as any error and prevents the application executing unless it is caught. this prevents bad code running and informs the programmer on their misuse
            raise ValueError('Format Enum Not Entrered In FormatCheck')
            return False
        # our string formatchecks
        if(Validation.TypeCheck(data,str)):
            if(form == Format.Date): # Date Check
                pattern = r"^\d{2}/\d{2}/\d{4}$"
                if(re.match(pattern,data)):
                    return True
            if(form == Format.Time): #Time Check
                pattern = r"^\d{2}:\d{2}$"
                if(re.match(pattern,data)):
                    return True
        return False
class Database:
    """
This class is meant to create the database and write and read from/to the database

    """
    def __init__(self, filename: str):
        """
        Initialize the database.
        """
        self.Filename = filename
        self.CreateDatabase()

    def CreateDatabase(self):
        """
        Check if our database is avaliable. Load it or prompt an error if it is unavaliable
        """
        if(not os.path.exists(self.Filename)):
            raise DBError("Database Not Found: " + self.Filename)# database not found
        else:
            self.Conn = sqlite3.connect(self.Filename) # connect to the database
            self.Cursor = self.Conn.cursor()# create cursor

    def ResetPassword(self, username:str, twofactor:str,newpassword:str):
        """
        Check if the new password meets requirements
        Check if the username exists
        Check if the two factor code goes with the username
        If username and two factor are both correct change the password
        Generate a new two factor code and send it back to the client
        """
        if(Validation.LengthCheckStr(newpassword,8,True)):
            return ("Password Too Short, It Must Exceeed 8 Characters") # Password length check
        self.Cursor.execute("SELECT * FROM Users WHERE Username=?", (username,)) # Query for the database
        validusername = not self.Cursor.fetchone() # Check if instance >= 1
        if(validusername):
            return("Username Is Invalid") #Username doesn't exist
        self.Cursor.execute("SELECT * FROM Users WHERE Username=? And TwoFactor=?", (username,sha256(twofactor.encode("utf-8")).hexdigest())) # Query for the database
        validtwofactor = not self.Cursor.fetchone() # Check if instance >= 1
        if(validtwofactor):
            return("Two Factor Code Is Invalid") #Two factor mistmatch
        newtwofactor = str("".join(random.choices(string.ascii_letters + string.digits, k=12))) # Creates a 12 character long random string with numbers and chars
        self.Cursor.execute("UPDATE Users Set Password = ? WHERE Username = ? And TwoFactor = ?",(sha256(newpassword.encode("utf-8")).hexdigest(),username,sha256(twofactor.encode("utf-8")).hexdigest())) # Update the password for the user, double check their twofactor
        self.Cursor.execute("UPDATE Users Set TwoFactor = ? WHERE Username = ? And Password = ?",(sha256(newtwofactor.encode("utf-8")).hexdigest(),username,sha256(newpassword.encode("utf-8")).hexdigest())) # Update the twofactor code
        self.Conn.commit()# save
        return("Successful Password Reset. New Two Factor Code: " + newtwofactor) # Operation successful. Inform the user of their new two factor code.

    def CheckLogin(self, username:str,password:str):
        """
        Check the user credentials are null
        If credentials are null return the error
        If they aren't null locate the username
        If username isn't found return error
        If the username and password are both found then return success
        """
        if(not Validation.PresenceCheck(password)):
            return ("Please Enter A Password") # Check if the password is null
        if(not Validation.PresenceCheck(username)):
            return ("Please Enter A Username") # Check if the username is null
        self.Cursor.execute("SELECT * FROM Users WHERE Username=?", (username,)) # Query for the database
        validusername = not self.Cursor.fetchone() # Check if instance >= 1
        if(validusername):
            return("Username Is Invalid") #Username doesn't exist
        self.Cursor.execute("SELECT * FROM Users WHERE Username=? And Password=?", (username,sha256(password.encode("utf-8")).hexdigest())) # Query if the user exists
        validuserpass = self.Cursor.fetchone() # Check if instance >= 1
        if(validuserpass):
            return("Login Success")
        else:
            return("Invalid Password")
    def AddServer(self, serverid:str,username:str,servername:str,serverusername:str,serverpassword:str):
        """
        Mysql insert into the servers table with the server information
        """
        self.Cursor.execute("INSERT INTO Servers (ServerID, UserID ,ServerName, ServerUsername,ServerPassword) VALUES (?, ?, ?,?,?)", (serverid,username,servername,serverusername,serverpassword)) # add the server information 
        self.Conn.commit()# save
    def GetServers(self,username:str):
        """
        Get all servers that the user owns
        Fetch the data
        Loop through the data in a linear search to find what data isn't the username
        Save all none username data to a list
        Return the list
        """
        servers = []
        self.Cursor.execute("SELECT * FROM servers WHERE UserID = ?",(username,)) # get list of servers by username
        rows = self.Cursor.fetchall() # fetch them
        for row in rows: # linear search through dict
            for word in row: # linear search through the array from the dict
                if word != username: # check if its username
                    servers.append(word) # add the data

        return servers
    def DeleteServer(self,serverid:str):
        """
        Deletes server by serverid
        Tells database to delete server and then save
        """
        self.Cursor.execute("DELETE FROM Servers WHERE ServerID = ?", (serverid,)) # delete the server
        self.Conn.commit() # save changes
    def AddUser(self, username:str,password:str,twofactor:str):
        """
        Adds a user to the User to the User table Through inserting the username, password, twofactor code
        """
        if(Validation.LengthCheckStr(username,3,True)):
            return ("Username Too Short, It Must Exceed 3 Characters") # Username length check
        if(Validation.LengthCheckStr(password,8,True)):
            return ("Password Too Short, It Must Exceeed 8 Characters") # Password length check

        self.Cursor.execute("SELECT * FROM Users WHERE Username=?", (username,)) # Query for the database
        validusername = self.Cursor.fetchone() # Check if instance >= 1
        if(validusername):
            return("Username Is Already Taken") #Username taken, return, tell client
        self.Cursor.execute("INSERT INTO Users (Username, Password, TwoFactor) VALUES (?, ?, ?)", (username, sha256(password.encode("utf-8")).hexdigest(),sha256(twofactor.encode("utf-8")).hexdigest()))
        self.Conn.commit() # save
        return("Successful Registration, Please Write Down Your Two Factor Key: "+ str(twofactor)) # information for the client
    def Close(self):
        """
        Close connection to database and commit any uncommitted changed to the database.
        """
        self.Conn.commit()
        self.Conn.close() 

