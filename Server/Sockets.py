import ssl
import socket
import sys
import select
# Generate a self-signed certificate and key
CertPath = 'Certs/PythonServer.crt'
KeyPath = 'Certs/PythonServer.key'

class Sockets:
    ClientSocket = None
    ServerSocket = None
    def RecieveMessage(self):
        # Initialize an empty buffer to hold the message
        buffer = bytearray()

        # Keep reading until the connection is closed or the message is complete
        while True:
            # Use select to check if there is data available to be read
            rlist, _, _ = select.select([self.ClientSocket], [], [], 0)
            if rlist:
                # Read a chunk of the message
                chunk = self.ClientSocket.recv(4096)

                # If the chunk is empty, the connection has been closed
                if not chunk:
                    raise ConnectionError('Connection closed by other end')

                # Add the chunk to the buffer
                buffer.extend(chunk)
            else:
                # No data available to be read, so we can break out of the loop
                break

        # Decode the message and return it
        return buffer.decode()
    def SendMessage(self, message:str):
        # Check if the client socket is still open
        if self.ClientSocket is not None:
            #Send Encrypted Message
            return self.ClientSocket.send(message.encode())
    def Close(self):
        # Close the client socket
        self.ClientSocket.close()

        # Close the server socket
        self.ServerSocket.close()
    def Start(self):
        # Create a socket
        self.ServerSocket = socket.socket()

        # Bind the socket to a port
        self.ServerSocket.bind(('localhost', 8000))

        # Listen for incoming connections
        self.ServerSocket.listen()

        # Accept an incoming connection
        self.ClientSocket, ClientAddress = self.ServerSocket.accept()

        # Wrap the client socket in a SSL context
        Context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        Context.load_cert_chain(CertPath, KeyPath)
        Context.verify_mode = ssl.CERT_NONE # Disable verify mode to prevent bugs verifying the CA
        self.ClientSocket = Context.wrap_socket(self.ClientSocket, server_side=True)
        