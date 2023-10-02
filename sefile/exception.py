# sefile/exception.py

"""
TODO: Create custom exception for certain cases.
"""

class InvalidFormat(Exception): ...
class InvalidFileFormat(Exception): ...
class InvalidFilename(Exception): ...
class InvalidPath(Exception): ...

def exception_factory(exception, message: str) -> Exception:
    """
    Custom exception factory
    """
    raise exception(message)
