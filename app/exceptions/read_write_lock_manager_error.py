class ReadWriteLockManagerError(Exception):
    """Exception raised when a Read lock manager member does not exist.
    Attributes:
        member_name -- Non-existing member
    """

    def __init__(self, member_name: str):
        message: str = f"{member_name} member does not exists on the read write lock manager"
        super().__init__(message)
