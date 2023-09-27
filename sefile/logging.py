# search/logs.py

from sefile import (
    dataclass,
    os, 
    pathlib, 
    logging,
    functools,
    )


def log_file():
    fullpath = os.path.join(pathlib.Path.cwd(), 'search', 'logs')
    has_dir = os.path.isdir(fullpath)
    
    if has_dir:
        file_target = os.path.join(fullpath, 'log.txt')
        return file_target
    else:
        pathlib.Path(fullpath).mkdir(exist_ok=False)
        file_target = os.path.join(fullpath, 'log.txt')
        return file_target

# create factory for exception.
def exception_factory(exception, message: str) -> Exception:
    return exception(message)

# def info_logging(func, message: str, pause: bool = False):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             value = func(*args, **kwargs)
#             return value
#         return wrapper
    
#     if not pause:
#         pass
#     else:
#         logging.basicConfig(filename=log_file(), 
#                             filemode='a+', 
#                             format='%(name)s | %(asctime)s %(levelname)s - %(message)s', 
#                             level=logging.INFO)
#         logging.info(message)

# @dataclass(frozen=True)
# class CustomLogging:
#     format_log: str = '%(name)s | %(asctime)s %(levelname)s - %(message)s'

#     def __str__(self) -> None:
#         return f"({self.format_log})"

#     def __repr__(self) -> None:
#         return f"{self.__class__.__name__}({self.format_log})"
    
#     def info_log(self, func, message: str) -> None:
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             logging.basicConfig(filename=log_file(), filemode='a+', 
#                                 format=self.format_log,
#                                 level=logging.INFO)
#             logging.info(message)
    
#     def error_log(self, exception, message: str) -> None:
#         logging.basicConfig(filename=log_file(), filemode='a+', 
#                             format=self.format_log,
#                             level=logging.ERROR)
#         logging.error(message)
#         raise exception_factory(exception, message)
    
#     def debug_log(self, message: str) -> None:
#         logging.basicConfig(filename=log_file(), filemode='a+', 
#                             format=self.format_log,
#                             level=logging.DEBUG)
#         logging.error(message)
    
#     def warning_log(self, message: str) -> None:
#         logging.basicConfig(filename=log_file(), filemode='a+', 
#                             format=self.format_log,
#                             level=logging.WARNING)
#         logging.error(message)
    
#     def critical_log(self, message: str) -> None:
#         logging.basicConfig(filename=log_file(), filemode='a+', 
#                             format=self.format_log,
#                             level=logging.CRITICAL)
#         logging.error(message)
    
#     def notset_log(self, message: str) -> None:
#         logging.basicConfig(filename=log_file(), filemode='a+', 
#                             format=self.format_log,
#                             level=logging.NOTSET)
#         logging.error(message)

