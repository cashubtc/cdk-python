#!/usr/bin/env python3
"""
Example usage of CDK Python bindings.

This example demonstrates basic wallet operations.
Note: This example uses a fake mint URL and will fail on network operations.
For a real example, use an actual Cashu mint URL.
"""

import asyncio
from cdk import Wallet, WalletConfig, WalletDbBackend, create_wallet_db, CurrencyUnit


async def main():
    print("CDK Python Example")
    print("=" * 50)

    # Create an in-memory database
    print("\n1. Creating in-memory database...")
    backend = WalletDbBackend.SQLITE(path=":memory:")
    database = create_wallet_db(backend)
    print("   ✓ Database created")

    # Configure wallet
    print("\n2. Configuring wallet...")
    config = WalletConfig(target_proof_count=3)
    print(f"   ✓ Config created with target_proof_count=3")

    # Create wallet
    print("\n3. Creating wallet...")
    wallet = Wallet(
        mint_url="https://mint.example.com",
        unit=CurrencyUnit.SAT(),
        mnemonic="abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
        db=database,
        config=config
    )
    print("   ✓ Wallet created")
    print("   ✓ Mint URL: https://mint.example.com")
    print("   ✓ Unit: SAT")

    # Check balance (async operations)
    print("\n4. Checking balance...")
    balance = await wallet.total_balance()
    pending = await wallet.total_pending_balance()
    reserved = await wallet.total_reserved_balance()
    print(f"   ✓ Total balance: {balance.value} sats")
    print(f"   ✓ Pending balance: {pending.value} sats")
    print(f"   ✓ Reserved balance: {reserved.value} sats")

    # Note: Network operations would fail with fake mint
    print("\n5. Network operations...")
    print("   (Skipped - using fake mint URL)")
    print("   To perform real operations, use an actual mint URL")

    print("\n" + "=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease run 'just generate' to build the bindings first.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
