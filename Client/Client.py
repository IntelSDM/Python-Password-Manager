import Sockets
# Main is our initializer for general usage
def Main():
    Sock = Sockets.Sockets()
    Sock.Start()
    username = input("Username:")
    Sock.SendMessage(username)
    password = input("Password:")
    Sock.SendMessage(password)
    print(Sock.RecieveMessage())
Main() # Execute Main
