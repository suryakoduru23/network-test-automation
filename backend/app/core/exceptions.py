"""Custom Exceptions"""


class APIException(Exception):
    """Base API Exception"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(APIException):
    """Authentication failed"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class AuthorizationError(APIException):
    """Authorization failed"""
    def __init__(self, message: str = "Authorization failed"):
        super().__init__(message, 403)


class ResourceNotFoundError(APIException):
    """Resource not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class ValidationError(APIException):
    """Validation error"""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, 422)


class SSHConnectionError(APIException):
    """SSH connection error"""
    def __init__(self, message: str = "SSH connection failed"):
        super().__init__(message, 500)


class TestExecutionError(APIException):
    """Test execution error"""
    def __init__(self, message: str = "Test execution failed"):
        super().__init__(message, 500)
