"""Shared test fixtures and utilities for CDK Python tests."""

import os
import tempfile
import uuid
from pathlib import Path

import pytest


# Fake mint URL for testing (will fail network operations, which is intended for offline tests)
FAKE_MINT_URL = "https://fake-mint.example.com"
TEST_MNEMONIC = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_db_path(temp_dir):
    """Create a temporary database file path."""
    db_path = temp_dir / f"test_wallet_{uuid.uuid4()}.db"
    yield str(db_path)
    # Cleanup is automatic via temp_dir fixture


@pytest.fixture
def memory_database():
    """Create an in-memory database for testing."""
    from cdk import WalletDbBackend, create_wallet_db
    backend = WalletDbBackend.SQLITE(path=":memory:")
    return create_wallet_db(backend)


@pytest.fixture
def sqlite_database(temp_db_path):
    """Create a SQLite database for testing."""
    from cdk import WalletDbBackend, create_wallet_db
    backend = WalletDbBackend.SQLITE(path=temp_db_path)
    return create_wallet_db(backend)


@pytest.fixture
def wallet_config():
    """Create a basic wallet configuration for testing."""
    from cdk import WalletConfig
    return WalletConfig(target_proof_count=3)


@pytest.fixture
def wallet_config_with_targets():
    """Create a wallet configuration with target proof counts."""
    from cdk import WalletConfig
    return WalletConfig(target_proof_count=5)


@pytest.fixture
def test_wallet(wallet_config, memory_database):
    """Create a test wallet with in-memory database."""
    from cdk import Wallet, CurrencyUnit
    return Wallet(
        mint_url=FAKE_MINT_URL,
        unit=CurrencyUnit.SAT(),
        mnemonic=TEST_MNEMONIC,
        db=memory_database,
        config=wallet_config
    )


@pytest.fixture
def test_wallet_sqlite(wallet_config, sqlite_database):
    """Create a test wallet with SQLite database."""
    from cdk import Wallet, CurrencyUnit
    return Wallet(
        mint_url=FAKE_MINT_URL,
        unit=CurrencyUnit.SAT(),
        mnemonic=TEST_MNEMONIC,
        db=sqlite_database,
        config=wallet_config
    )


def skip_if_no_network():
    """Skip test if network is not available or desired."""
    if os.environ.get("SKIP_NETWORK_TESTS"):
        pytest.skip("Network tests disabled")


def skip_if_no_postgres():
    """Skip test if PostgreSQL is not available."""
    if not os.environ.get("POSTGRES_CONNECTION_STRING"):
        pytest.skip("PostgreSQL not configured")
