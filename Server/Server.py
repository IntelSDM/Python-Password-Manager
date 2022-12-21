import DatabaseHandler
import Sockets
# Main is our initializer for general usage
def Main():
    db = DatabaseHandler.Database("Testdb.json")
    Sockets.Sockets.Start()
    print("Test")
Main() # Execute Main
