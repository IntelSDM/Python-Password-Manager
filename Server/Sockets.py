import ssl
import socket
import sys
import select
import sys
import Client
# Generate a self-signed certificate and key
CertPath = 'Certs/PythonServer.crt'
KeyPath = 'Certs/PythonServer.key'

class Sockets:

    ClientSocket = None
    ServerSocket = None
    SocketList = []
    
    def Close(self):
        # Close the client socket
        self.ClientSocket.close()

        # Close the server socket
        self.ServerSocket.close()
    

    def Start(self):
        # Create a socket
        self.ServerSocket = socket.socket()

        # Bind the socket to a port
        self.ServerSocket.bind(('localhost', 8008))

        
        
    def Listen(self):
        """
        Listening thread, Listen for new client connections and add them to the client list
        """
        while(True):
            # Listen for incoming connections
            self.ServerSocket.listen()

            # Accept an incoming connection
            self.ClientSocket, self.ClientAddress = self.ServerSocket.accept()

            # Wrap the client socket in a SSL context
            self.Context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.Context.load_cert_chain(CertPath, KeyPath)
            self.Context.verify_mode = ssl.CERT_NONE # Disable verify mode to prevent bugs verifying the CA
            self.ClientSocket = self.Context.wrap_socket(self.ClientSocket, server_side=True)
            self.SocketList.append(Client.Client(self.ClientSocket))

            #  Clean up, Don't want to waste memory creating local variables
            self.ClientSocket = None 
            self.Context = None
