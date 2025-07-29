from typing import Optional, Dict, Any, cast
from dataclasses import dataclass
from .providers.adyen import AdyenClient
from .providers.checkout import CheckoutClient
from .exceptions import ConfigurationError


@dataclass
class AdyenConfig:
    api_key: str
    merchant_account: str
    production_prefix: str = ""


@dataclass
class CheckoutConfig:
    private_key: str
    processing_channel: str


@dataclass
class ProviderConfig:
    adyen: Optional[AdyenConfig] = None
    checkout: Optional[CheckoutConfig] = None


class Connections:
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the Connections SDK with the provided configuration."""
        self.is_test: bool = False
        self.bt_api_key: str = ""
        self.provider_config: Optional[ProviderConfig] = None

        if 'is_test' not in config:
            config['is_test'] = False
        if 'bt_api_key' not in config:
            raise ConfigurationError("'bt_api_key' parameter is required")
        if 'provider_config' not in config:
            raise ConfigurationError("'provider_config' parameter is required")

        self.is_test = config['is_test']
        self.bt_api_key = config['bt_api_key']

        provider_config = config['provider_config']
        self.provider_config = ProviderConfig()

        # Initialize Adyen configuration if provided
        if 'adyen' in provider_config:
            adyen_config = provider_config.get('adyen')
            self.provider_config.adyen = AdyenConfig(
                api_key=adyen_config.get('api_key'),
                merchant_account=adyen_config.get('merchant_account'),
                production_prefix=adyen_config.get('production_prefix', "")
            )

        # Initialize Checkout.com configuration if provided
        if 'checkout' in provider_config:
            checkout_config = provider_config.get('checkout')
            self.provider_config.checkout = CheckoutConfig(
                private_key=checkout_config.get('private_key'),
                processing_channel=checkout_config.get('processing_channel')
            )

    @property
    def adyen(self) -> AdyenClient:
        """Get the Adyen client instance."""
        if not self.provider_config or not self.provider_config.adyen:
            raise ConfigurationError("Adyen is not configured")

        return AdyenClient(
            api_key=self.provider_config.adyen.api_key,
            merchant_account=self.provider_config.adyen.merchant_account,
            is_test=self.is_test,
            bt_api_key=self.bt_api_key,
            production_prefix=self.provider_config.adyen.production_prefix
        )

    @property
    def checkout(self) -> CheckoutClient:
        """Get the Checkout client instance."""
        if not self.provider_config or not self.provider_config.checkout:
            raise ConfigurationError("Checkout is not configured")

        return CheckoutClient(
            private_key=self.provider_config.checkout.private_key,
            processing_channel=self.provider_config.checkout.processing_channel,
            is_test=self.is_test,
            bt_api_key=self.bt_api_key
        )