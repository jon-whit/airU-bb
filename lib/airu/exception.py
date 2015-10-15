
class RetryException(Exception):
    """
    A RetryException is raised when a retry count is exceeded when
    trying to execute a given function.
    """
    pass

class InitException(Exception):
    """
    An InitException is raised if an exceptional case occurs in the initialization
    of a given object.
    """
    pass