import socket
import threading
import string
import random
import DatabaseHandler
import time



class Client():

    def __init__(self,clientsocket):
        """
        Defines the clientsocket in this client class and starts the command thread.
        """
       
        self.ClientSocket = clientsocket
        self.ClientThread = threading.Thread(target = self.HandleCommands) 
        self.ClientThread.start()
    def RecieveMessage(self):
        """
        Loops a byte array of data and waits to recieve any data that isn't blank or null. 
        When data is recieved it is decoded from the TLS encryption and then returned to the function
        """
        # Initialize an empty buffer to hold the message
        buffer = bytearray()
        while True:
            chunk = self.ClientSocket.recv(4096).decode() # Recieve on itteration for multiple messages and decode them
            if(chunk != None):
                return chunk # Loop Until Nothing Is Left. Dont Add Empty Chunk To Buffer. Return When Nothing Left

    def SendMessage(self, message:str):
        """
        Allows us to send messages by turning a string into a byte array
        Checks if the clientsocket is still open and then sends it in a TLS secure encrypted message
        """
        # Check if the client socket is still open
        if self.ClientSocket is not None:
            #Send Encrypted Message
            return self.ClientSocket.send(message.encode())

    def Close(self):
        # Close the client socket
        self.ClientSocket.close()
    def Login(self):
        """
        Logs the client in
        Recieves the username and password 
        Checks the login details in the database handler
        If its a successful login the client is logged in on the server
        Tells the client the database response
        """
        self.Username = self.RecieveMessage() # Get username
        self.Password = self.RecieveMessage() # Get password
        login = self.Database.CheckLogin(self.Username,self.Password) # Check is valid
        if(login == "Login Success"): # Valid user
            self.LoggedIn = True # set the user to logged in
        self.SendMessage(login) # send the client the message

    def Register(self):
        """
        Recieves the username and password
        Creates a two factor key
        Sends back a response to the client if their registration was successful or not
        """
        self.Username = self.RecieveMessage() # recieve the username
        self.Password = self.RecieveMessage() # recieve the password
        self.TwoFactor =  str("".join(random.choices(string.ascii_letters + string.digits, k=12))) # Creates a 12 character long random string with numbers and chars
        self.SendMessage(self.Database.AddUser(self.Username,self.Password,self.TwoFactor)) # send the response from adding the user
    def ResetPassword(self):
        """
        Recieves the username, new password and the two factor
        Sends the details to the database
        Sends the response from the database back to the client
        """
        self.Username = self.RecieveMessage() # recieve username
        self.Password = self.RecieveMessage() # recieve password
        self.TwoFactor = self.RecieveMessage() # recieve two factor
        self.SendMessage(self.Database.ResetPassword(self.Username,self.TwoFactor,self.Password))

    def DeleteServer(self):
        """
        Check if the user is logged in or not
        If so we will tell the database to delete the server by the serverid we recieve
        """
        if(self.LoggedIn == False):
            return
        self.Database.DeleteServer(self.RecieveMessage()) # Send the serverid that we recieve to the database
    def CreateServer(self):
        """
        Recieves all of the details for the server logins
        Then saves them to the database
        """
        if(self.LoggedIn == False):
            return # User isn't logged in
        sid = self.RecieveMessage() # recieve the serverid
        name = self.RecieveMessage() # recieve server name
        user = self.RecieveMessage() # recieve the server username
        password = self.RecieveMessage() # recieve the server password
        self.Database.AddServer(sid,self.Username,name,user,password) # send the details to the database
    def SendServers(self):
        """
        Sends the list of servers that are owned by the user
        Firstly checks for the login
        If so we will get the servers from the database
        Send the client the length of the server array
        We then send all the data from the servers to the client
        """
        if(self.LoggedIn == False):
            return
        servers = []
        servers = self.Database.GetServers(self.Username)
        self.SendMessage(str(len(servers))) # Send the amount of data to the client
        i = 0
        for server in servers:
            i = i+1
            if(i%4 == 0):
                time.sleep(1) # Allow both programs  to sync
            self.SendMessage(server)
    def HandleCommands(self):
        """
        Allows us to handle commands and then call functions in an event based system.
        Since the function relies on a syscall to recv the cpu clock will allocate everything onto the same physical thread with different addresses cached.
        Therefore it wont be as cpu consuming as expected even when running 100s of virtual threads.
        The database has to be created in this thread as it will be accessed from the thread. Thread safety. 
        """
        self.Database = DatabaseHandler.Database("Database.db") # Initial DB Instance
        while(True):
            if(self.ClientSocket == None):
                break # Check if the client is still alive
            Message = self.RecieveMessage()
            if(Message == "Login"):
                self.Login() # Client is logging in
            if(Message == "Register"):
                self.Register()# Client is registering
            if(Message == "Resetting Password"):
                self.ResetPassword() # Client is resetting password
            if(Message == "Delete Server"):
                self.DeleteServer() # client is deleting server
            if(Message == "Create Server"):
                self.CreateServer() # client is creating new server
            if(Message == "Send Servers"):
                self.SendServers() # client is asking for their server list
        self.Database.Close() # close handle to database
        self.ClientSocket.close() # close sockets
