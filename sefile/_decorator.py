# sefile/_decorator.py

from sefile import (
    Optional, 
    functools, 
    logging
    )
from sefile.logging import log_file

# decorator for logging
def do_log(func=None, 
           message: Optional[str] = None, 
           pause: bool = True, 
           format: str = '%(name)s | %(asctime)s %(levelname)s - %(message)s'
           ) -> None:
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if pause:
                return func(*args, **kwargs)
            else:
                try:
                    some_object = func(*args, **kwargs)
                except Exception as error:
                    logging.basicConfig(filename=log_file(), filemode='a+', 
                            format=format,
                            level=logging.ERROR)
                    logging.error(error)
                    raise error
                else:
                    logging.basicConfig(filename=log_file(), 
                            filemode='a+', 
                            format='%(name)s | %(asctime)s %(levelname)s - %(message)s', 
                            level=logging.INFO)
                    logging.info(message)
            return some_object
        return wrapper
    return decorator

