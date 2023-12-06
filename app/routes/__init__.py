from .auth_routes import *
from .profile_routes import *

__all__ = []

auth_functions = [name for name in dir() if callable(eval(name)) and not name.startswith("__")]

__all__.extend(auth_functions)

profile_functions = [name for name in dir() if callable(eval(name)) and not name.startswith("__")]

__all__.extend(profile_functions)