# Setup the configuration and connection for the MySQLDB

# Third Party Packages
import os
from flask_sqlalchemy import SQLAlchemy

# Local Imports
from .exceptions import MissingEnvVariable

DEFAULT_DB_NAME = 'learning'


class SQLConfiguration:

    def __init__(self):
        # Fetch Auth credentials
        self.__fetch_db_credentials()

        # Setup default credentials
        self.MYSQL_DATABASE_HOST = os.getenv('MYSQL_DATABASE_HOST', 'localhost')
        self.MYSQL_DATABASE_PORT = os.getenv('MYSQL_DATABASE_PORT', 3306)
        self.MYSQL_DATABASE_DB = os.getenv('MYSQL_DATABASE_DB', DEFAULT_DB_NAME)

        # Construct the URI
        self.URI = f'mysql://{self.MYSQL_DATABASE_HOST}:{self.MYSQL_DATABASE_PORT}/{self.MYSQL_DATABASE_DB}'

    def __fetch_db_credentials(self):
        """Inspect environment for required DB auth credentials
        :raises: MissingEnvVariable if either username or password is missing
        """
        for ky in ('MYSQL_DATABASE_USER', 'MYSQL_DATABASE_PASSWORD'):
            if ky not in os.environ.keys():
                raise MissingEnvVariable(ky)

        # Set the variables as long as they're there
        self.__db_user = os.environ['MYSQL_DATABASE_USER']
        self.__db_pw = os.environ['MYSQL_DATABASE_PASSWORD']

    def get_db(self) -> SQLAlchemy:
        """Creates the DB instance, adds generic user to active session
        :return: Return the DB object that will be bound to the current app
        """
        db = SQLAlchemy()
        # Create the user connection
        return db
