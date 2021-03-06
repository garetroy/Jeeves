class JeevesException(Exception):
    """ 
        Base exception class for jeeves.
    """
    pass


class UserNotAdded(JeevesException):
    """
        An JeevesException that raises when there is not a user added to the
        server or "not found".

        Parameters
        ----------
        name : string
            The name of the Member not found.
        
        Attributes
        ----------
        message : string
            The message that is generated from this error.
    """
    def __init__(self, name): 
        self.name    = name
        self.message = "{} is not added to anything or is a non-existant user"\
            .format(name)

class UserInsufficentPermissions(JeevesException):
    """
        An JeevesException that raises when a Member does not have sufficent
        permissions.

        Parameters
        -----------
        name : string
            The name of the Member not found.
        
        Attributes
        ----------
        message : string
            The message that is generated from this error.
    """
    def __init__(self, name):
        self.name    = name
        self.message = "{} does not have sufficent permissions".format(name)

class BadInput(JeevesException):
    """
        An JeevesException that raises when the input was bad.

        Attributes
        ----------
        message : string
            The message that is generated from this error.
    """
    def __init__(self, message):
        self.message = message

class InvalidType(JeevesException):
    """
        An JeevesException that raises when the input was bad.

        Parameters
        -----------
        type1 : type
            The type we got.

        type2 : type
            The type we expected.
    
        location : str
            A string with the location of the incident.
        
        Attributes
        ----------
        message : str
            The message that is generated from this error.
    """
    def __init__(self, type1, type2, location):
        self.message = "Got type:{} but expected type:{} - in {}".format(\
            type1,type2,location)

class BadArgs(JeevesException):
    """
        A JeevesException that raises when bad **kwargs are passed in.

        Parameters
        -----------
        what : str
            What argument was bad.

        where : str
            Location where it was bad.
    
        why : str 
            Why the argument was bad.

        Attributes
        -----------
        message : str
            The message that is generated from this error.
    """
    def __init__(self,what,where,why):
        self.message = "{} at {} had a bad argument because {}".format(\
            what,where,why)
