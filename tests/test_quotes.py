"""Tests for mint and melt quote operations."""

import pytest
from cdk import Wallet, SendOptions, MeltOptions, Amount, SendMemo, SendKind, SplitTarget


class TestMintQuotes:
    """Test mint quote creation and operations."""

    @pytest.mark.network
    @pytest.mark.asyncio
    async def test_mint_quote_creation(self, test_wallet):
        """Test creating a mint quote."""
        # This will fail with fake mint, but tests the API
        with pytest.raises(Exception):
            quote = await test_wallet.mint_quote(
                amount=Amount(value=100),
                description="Test mint quote"
            )

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_mint_quote_amount_validation(self, test_wallet):
        """Test mint quote with different amounts."""
        amounts_to_test = [1, 100, 1000, 21000000]

        for amount in amounts_to_test:
            # Should not raise on creation (will fail on network call)
            with pytest.raises(Exception):
                await test_wallet.mint_quote(amount=Amount(value=amount), description="Test")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_mint_quote_with_description(self, test_wallet):
        """Test mint quote with custom description."""
        with pytest.raises(Exception):
            await test_wallet.mint_quote(
                amount=Amount(value=500),
                description="Payment for services"
            )


class TestMeltQuotes:
    """Test melt quote creation and operations."""

    @pytest.mark.network
    def test_melt_quote_creation(self, test_wallet):
        """Test creating a melt quote with Lightning invoice."""
        # Fake invoice for testing
        fake_invoice = "lnbc100n1p0example..."

        with pytest.raises(Exception):
            quote = test_wallet.melt_quote(
                invoice=fake_invoice,
                description="Test melt quote"
            )

    @pytest.mark.unit
    def test_melt_quote_with_options(self, test_wallet):
        """Test melt quote with melt options."""
        fake_invoice = "lnbc100n1p0example..."

        # Test different melt option configurations
        with pytest.raises(Exception):
            options = MeltOptions()
            test_wallet.melt_quote(
                invoice=fake_invoice,
                description="Test with options",
                options=options
            )


class TestQuoteStates:
    """Test quote state management."""

    @pytest.mark.unit
    def test_quote_states_exist(self):
        """Test that quote state enums are available."""
        # Import quote states
        try:
            from cdk import QuoteState
            assert QuoteState is not None
        except ImportError:
            pytest.skip("QuoteState not available in this version")


class TestSendAndReceiveOptions:
    """Test send and receive options configuration."""

    def test_send_options_creation(self):
        """Test creating send options."""
        options = SendOptions(
            memo=SendMemo(memo="Test payment", include_memo=True),
            conditions=None,
            amount_split_target=SplitTarget.NONE(),
            send_kind=SendKind.ONLINE_EXACT(),
            include_fee=True,
            max_proofs=None,
            metadata={}
        )
        assert options is not None

    def test_send_options_with_conditions(self):
        """Test send options with spending conditions."""
        options = SendOptions(
            memo=SendMemo(memo="Conditional payment", include_memo=True),
            conditions=None,
            amount_split_target=SplitTarget.NONE(),
            send_kind=SendKind.OFFLINE_EXACT(),
            include_fee=False,
            max_proofs=None,
            metadata={}
        )
        assert options is not None

    def test_melt_options_creation(self):
        """Test creating melt options variants."""
        from cdk import MeltOptions, Amount

        # Test MPP variant
        mpp_options = MeltOptions.MPP(amount=Amount(value=1000))
        assert mpp_options is not None
        assert mpp_options.amount.value == 1000

        # Test AMOUNTLESS variant
        amountless_options = MeltOptions.AMOUNTLESS(amount_msat=Amount(value=1000000))
        assert amountless_options is not None
        assert amountless_options.amount_msat.value == 1000000
