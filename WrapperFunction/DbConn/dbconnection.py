import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DatabaseSessionManager:
    """
    A class that manages the database session and connection.
    """

    def __init__(self):
        self._engine: create_engine| None = None
        self._sessionmaker: sessionmaker | None = None

    def init(self, host: str):
        """
        Initializes the database session manager with the given host.

        Args:
            host (str): The database host.

        Returns:
            None
        """
        self._engine = create_engine(host)
        self._sessionmaker = sessionmaker(autocommit=False, bind=self._engine)

    def close(self):
        """
        Closes the database session manager.

        Raises:
            Exception: If the database session manager is not initialized.

        Returns:
            None
        """
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        self._engine.dispose()
        self._engine = None
        self._sessionmaker = None


    def connect(self):
        """
        Connects to the database.

        Raises:
            Exception: If the database session manager is not initialized.

        Returns:
            connection: The database connection.
        """
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        with self._engine.begin() as connection:
            try:
                return connection
            except Exception:
                connection.rollback()
                raise

    def session(self):
        """
        Creates a new database session.

        Raises:
            Exception: If the database session manager is not initialized.

        Returns:
            session: The database session.
        """
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            return session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


sessionmanager = DatabaseSessionManager()


def get_db():
    """
    Returns a database session.

    Returns:
        session: The database session.
    """
    with sessionmanager.session() as session:
        return session