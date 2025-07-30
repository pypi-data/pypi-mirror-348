class fuiException(Exception):
    pass


class fuiUnsupportedPlatformException(fuiException):
    """
    Thrown by operations that are not supported on the current platform.
    """

    def __init__(self, message: str):
        super().__init__(message)


class fuiUnimplementedPlatformEception(fuiUnsupportedPlatformException):
    """
    Thrown by operations that have not been implemented yet.
    """

    pass
