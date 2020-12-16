# Local Imports
from .sql_config import SQLConfiguration


# DB configuration inspection and initialization
DB_CONFIG = SQLConfiguration()
print(DB_CONFIG.URI)

db = DB_CONFIG.get_db()

