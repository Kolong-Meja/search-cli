# sefile/exception.py

"""
TODO: Create custom exception for certain cases.
"""

class InvalidFormat(Exception): ...
class InvalidFileFormat(Exception): ...
class RequiredFile(Exception): ...

def exception_factory(exception, message: str) -> Exception:
    """
    custom exception factory
    """
    raise exception(message)
