import ssl
import socket
import sys
import select

class Sockets:

    ClientSocket = None
    def RecieveMessage(self):
        # Initialize an empty buffer to hold the message
        buffer = bytearray()

        # Keep reading until the connection is closed or the message is complete
        while True:
            # Use select to check if there is data available to be read, Refreshes after 1 second
            rlist, _, _ = select.select([self.ClientSocket], [], [], 1)
            if rlist:
                # Read a chunk of the message
                chunk = self.ClientSocket.recv(4096)

                # If the chunk is empty, the connection has been closed
                if not chunk:
                    break

                # Add the chunk to the buffer
                buffer.extend(chunk)
            else:
                # No data available to be read, so we can break out of the loop
                break

        # Decode the message and return it
        return buffer.decode()
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
        self.ClientSocket.connect(('localhost', 8000))