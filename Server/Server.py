import DatabaseHandler
import Sockets
import threading

Sock = Sockets.Sockets()




# Main is our initializer for general usage
def Main():
    """
    Initialize the sockets for the server
    Initialize the listening thread to accept clients
    """
    Sock.Start()
    listeningthread = threading.Thread(target=Sock.Listen) # create thread to listen for clients
    listeningthread.start()

Main() # Execute Main
