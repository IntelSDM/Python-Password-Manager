class Server:
    def __init__(self, serverid:str ):
        """
        Initializer which sets the serverid for the server instance
        """
        self.ServerID = serverid

    def SetPassword(self,password:str):
        """
        Public function allows external callers to save passwords
        """
        self.Password = password

    def SetUsername(self,username:str):
        """
        Public function allows external callers to save usernames
        """
        self.Username = username

    def SetServerName(self,servername:str):
        """
        Public function allows external callers to save server names
        """
        self.ServerName = servername
