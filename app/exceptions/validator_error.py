class ValidatorError(Exception):
    """Exception raised when an argument is invalid.
    Attributes:
        argument -- Argument that is invalid
        value -- Invalid argument value
    """

    def __init__(self, field_name: str, error_message: str = ''):
        self.field_name = field_name

        if error_message != '':
            error_message = f'Error: {error_message}'

        message: str = f"field '{field_name}' has an incorrect value.{error_message}"

        super().__init__(message)
