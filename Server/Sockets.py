import ssl
import socket

# Generate a self-signed certificate and key
CertPath = 'Certs/PythonServer.crt'
KeyPath = 'Certs/PythonServer.key'

class Sockets:

    def Start():
        # Create a socket
        ServerSocket = socket.socket()

        # Bind the socket to a port
        ServerSocket.bind(('localhost', 8000))

        # Listen for incoming connections
        ServerSocket.listen()

        # Accept an incoming connection
        ClientSocket, ClientAddress = ServerSocket.accept()

        # Wrap the client socket in a SSL context
        Context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        Context.load_cert_chain(CertPath, KeyPath)
        Context.verify_mode = ssl.CERT_NONE
        ClientSocket = Context.wrap_socket(ClientSocket, server_side=True)

        # Send a message to the client
        ClientSocket.send('Hello from the server!'.encode())

        # Receive a message from the client
        Message = ClientSocket.recv(1024).decode()
        print(Message)
        
        # Close the client socket
        ClientSocket.close()
        
        # Close the server socket
        ServerSocket.close()