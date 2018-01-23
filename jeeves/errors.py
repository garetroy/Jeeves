class JeevesException(Exception):
    """ 
        Base exception class for jeeves
    """
    pass


class UserNotAdded(JeevesException):
    def __init__(self, name, *args): 
        self.name    = name
        self.message = "{} is not added to anything or is non-existant"\
            .format(name)

class UserInsufficentPermissions(JeevesException):
    def __init__(self, name, *args):
        self.name    = name
        self.message = "{} does not have sufficent permissions".format(name)
