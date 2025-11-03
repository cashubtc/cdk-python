"""Basic tests to verify CDK Python bindings work."""

import pytest


class TestImports:
    """Test that all major modules can be imported."""

    def test_import_cdk(self):
        """Test that cdk module can be imported."""
        import cdk
        assert cdk is not None

    def test_wallet_class_exists(self):
        """Test that Wallet class exists."""
        from cdk import Wallet
        assert Wallet is not None

    def test_database_functions_exist(self):
        """Test that database creation functions exist."""
        from cdk import WalletDbBackend, create_wallet_db
        assert WalletDbBackend is not None
        assert create_wallet_db is not None

    def test_config_class_exists(self):
        """Test that WalletConfig class exists."""
        from cdk import WalletConfig
        assert WalletConfig is not None

    def test_currency_unit_exists(self):
        """Test that CurrencyUnit enum exists."""
        from cdk import CurrencyUnit
        assert CurrencyUnit is not None


class TestDatabaseCreation:
    """Test database creation."""

    def test_create_memory_database(self):
        """Test creating in-memory database."""
        from cdk import WalletDbBackend, create_wallet_db
        backend = WalletDbBackend.SQLITE(path=":memory:")
        db = create_wallet_db(backend)
        assert db is not None

    def test_create_sqlite_database(self, temp_db_path):
        """Test creating SQLite database."""
        from cdk import WalletDbBackend, create_wallet_db
        backend = WalletDbBackend.SQLITE(path=temp_db_path)
        db = create_wallet_db(backend)
        assert db is not None


class TestWalletConfig:
    """Test wallet configuration."""

    def test_create_wallet_config(self):
        """Test creating wallet configuration."""
        from cdk import WalletConfig
        config = WalletConfig(target_proof_count=3)
        assert config is not None

    def test_wallet_config_with_none(self):
        """Test creating wallet configuration with None."""
        from cdk import WalletConfig
        config = WalletConfig(target_proof_count=None)
        assert config is not None


class TestWalletCreation:
    """Test wallet creation."""

    def test_create_wallet(self, wallet_config, memory_database):
        """Test creating a wallet."""
        from cdk import Wallet, CurrencyUnit
        wallet = Wallet(
            mint_url="https://mint.example.com",
            unit=CurrencyUnit.SAT(),
            mnemonic="abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
            db=memory_database,
            config=wallet_config
        )
        assert wallet is not None

    def test_wallet_with_fixture(self, test_wallet):
        """Test that wallet fixture works."""
        assert test_wallet is not None


@pytest.mark.asyncio
class TestWalletOperations:
    """Test basic wallet operations."""

    async def test_wallet_total_balance(self, test_wallet):
        """Test getting total balance."""
        balance = await test_wallet.total_balance()
        assert balance is not None
        # Balance should be Amount type
        assert hasattr(balance, 'value')
        assert balance.value == 0

    async def test_wallet_pending_balance(self, test_wallet):
        """Test getting pending balance."""
        pending = await test_wallet.total_pending_balance()
        assert pending is not None
        assert hasattr(pending, 'value')
        assert pending.value == 0

    async def test_wallet_reserved_balance(self, test_wallet):
        """Test getting reserved balance."""
        reserved = await test_wallet.total_reserved_balance()
        assert reserved is not None
        assert hasattr(reserved, 'value')
        assert reserved.value == 0


class TestCurrencyUnits:
    """Test currency unit enums."""

    def test_currency_unit_sat(self):
        """Test SAT currency unit."""
        from cdk import CurrencyUnit
        sat = CurrencyUnit.SAT()
        assert sat is not None

    def test_currency_unit_msat(self):
        """Test MSAT currency unit."""
        from cdk import CurrencyUnit
        msat = CurrencyUnit.MSAT()
        assert msat is not None

    def test_currency_unit_usd(self):
        """Test USD currency unit."""
        from cdk import CurrencyUnit
        usd = CurrencyUnit.USD()
        assert usd is not None
