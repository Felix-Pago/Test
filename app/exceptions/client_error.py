from app.entities.exceptions.client_error_type import ClientErrorType


class ClientError(Exception):
    """Exception raised when there is an error caused by the client.

    Attributes:
        client_error_type -- Enum that identifies the specific error.
        message -- Human readable message to provide information about the error.
    """

    def __init__(self, client_error_type: ClientErrorType, message: str = ''):
        self.client_error_type: ClientErrorType = client_error_type
        self.message = message

        super().__init__(message)
