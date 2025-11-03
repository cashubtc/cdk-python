"""Tests for wallet creation, configuration, and basic operations."""

import pytest
from cdk import Wallet, WalletConfig, Database, CurrencyUnit
from conftest import FAKE_MINT_URL, TEST_MNEMONIC


class TestWalletCreation:
    """Test wallet instantiation and configuration."""

    def test_wallet_creation_memory(self, wallet_config):
        """Test creating a wallet with in-memory database."""
        database = Database.memory()
        wallet = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database,
            config=wallet_config
        )
        assert wallet is not None

    def test_wallet_creation_sqlite(self, wallet_config, temp_db_path):
        """Test creating a wallet with SQLite database."""
        database = Database.sqlite(temp_db_path)
        wallet = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database,
            config=wallet_config
        )
        assert wallet is not None

    def test_wallet_config_basic(self):
        """Test basic wallet configuration creation."""
        config = WalletConfig(target_proof_count=3)
        assert config is not None
        assert config.target_proof_count == 3

    def test_wallet_config_with_target_proofs(self):
        """Test wallet configuration with target proof count."""
        config = WalletConfig(target_proof_count=5)
        assert config is not None
        assert config.target_proof_count == 5

    def test_wallet_with_config_fixture(self, test_wallet):
        """Test wallet creation using fixture."""
        assert test_wallet is not None


class TestWalletBalance:
    """Test wallet balance operations."""

    @pytest.mark.asyncio
    async def test_initial_balance_zero(self, test_wallet):
        """Test that a new wallet has zero balance."""
        balance = await test_wallet.total_balance()
        assert balance.value == 0

    @pytest.mark.asyncio
    async def test_pending_balance_zero(self, test_wallet):
        """Test that a new wallet has zero pending balance."""
        pending = await test_wallet.total_pending_balance()
        assert pending.value == 0

    @pytest.mark.asyncio
    async def test_reserved_balance_zero(self, test_wallet):
        """Test that a new wallet has zero reserved balance."""
        reserved = await test_wallet.total_reserved_balance()
        assert reserved.value == 0


class TestWalletErrorHandling:
    """Test error handling in wallet operations."""

    def test_invalid_mint_url(self):
        """Test that invalid mint URL is rejected during wallet creation."""
        from cdk.cdk import FfiError
        config = WalletConfig(target_proof_count=3)
        database = Database.memory()

        # Creating wallet with invalid URL should raise an exception
        with pytest.raises(FfiError.InvalidUrl):
            wallet = Wallet(
                mint_url="not-a-valid-url",
                unit=CurrencyUnit.SAT(),
                mnemonic=TEST_MNEMONIC,
                db=database,
                config=config
            )

    @pytest.mark.network
    @pytest.mark.asyncio
    async def test_network_operation_with_fake_mint(self, test_wallet):
        """Test that network operations fail gracefully with fake mint."""
        # This should raise an exception or return an error
        # since we're using a fake mint URL
        # get_mint_info() may return None instead of raising for fake URLs
        result = await test_wallet.get_mint_info()
        # Either it returns None or raises an exception
        assert result is None or isinstance(result, Exception)


class TestWalletDatabasePersistence:
    """Test wallet data persistence across instances."""

    @pytest.mark.asyncio
    async def test_sqlite_persistence(self, wallet_config, temp_db_path):
        """Test that wallet data persists in SQLite database."""
        # Create first wallet instance
        database1 = Database.sqlite(temp_db_path)
        wallet1 = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database1,
            config=wallet_config
        )

        # Perform some operation (balance check)
        balance1 = await wallet1.total_balance()
        assert balance1.value == 0

        # Create second wallet instance with same database
        database2 = Database.sqlite(temp_db_path)
        wallet2 = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=database2,
            config=wallet_config
        )

        # Should have same balance
        balance2 = await wallet2.total_balance()
        assert balance2.value == balance1.value


class TestWalletCurrencyUnits:
    """Test wallet with different currency units."""

    def test_wallet_with_sat_unit(self, memory_database):
        """Test wallet with satoshi unit."""
        config = WalletConfig(target_proof_count=3)
        wallet = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.SAT(),
            mnemonic=TEST_MNEMONIC,
            db=memory_database,
            config=config
        )
        assert wallet is not None

    def test_wallet_with_msat_unit(self, memory_database):
        """Test wallet with millisatoshi unit."""
        config = WalletConfig(target_proof_count=3)
        wallet = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.MSAT(),
            mnemonic=TEST_MNEMONIC,
            db=memory_database,
            config=config
        )
        assert wallet is not None

    def test_wallet_with_usd_unit(self, memory_database):
        """Test wallet with USD unit."""
        config = WalletConfig(target_proof_count=3)
        wallet = Wallet(
            mint_url=FAKE_MINT_URL,
            unit=CurrencyUnit.USD(),
            mnemonic=TEST_MNEMONIC,
            db=memory_database,
            config=config
        )
        assert wallet is not None
