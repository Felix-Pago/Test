class FormatterError(Exception):
    """Exception raised when a formatting operation can't be completed.
    Attributes:
        formatter_name -- Name of the formatter that was applied
        error_message -- Message of error
    """

    def __init__(self, formatter_name: str, error_message: str = ''):
        if error_message != '':
            error_message = f'Error: {error_message}'

        message: str = f"Couldn't format field '{formatter_name}'. {error_message}"

        super().__init__(message)
