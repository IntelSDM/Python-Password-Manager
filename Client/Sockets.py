import ssl
import socket
import sys
import select

class Sockets:

    ClientSocket = None
    def RecieveMessage(self):
        while True:
            chunk = self.ClientSocket.recv(4096).decode() # Recieve on itteration for multiple messages and decode them
            if(chunk != None):
                return chunk # Loop Until Nothing Is Left. Dont Add Empty Chunk To Buffer. Return When Nothing Left


    def SendMessage(self, message:str):
            #Send Encrypted Message
            return self.ClientSocket.send(message.encode())
    def Close(self):
        # Close the socket
        self.ClientSocket.close()
    def Start(self):
        self.ClientSocket = socket.socket()

        # Wrap the socket in a SSL context
        Context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        Context.check_hostname = False # Disable hostname check as dns isn't set
        Context.verify_mode = ssl.CERT_NONE # Disable verify mode to prevent bugs verifying the CA
        self.ClientSocket = Context.wrap_socket(self.ClientSocket,server_hostname=None)# Define hostname to none as a dns hasn't been set.
        
        # Connect to the server
        self.ClientSocket.connect(('localhost', 8008))