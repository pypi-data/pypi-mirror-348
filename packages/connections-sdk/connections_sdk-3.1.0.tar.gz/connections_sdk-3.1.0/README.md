# Connections SDK

The Connections SDK simplifies payment processing by providing a unified interface to multiple payment providers. It uses Basis Theory for secure card tokenization and supports multiple payment processors.

## Features

- Unified payment processing interface
- Support for multiple payment providers
- Support for one-time payments and card-on-file transactions
- 3DS authentication support
- Comprehensive error handling and categorization
- [Providers](./docs/providers/index.md) documentation for each provider supported by the SDK.

## Installation

```bash
pip install connections_sdk
```

## Quick Start

```python
from connections_sdk import Connections
from connections_sdk.models import RecurringType

# Initialize the SDK with your chosen provider
sdk = Connections({
    'is_test': True,  # Use test environment
    'bt_api_key': 'YOUR_BASIS_THEORY_API_KEY',
    'provider_config': {
        # Configure your chosen provider
        'adyen': {
            'apiKey': 'YOUR_PROVIDER_API_KEY',
            'merchantAccount': 'YOUR_MERCHANT_ACCOUNT',
        }
    }
})

# Create a transaction request
transaction_request = TransactionRequest(
    reference='unique-transaction-reference',
    type=RecurringType.ONE_TIME,
    amount=Amount(
        value=1000,  # Amount in cents
        currency='USD'
    ),
    source=Source(
        type=SourceType.BASIS_THEORY_TOKEN,
        id='YOUR_BASIS_THEORY_TOKEN_ID',
        store_with_provider=False
    ),
    customer=Customer(
        reference='customer-reference'
    )
)

# Process the transaction with your chosen provider
response = sdk.adyen.create_transaction(transaction_request)  # Use sdk.<provider>.transaction()
```

## Documentation

- [Getting Started](./docs/getting-started.md)
- [Authentication](./docs/authentication.md)
- [Processing Payments](./docs/processing-payments.md)
- [Error Handling](./docs/error-handling.md)
- [API Reference](./docs/api-reference.md)
- [Providers](./docs/providers/index.md)

## Support

For support, please contact [support@basistheory.com](mailto:support@basistheory.com) or open an issue on GitHub. 