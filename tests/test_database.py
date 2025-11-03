"""Tests for database backends (Memory, SQLite, PostgreSQL)."""

import os
import pytest
from pathlib import Path
from cdk import Database, Wallet, WalletConfig, CurrencyUnit
from conftest import FAKE_MINT_URL, TEST_MNEMONIC


class TestMemoryDatabase:
    """Test in-memory database backend."""

    def test_memory_database_creation(self):
        """Test creating an in-memory database."""
        database = Database.memory()
        assert database is not None

    @pytest.mark.asyncio
    async def test_memory_database_with_wallet(self, wallet_config):
        """Test using in-memory database with wallet."""
        database = Database.memory()
        wallet = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database,
            config=wallet_config
        )
        assert wallet is not None
        balance = await wallet.total_balance()
        assert balance.value == 0

    @pytest.mark.asyncio
    async def test_memory_database_isolation(self, wallet_config):
        """Test that each memory database is isolated."""
        database1 = Database.memory()
        database2 = Database.memory()

        wallet1 = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database1,
            config=wallet_config
        )
        wallet2 = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database2,
            config=wallet_config
        )

        # Each wallet should have independent state
        balance1 = await wallet1.total_balance()
        balance2 = await wallet2.total_balance()
        assert balance1.value == 0
        assert balance2.value == 0


class TestSQLiteDatabase:
    """Test SQLite database backend."""

    def test_sqlite_database_creation(self, temp_db_path):
        """Test creating a SQLite database."""
        database = Database.sqlite(temp_db_path)
        assert database is not None

    def test_sqlite_file_created(self, temp_db_path, wallet_config):
        """Test that SQLite database file is created."""
        database = Database.sqlite(temp_db_path)
        wallet = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database,
            config=wallet_config
        )

        # File should exist after wallet creation
        assert Path(temp_db_path).exists()

    @pytest.mark.asyncio
    async def test_sqlite_persistence(self, temp_db_path, wallet_config):
        """Test that data persists between wallet instances."""
        # Create first wallet
        database1 = Database.sqlite(temp_db_path)
        wallet1 = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database1,
            config=wallet_config
        )
        initial_balance = await wallet1.total_balance()

        # Close first wallet (in Python, this happens when object is garbage collected)
        del wallet1
        del database1

        # Open second wallet with same database
        database2 = Database.sqlite(temp_db_path)
        wallet2 = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database2,
            config=wallet_config
        )
        persisted_balance = await wallet2.total_balance()

        # Balance should be the same
        assert persisted_balance.value == initial_balance.value

    def test_sqlite_with_relative_path(self, temp_dir):
        """Test SQLite database with relative path."""
        db_name = "test_wallet.db"
        db_path = temp_dir / db_name

        database = Database.sqlite(str(db_path))
        assert database is not None

    def test_sqlite_with_absolute_path(self, temp_db_path):
        """Test SQLite database with absolute path."""
        # temp_db_path is already absolute
        database = Database.sqlite(temp_db_path)
        assert database is not None
        assert Path(temp_db_path).is_absolute()


class TestPostgreSQLDatabase:
    """Test PostgreSQL database backend."""

    @pytest.mark.skipif(
        not os.environ.get("POSTGRES_CONNECTION_STRING"),
        reason="PostgreSQL not configured"
    )
    def test_postgres_database_creation(self):
        """Test creating a PostgreSQL database connection."""
        connection_string = os.environ["POSTGRES_CONNECTION_STRING"]
        database = Database.postgres(connection_string)
        assert database is not None

    @pytest.mark.skipif(
        not os.environ.get("POSTGRES_CONNECTION_STRING"),
        reason="PostgreSQL not configured"
    )
    def test_postgres_with_wallet(self, wallet_config):
        """Test using PostgreSQL database with wallet."""
        connection_string = os.environ["POSTGRES_CONNECTION_STRING"]
        database = Database.postgres(connection_string)
        wallet = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database,
            config=wallet_config
        )
        assert wallet is not None

    @pytest.mark.skipif(
        not os.environ.get("POSTGRES_CONNECTION_STRING"),
        reason="PostgreSQL not configured"
    )
    @pytest.mark.asyncio
    async def test_postgres_persistence(self, wallet_config):
        """Test that data persists in PostgreSQL between wallet instances."""
        connection_string = os.environ["POSTGRES_CONNECTION_STRING"]

        # Create first wallet
        database1 = Database.postgres(connection_string)
        wallet1 = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database1,
            config=wallet_config
        )
        initial_balance = await wallet1.total_balance()

        # Close first wallet
        del wallet1
        del database1

        # Open second wallet with same connection
        database2 = Database.postgres(connection_string)
        wallet2 = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database2,
            config=wallet_config
        )
        persisted_balance = await wallet2.total_balance()

        # Balance should be the same
        assert persisted_balance.value == initial_balance.value


class TestDatabaseSwitching:
    """Test switching between different database backends."""

    @pytest.mark.asyncio
    async def test_switch_from_memory_to_sqlite(self, wallet_config, temp_db_path):
        """Test that different database types can be used."""
        # Use memory database
        memory_db = Database.memory()
        wallet_memory = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=memory_db,
            config=wallet_config
        )
        memory_balance = await wallet_memory.total_balance()
        assert memory_balance.value == 0

        # Use SQLite database (different wallet instance)
        sqlite_db = Database.sqlite(temp_db_path)
        wallet_sqlite = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=sqlite_db,
            config=wallet_config
        )
        sqlite_balance = await wallet_sqlite.total_balance()
        assert sqlite_balance.value == 0

        # They should be independent
        assert wallet_memory is not wallet_sqlite
