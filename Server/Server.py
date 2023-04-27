import DatabaseHandler
import Sockets
import threading

Sock = Sockets.Sockets()




# Main is our initializer for general usage
def Main():
    Sock.Start()
    listeningthread = threading.Thread(target=Sock.Listen)
    listeningthread.start()

Main() # Execute Main
