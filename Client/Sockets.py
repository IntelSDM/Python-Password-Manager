import ssl
import socket
class Sockets:

    def Start():
        print("test")
        ClientSocket = socket.socket()

        # Wrap the socket in a SSL context
        Context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        Context.check_hostname = False
        Context.verify_mode = ssl.CERT_NONE
        ClientSocket = Context.wrap_socket(ClientSocket,server_hostname=None)# define hostname to none as a dns hasn't been set.
        
        # Connect to the server
        ClientSocket.connect(('localhost', 8000))

        # Receive a message from the server
        Message = ClientSocket.recv(1024).decode()
        print(Message)

        # Send a message to the server
        ClientSocket.send('Hello from the client!'.encode())

        # Close the socket
        ClientSocket.close()