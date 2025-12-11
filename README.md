# CDK Python

Python language bindings for the [Cashu Development Kit (CDK)](https://github.com/cashubtc/cdk).

## About

CDK Python provides UniFFI-generated Python bindings for the Cashu Development Kit, enabling developers to build Cashu ecash applications in Python with full access to CDK's wallet functionality.

## Features

- **Complete Wallet Operations**: Create, configure, and manage Cashu wallets
- **Mint & Melt**: Request quotes and perform minting and melting operations
- **Token Management**: Send and receive Cashu tokens
- **Proof Handling**: Track proof states and manage transactions
- **Multiple Backends**: Support for SQLite, PostgreSQL, and in-memory databases
- **BIP39 Support**: Mnemonic generation and management
- **Authentication**: CAT tokens and refresh token support
- **Subscriptions**: Real-time updates via NUT-17

## Installation

```bash
pip install cdk-python
```

### Requirements

- Python 3.10 or higher
- Supported platforms:
  - Linux (x86_64, ARM64)
  - macOS (Apple Silicon, Intel)
  - Windows (x86_64)

## Quick Start

```python
from cdk import Wallet, WalletConfig, Database, CurrencyUnit
import asyncio

async def main():
    # Create an in-memory database for testing
    database = Database.memory()

    config = WalletConfig(
        target_proof_count= None
    )

    # Create wallet
    wallet = Wallet(
        "https://mint.example.com",
        CurrencyUnit.SAT(),
        "slot destroy disagree air autumn cigar fade hat black cherry repair scrub",
        database,
        config,
    )


    # Get mint information
    mint_info = await wallet.get_mint_info()
    print(f"Mint: {mint_info.name}")

    # Request a mint quote
    quote = await wallet.mint_quote(amount=100, description="Test deposit")
    print(f"Pay this invoice: {quote.request}")

    # Check balance
    balance = await wallet.total_balance()
    print(f"Balance: {balance} sats")


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
```

## Examples

### Creating a Wallet with SQLite

```python
from cdk import Wallet, WalletConfig, Database, CurrencyUnit

# Create SQLite database
database = await Database.sqlite("/path/to/wallet.db")

# Create wallet configuration
config = WalletConfig(
    target_proof_count=3  # Optional: target number of proofs
)

# Initialize wallet
wallet = Wallet(
	"https://mint.example.com",
	CurrencyUnit.SAT(),
	"slot destroy disagree air autumn cigar fade hat black cherry repair scrub",
	database,
	config,
)
```

### Sending and Receiving Tokens

```python
from cdk import SendOptions, ReceiveOptions


# Send tokens
send_opts = SendOptions(
    memo="Payment for coffee",
    include_fees=True
)
token = await wallet.send(amount=50, send_options=send_opts)
print(f"Token: {token}")

# Receive tokens
receive_opts = ReceiveOptions(
    signature_flag="all"  # Verify all proofs
)
amount_received = await wallet.receive(token, receive_opts)
print(f"Received: {amount_received} sats")
```

### Melt Quote (Lightning Payment)

```python
# Create melt quote for Lightning payment
melt_quote = await wallet.melt_quote(
    invoice="lnbc...",  # Lightning invoice
    description="Outgoing payment"
)

# Execute the melt
result = await wallet.melt(melt_quote.quote_id)
print(f"Payment preimage: {result.preimage}")
```

### Generating Mnemonics

```python
from cdk import Mnemonic

# Generate new mnemonic
mnemonic = Mnemonic.generate(word_count=12)
print(f"Mnemonic: {mnemonic.phrase()}")

# Restore from existing mnemonic
existing = Mnemonic.from_string("word1 word2 ... word12")
seed = existing.to_seed(passphrase="")  # Optional passphrase
```

### Transaction History

```python
from cdk import TransactionDirection

# List all transactions
transactions = await wallet.list_transactions()
for tx in transactions:
    print(f"Amount: {tx.amount}, Date: {tx.created_at}")

# Filter by direction
sent = wallet.list_transactions(direction=TransactionDirection.OUTGOING)
received = wallet.list_transactions(direction=TransactionDirection.INCOMING)

# Get specific transaction
tx = wallet.get_transaction(transaction_id)
```

### Proof State Management

```python
from cdk import ProofState

# Get proofs by state
pending = await wallet.get_proofs_by_state([ProofState.PENDING])
spent = await wallet.get_proofs_by_state([ProofState.SPENT])

# Check reserved balance
reserved = await wallet.reserved_balance()
print(f"Reserved: {reserved} sats")
```

## PostgreSQL Support

CDK Python includes PostgreSQL database support for production deployments:

```python
from cdk import Database

# Create PostgreSQL database connection
database = Database.postgres(
    connection_string="postgresql://user:pass@localhost/cdk_wallet"
)

wallet = Wallet(
	"https://mint.example.com",
	CurrencyUnit.SAT(),
	"slot destroy disagree air autumn cigar fade hat black cherry repair scrub",
	database,
	config,
)
```

## Development

### Building from Source

Requirements:
- Rust 1.85.0 or higher
- Python 3.10 or higher
- just (command runner)

```bash
# Clone the repository
git clone https://github.com/cashubtc/cdk-python.git
cd cdk-python

# Install development dependencies
pip install -r requirements-dev.txt

# Generate bindings for your platform
just generate

# Build the package
just build

# Run tests
just test
```

### Testing the Publishing Workflow

Before publishing to PyPI, test the workflow with TestPyPI:

1. **Set up TestPyPI** (one-time setup)
   - Follow the guide in [TESTPYPI_SETUP.md](TESTPYPI_SETUP.md)
   - Configure GitHub environment and trusted publishing

2. **Run test workflow**
   - Go to Actions → "Test Build and Publish (TestPyPI)" → Run workflow
   - Enter a CDK version tag (e.g., `v0.4.0`)
   - This will build and publish to https://test.pypi.org

3. **Verify the test package**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ cdk-python==0.4.0
   python -c "import cdk; print('Success!')"
   ```

See [TESTING_WORKFLOW.md](TESTING_WORKFLOW.md) for complete testing documentation.

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_wallet.py

# Run with verbose output
pytest -v
```

### Platform-Specific Builds

```bash
# macOS ARM64 (Apple Silicon)
./scripts/generate-macos-arm64.sh

# macOS x86_64 (Intel)
./scripts/generate-macos-x86_64.sh

# Linux x86_64
./scripts/generate-linux-x86_64.sh

# Linux ARM64
./scripts/generate-linux-aarch64.sh

# Windows x86_64
./scripts/generate-windows-x86_64.sh
```

## Project Structure

```
cdk-python/
├── src/
│   └── cdk/           # Python package (generated bindings + native lib)
├── tests/             # Test suite
├── scripts/           # Platform-specific build scripts
├── pyproject.toml     # Package configuration
├── setup.py           # Build configuration
└── justfile           # Development commands
```

## Documentation

- [CDK Documentation](https://docs.cashu.space)
- [Cashu Protocol](https://github.com/cashubtc/nuts)
- [API Reference](https://docs.rs/cdk)

## Related Projects

- [CDK](https://github.com/cashubtc/cdk) - Rust core library
- [CDK Swift](https://github.com/cashubtc/cdk-swift) - Swift bindings
- [CDK Kotlin](https://github.com/cashubtc/cdk-kotlin) - Kotlin bindings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- GitHub Issues: https://github.com/cashubtc/cdk-python/issues
- Discord: https://discord.gg/cashu
- Telegram: https://t.me/CashuBTC

## Acknowledgments

Built with [UniFFI](https://mozilla.github.io/uniffi-rs/) by Mozilla.
