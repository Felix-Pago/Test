from app.entities.exceptions.server_error_type import ServerErrorType


class ServerError(Exception):
    """Exception raised when there is an error caused by the server.

    Attributes:
        server_error_type -- Enum that identifies the specific error.
        message -- Human readable message to provide information about the error.
    """

    def __init__(self, server_error_type: ServerErrorType, message: str = ''):
        self.server_error_type: ServerErrorType = server_error_type
        self.message = message

        super().__init__(message)
