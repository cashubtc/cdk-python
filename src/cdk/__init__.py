"""
CDK Python - Python bindings for the Cashu Development Kit.

This module provides Python access to the Cashu Development Kit (CDK) wallet
functionality through UniFFI-generated bindings.

Example:
    >>> from cdk import Wallet, WalletConfig, Database
    >>> database = Database.memory()
    >>> config = WalletConfig(mint_url="https://mint.example.com", unit="sat")
    >>> wallet = Wallet(config, database)
    >>> balance = wallet.total_balance()
"""

__version__ = "0.13.0"  # Updated automatically by CI during release
__author__ = "CDK Developers"
__license__ = "MIT"

# The actual bindings will be imported from the generated cdk.py file
# This __init__.py serves as the package entry point and provides metadata

try:
    # Import all public APIs from the generated bindings
    from .cdk import *  # noqa: F401, F403
    from .cdk import WalletSqliteDatabase, WalletPostgresDatabase
except ImportError as e:
    import sys
    print(
        "Error: CDK Python bindings not found. "
        "Please run 'just generate' to build the bindings.",
        file=sys.stderr
    )
    raise ImportError(
        "CDK bindings not generated. Run 'just generate' to build them."
    ) from e


class Database:
    """
    Convenience wrapper for creating database backends.

    This class provides simple static methods for creating different
    database backends (memory, SQLite, PostgreSQL).
    """

    @staticmethod
    def memory():
        """
        Create an in-memory SQLite database.

        Returns:
            WalletSqliteDatabase: An in-memory database instance.
        """
        return WalletSqliteDatabase(":memory:")

    @staticmethod
    def sqlite(file_path: str):
        """
        Create a SQLite database at the given file path.

        Args:
            file_path: Path to the SQLite database file.

        Returns:
            WalletSqliteDatabase: A SQLite database instance.
        """
        return WalletSqliteDatabase(file_path)

    @staticmethod
    def postgres(connection_string: str):
        """
        Create a PostgreSQL database connection.

        Args:
            connection_string: PostgreSQL connection string.
                Example: "host=localhost user=test password=test dbname=testdb"

        Returns:
            WalletPostgresDatabase: A PostgreSQL database instance.
        """
        return WalletPostgresDatabase(connection_string)
