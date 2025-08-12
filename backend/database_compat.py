"""
Backward compatibility module for database imports
This allows existing code to continue working while we migrate to the new structure
"""

# Import everything from the new database package
from database import *

# This file can be removed once all imports are updated to use:
# from database import ...
# instead of:
# from database import ...
# from database_utils import ...
# from models import ...