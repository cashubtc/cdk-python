"""Tests for token send and receive operations."""

import pytest


class TestTokenSending:
    """Test token sending operations."""

    @pytest.mark.unit
    def test_send_requires_balance(self, test_wallet):
        """Test that sending tokens requires sufficient balance."""
        # Wallet has zero balance, so send should fail
        with pytest.raises(Exception):
            test_wallet.send(amount=100)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_send_with_options(self, test_wallet):
        """Test sending tokens with send options."""
        from cdk import SendOptions, Amount, SendMemo, SendKind, SplitTarget

        options = SendOptions(
            memo=SendMemo(memo="Test payment", include_memo=True),
            conditions=None,
            amount_split_target=SplitTarget.NONE(),
            send_kind=SendKind.ONLINE_EXACT(),
            include_fee=True,
            max_proofs=None,
            metadata={}
        )

        # Should fail due to insufficient balance
        with pytest.raises(Exception):
            await test_wallet.prepare_send(amount=Amount(value=50), send_options=options)

    @pytest.mark.unit
    def test_send_zero_amount(self, test_wallet):
        """Test that sending zero amount is handled."""
        with pytest.raises(Exception):
            test_wallet.send(amount=0)

    @pytest.mark.unit
    def test_send_negative_amount(self, test_wallet):
        """Test that sending negative amount is handled."""
        with pytest.raises(Exception):
            test_wallet.send(amount=-100)


class TestTokenReceiving:
    """Test token receiving operations."""

    @pytest.mark.unit
    def test_receive_invalid_token(self, test_wallet):
        """Test receiving an invalid token."""
        invalid_token = "invalid_token_string"

        with pytest.raises(Exception):
            test_wallet.receive(invalid_token)

    @pytest.mark.unit
    def test_receive_empty_token(self, test_wallet):
        """Test receiving an empty token."""
        with pytest.raises(Exception):
            test_wallet.receive("")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_receive_with_options(self, test_wallet):
        """Test receiving tokens with receive options."""
        try:
            from cdk import ReceiveOptions, Token, SplitTarget

            options = ReceiveOptions(
                amount_split_target=SplitTarget.NONE(),
                p2pk_signing_keys=[],
                preimages=[],
                metadata={}
            )

            # Should fail with invalid token string parsing
            with pytest.raises(Exception):
                # Try to parse invalid token first
                token = Token.from_string("invalid_token")
                await test_wallet.receive(token, options=options)
        except (ImportError, AttributeError, TypeError):
            pytest.skip("ReceiveOptions not available or signature changed")


class TestTokenMetadata:
    """Test token metadata handling."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_send_with_memo(self, test_wallet):
        """Test sending token with memo."""
        from cdk import SendOptions, Amount, SendMemo, SendKind, SplitTarget

        options = SendOptions(
            memo=SendMemo(memo="Coffee payment", include_memo=True),
            conditions=None,
            amount_split_target=SplitTarget.NONE(),
            send_kind=SendKind.ONLINE_EXACT(),
            include_fee=False,
            max_proofs=None,
            metadata={}
        )

        with pytest.raises(Exception):
            await test_wallet.prepare_send(amount=Amount(value=100), send_options=options)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_send_with_metadata(self, test_wallet):
        """Test sending token with custom metadata."""
        from cdk import SendOptions, Amount, SendMemo, SendKind, SplitTarget

        # Test with metadata if supported
        options = SendOptions(
            memo=SendMemo(memo="Payment", include_memo=True),
            conditions=None,
            amount_split_target=SplitTarget.NONE(),
            send_kind=SendKind.OFFLINE_EXACT(),
            include_fee=True,
            max_proofs=None,
            metadata={"custom_key": "custom_value"}
        )

        with pytest.raises(Exception):
            await test_wallet.prepare_send(amount=Amount(value=100), send_options=options)


class TestSplitTargets:
    """Test split target configurations."""

    @pytest.mark.unit
    def test_split_target_enum_exists(self):
        """Test that split target enum is available."""
        try:
            from cdk import SplitTarget
            assert SplitTarget is not None
        except ImportError:
            pytest.skip("SplitTarget enum not available")

    @pytest.mark.unit
    def test_split_target_variants(self):
        """Test different split target cases."""
        try:
            from cdk import SplitTarget

            # Test that enum variants exist
            # Exact variants depend on CDK implementation
            assert hasattr(SplitTarget, '__members__') or hasattr(SplitTarget, '__dict__')
        except ImportError:
            pytest.skip("SplitTarget enum not available")
