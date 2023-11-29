from .auth_routes import *
from .profile_routes import *

__all__ = []

auth_functions = [name for name in dir() if callable(eval(name)) and not name.startswith("__")]

# Extend __all__ with the function names from auth_routes module
__all__.extend(auth_functions)

# Get all function names from profile_routes module
profile_functions = [name for name in dir() if callable(eval(name)) and not name.startswith("__")]

# Extend __all__ with the function names from profile_routes module
__all__.extend(profile_functions)