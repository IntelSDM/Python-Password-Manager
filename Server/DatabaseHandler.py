
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
            raise DBError("Database Not Found: " + self.Filename)
        else:
            self.Conn = sqlite3.connect(self.Filename)
            self.Cursor = self.Conn.cursor()

    def ResetPassword(self, username:str, twofactor:str,newpassword:str):
        print(username)
        print(twofactor)
        print(newpassword)
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
        self.Conn.commit()
        print(newtwofactor)
        return("Successful Password Reset. New Two Factor Code: " + newtwofactor) # Operation successful. Inform the user of their new two factor code.

    def CheckLogin(self, username:str,password:str):
        print(username)
        print(password)
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
    def AddUser(self, username:str,password:str,twofactor:str):
        """
        Adds a user to the User to the User table Through inserting the username, password, twofactor code
        """
        print(username)
        print(password)
        print(twofactor)
        if(Validation.LengthCheckStr(username,3,True)):
            return ("Username Too Short, It Must Exceed 3 Characters") # Username length check
        if(Validation.LengthCheckStr(password,8,True)):
            return ("Password Too Short, It Must Exceeed 8 Characters") # Password length check

        self.Cursor.execute("SELECT * FROM Users WHERE Username=?", (username,)) # Query for the database
        validusername = self.Cursor.fetchone() # Check if instance >= 1
        if(validusername):
            return("Username Is Already Taken") #Username taken, return, tell client
        self.Cursor.execute("INSERT INTO Users (Username, Password, TwoFactor) VALUES (?, ?, ?)", (username, sha256(password.encode("utf-8")).hexdigest(),sha256(twofactor.encode("utf-8")).hexdigest()))
        self.Conn.commit()
        return("Successful Registration, Please Write Down Your Two Factor Key: "+ str(twofactor))
    def Close(self):
        """
        Close connection to database and commit any uncommitted changed to the database.
        """
        self.Conn.commit()
        self.Conn.close() 

