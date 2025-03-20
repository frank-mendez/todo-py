class CustomError(Exception):
    """Base class for other exceptions"""
    pass

class NotFoundError(CustomError):
    """Raised when a resource is not found"""
    pass

class ValidationError(CustomError):
    """Raised when there is a validation error"""
    pass

class UnauthorizedError(CustomError):
    """Raised when the user is not authorized"""
    pass

class ConflictError(CustomError):
    """Raised when there is a conflict"""
    pass
