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
        # Initialize an empty buffer to hold the message
        buffer = bytearray()
        while True:
            chunk = self.ClientSocket.recv(4096).decode() # Recieve on itteration for multiple messages and decode them
            if(chunk != None):
                return chunk # Loop Until Nothing Is Left. Dont Add Empty Chunk To Buffer. Return When Nothing Left

    def SendMessage(self, message:str):
        # Check if the client socket is still open
        if self.ClientSocket is not None:
            #Send Encrypted Message
            return self.ClientSocket.send(message.encode())

    def Close(self):
        # Close the client socket
        self.ClientSocket.close()
    def Login(self):
        self.Username = self.RecieveMessage() # Get username
        self.Password = self.RecieveMessage() # Get password
        self.SendMessage(self.Database.CheckLogin(self.Username,self.Password))

    def Register(self):
        self.Username = self.RecieveMessage()
        self.Password = self.RecieveMessage()
        self.TwoFactor =  str("".join(random.choices(string.ascii_letters + string.digits, k=12))) # Creates a 12 character long random string with numbers and chars
        self.SendMessage(self.Database.AddUser(self.Username,self.Password,self.TwoFactor))
    def ResetPassword(self):
        self.Username = self.RecieveMessage()
        self.Password = self.RecieveMessage()
        self.TwoFactor = self.RecieveMessage()
        self.SendMessage(self.Database.ResetPassword(self.Username,self.TwoFactor,self.Password))
  #  def SendServers(self):
        #loop all servers in db, send them all
    def DeleteServer(self):
        self.Database.DeleteServer(self.RecieveMessage())
    def CreateServer(self):
        sid = self.RecieveMessage()
        name = self.RecieveMessage()
        user = self.RecieveMessage()
        password = self.RecieveMessage()
        self.Database.AddServer(sid,self.Username,name,user,password)
    def SendServers(self):
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
                self.DeleteServer()
            if(Message == "Create Server"):
                self.CreateServer()
            if(Message == "Send Servers"):
                self.SendServers()
        self.Database.Close()
        self.ClientSocket.close()
