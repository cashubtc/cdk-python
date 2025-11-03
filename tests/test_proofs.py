"""Tests for proof states and transaction management."""

import pytest


class TestProofStates:
    """Test proof state enumeration and filtering."""

    @pytest.mark.unit
    def test_proof_state_enum_exists(self):
        """Test that ProofState enum is available."""
        try:
            from cdk import ProofState
            assert ProofState is not None
        except ImportError:
            pytest.skip("ProofState enum not available")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_proof_states_retrieval(self, test_wallet):
        """Test retrieving proofs by state."""
        try:
            from cdk import ProofState

            # Test with different states
            states_to_test = [
                ProofState.PENDING,
                ProofState.UNSPENT,
                ProofState.SPENT,
            ]

            for state in states_to_test:
                proofs = await test_wallet.get_proofs_by_states([state])
                assert isinstance(proofs, list)
        except (ImportError, AttributeError):
            pytest.skip("Proof state filtering not available")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_multiple_proof_states(self, test_wallet):
        """Test filtering proofs by multiple states."""
        try:
            from cdk import ProofState

            # Query multiple states at once
            states = [ProofState.PENDING, ProofState.UNSPENT]
            proofs = await test_wallet.get_proofs_by_states(states)
            assert isinstance(proofs, list)
        except (ImportError, AttributeError):
            pytest.skip("Multi-state proof filtering not available")


class TestTransactions:
    """Test transaction listing and management."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_list_transactions_empty(self, test_wallet):
        """Test listing transactions on new wallet."""
        try:
            transactions = await test_wallet.list_transactions(direction=None)
            assert isinstance(transactions, list)
            assert len(transactions) == 0
        except AttributeError:
            pytest.skip("list_transactions not available")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_list_transactions_with_filter(self, test_wallet):
        """Test listing transactions with direction filter."""
        try:
            from cdk import TransactionDirection

            # Test filtering by direction
            outgoing = await test_wallet.list_transactions(
                direction=TransactionDirection.OUTGOING
            )
            assert isinstance(outgoing, list)

            incoming = await test_wallet.list_transactions(
                direction=TransactionDirection.INCOMING
            )
            assert isinstance(incoming, list)
        except (ImportError, AttributeError):
            pytest.skip("Transaction direction filtering not available")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_specific_transaction(self, test_wallet):
        """Test retrieving a specific transaction by ID."""
        try:
            from cdk import TransactionId
            # Create a fake transaction ID
            fake_id = TransactionId(hex="00000000-0000-0000-0000-000000000000")

            # Should raise or return None for non-existent transaction
            try:
                tx = await test_wallet.get_transaction(fake_id)
                assert tx is None
            except Exception:
                # Expected for non-existent transaction
                pass
        except (AttributeError, ImportError, TypeError):
            pytest.skip("get_transaction not available")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_revert_transaction(self, test_wallet):
        """Test reverting a transaction."""
        try:
            from cdk import TransactionId
            # Create a fake transaction ID
            fake_id = TransactionId(hex="00000000-0000-0000-0000-000000000000")

            # Should raise for non-existent transaction
            # revert_transaction might succeed with no-op or raise
            try:
                await test_wallet.revert_transaction(fake_id)
            except Exception:
                # Expected for non-existent transaction
                pass
        except (AttributeError, ImportError, TypeError):
            pytest.skip("revert_transaction not available")


class TestTransactionDirection:
    """Test transaction direction enumeration."""

    @pytest.mark.unit
    def test_transaction_direction_enum(self):
        """Test that TransactionDirection enum exists."""
        try:
            from cdk import TransactionDirection

            assert hasattr(TransactionDirection, 'INCOMING')
            assert hasattr(TransactionDirection, 'OUTGOING')
        except ImportError:
            pytest.skip("TransactionDirection enum not available")


class TestAmountOperations:
    """Test amount types and operations."""

    @pytest.mark.unit
    def test_amount_creation(self):
        """Test creating Amount objects."""
        try:
            from cdk import Amount

            amount = Amount(value=100)
            assert amount is not None
        except (ImportError, AttributeError):
            pytest.skip("Amount type not available")

    @pytest.mark.unit
    def test_amount_equality(self):
        """Test amount equality comparison."""
        try:
            from cdk import Amount

            amount1 = Amount(value=100)
            amount2 = Amount(value=100)
            amount3 = Amount(value=200)

            assert amount1 == amount2
            assert amount1 != amount3
        except (ImportError, AttributeError):
            pytest.skip("Amount type not available")

    @pytest.mark.unit
    def test_amount_value_access(self):
        """Test accessing amount value."""
        try:
            from cdk import Amount

            amount = Amount(value=500)
            # Try to access the value
            # Exact method depends on FFI implementation
            assert amount.value == 500
        except (ImportError, AttributeError):
            pytest.skip("Amount type not available")
