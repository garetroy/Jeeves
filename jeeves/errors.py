class JeevesException(Exception):
    """ 
        Base exception class for jeeves
    """
    pass


class UserNotAdded(JeevesException):
    def __init__(self, name, *args): 
        self.name    = name
        self.message = "{} is not added to anything or is a non-existant user"\
            .format(name)

class UserInsufficentPermissions(JeevesException):
    def __init__(self, name, *args):
        self.name    = name
        self.message = "{} does not have sufficent permissions".format(name)

class BadInput(JeevesException):
    def __init__(self, message):
        self.message = message

class InvalidType(JeevesException):
    def __init__(self, type1, type2, location):
        self.message = "Got type:{} but expected type:{} - in {}".format(\
            type1,type2,location)
