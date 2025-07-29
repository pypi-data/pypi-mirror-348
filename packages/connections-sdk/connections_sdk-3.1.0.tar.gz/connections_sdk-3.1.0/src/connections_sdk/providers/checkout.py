from typing import Dict, Any, Tuple, Optional, Union, cast
from datetime import datetime, timezone
from deepmerge import always_merger
import requests
import os
import json
from json.decoder import JSONDecodeError
from requests.structures import CaseInsensitiveDict
from ..models import (
    TransactionRequest,
    Amount,
    Source,
    SourceType,
    Customer,
    Address,
    StatementDescription,
    ThreeDS,
    RecurringType,
    TransactionStatusCode,
    ErrorType,
    ErrorCategory,
    RefundRequest,
    RefundResponse,
    TransactionStatus,
    ErrorResponse,
    ErrorCode,
    TransactionResponse,
    TransactionSource,
    ProvisionedSource,
    ResponseCode
)
from connections_sdk.exceptions import TransactionError
from ..utils.model_utils import create_transaction_request, validate_required_fields, _basis_theory_extras
from ..utils.request_client import RequestClient


RECURRING_TYPE_MAPPING = {
    RecurringType.ONE_TIME: "Regular",
    RecurringType.CARD_ON_FILE: "CardOnFile",
    RecurringType.SUBSCRIPTION: "Recurring",
    RecurringType.UNSCHEDULED: "Unscheduled"
}

# Map Checkout.com status to our status codes
STATUS_CODE_MAPPING = {
    "Authorized": TransactionStatusCode.AUTHORIZED,
    "Pending": TransactionStatusCode.PENDING,
    "Card Verified": TransactionStatusCode.CARD_VERIFIED,
    "Declined": TransactionStatusCode.DECLINED,
    "Retry Scheduled": TransactionStatusCode.RETRY_SCHEDULED
}

# Mapping of Checkout.com error codes to our error types
ERROR_CODE_MAPPING = {
    "card_authorization_failed": ErrorType.REFUSED,
    "card_disabled": ErrorType.BLOCKED_CARD,
    "card_expired": ErrorType.EXPIRED_CARD,
    "card_expiry_month_invalid": ErrorType.INVALID_CARD,
    "card_expiry_month_required": ErrorType.INVALID_CARD,
    "card_expiry_year_invalid": ErrorType.INVALID_CARD,
    "card_expiry_year_required": ErrorType.INVALID_CARD,
    "expiry_date_format_invalid": ErrorType.INVALID_CARD,
    "card_not_found": ErrorType.INVALID_CARD,
    "card_number_invalid": ErrorType.INVALID_CARD,
    "card_number_required": ErrorType.INVALID_CARD,
    "issuer_network_unavailable": ErrorType.OTHER,
    "card_not_eligible_domestic_money_transfer": ErrorType.NOT_SUPPORTED,
    "card_not_eligible_cross_border_money_transfer": ErrorType.NOT_SUPPORTED,
    "card_not_eligible_domestic_non_money_transfer": ErrorType.NOT_SUPPORTED,
    "card_not_eligible_cross_border_non_money_transfer": ErrorType.NOT_SUPPORTED,
    "card_not_eligible_domestic_online_gambling": ErrorType.NOT_SUPPORTED,
    "card_not_eligible_cross_border_online_gambling": ErrorType.NOT_SUPPORTED,
    "3ds_malfunction": ErrorType.AUTHENTICATION_FAILURE,
    "3ds_not_enabled_for_card": ErrorType.AUTHENTICATION_FAILURE,
    "3ds_not_supported": ErrorType.AUTHENTICATION_FAILURE,
    "3ds_not_configured": ErrorType.AUTHENTICATION_FAILURE,
    "3ds_payment_required": ErrorType.AUTHENTICATION_FAILURE,
    "3ds_version_invalid": ErrorType.AUTHENTICATION_FAILURE,
    "3ds_version_not_supported": ErrorType.AUTHENTICATION_FAILURE,
    "amount_exceeds_balance": ErrorType.INSUFFICENT_FUNDS,
    "amount_limit_exceeded": ErrorType.INSUFFICENT_FUNDS,
    "payment_expired": ErrorType.PAYMENT_CANCELLED,
    "cvv_invalid": ErrorType.CVC_INVALID,
    "processing_error": ErrorType.REFUSED,
    "velocity_amount_limit_exceeded": ErrorType.INSUFFICENT_FUNDS,
    "velocity_count_limit_exceeded": ErrorType.INSUFFICENT_FUNDS,
    "address_invalid": ErrorType.AVS_DECLINE,
    "city_invalid": ErrorType.AVS_DECLINE,
    "country_address_invalid": ErrorType.AVS_DECLINE,
    "country_invalid": ErrorType.AVS_DECLINE,
    "country_phone_code_invalid": ErrorType.AVS_DECLINE,
    "country_phone_code_length_invalid": ErrorType.AVS_DECLINE,
    "phone_number_invalid": ErrorType.AVS_DECLINE,
    "phone_number_length_invalid": ErrorType.AVS_DECLINE,
    "zip_invalid": ErrorType.AVS_DECLINE,
    "action_failure_limit_exceeded": ErrorType.PROCESSOR_BLOCKED,
    "token_expired": ErrorType.OTHER,
    "token_in_use": ErrorType.OTHER,
    "token_invalid": ErrorType.OTHER,
    "token_used": ErrorType.OTHER,
    "capture_value_greater_than_authorized": ErrorType.OTHER,
    "capture_value_greater_than_remaining_authorized": ErrorType.OTHER,
    "card_holder_invalid": ErrorType.OTHER,
    "previous_payment_id_invalid": ErrorType.OTHER,
    "processing_channel_id_required": ErrorType.CONFIGURATION_ERROR,
    "success_url_required": ErrorType.CONFIGURATION_ERROR,
    "source_token_invalid": ErrorType.INVALID_SOURCE_TOKEN,
    "aft_processor_not_matched": ErrorType.OTHER,
    "amount_invalid": ErrorType.OTHER,
    "api_calls_quota_exceeded": ErrorType.OTHER,
    "billing_descriptor_city_invalid": ErrorType.OTHER,
    "billing_descriptor_city_required": ErrorType.OTHER,
    "billing_descriptor_name_invalid": ErrorType.OTHER,
    "billing_descriptor_name_required": ErrorType.OTHER,
    "business_invalid": ErrorType.OTHER,
    "business_settings_missing": ErrorType.OTHER,
    "channel_details_invalid": ErrorType.OTHER,
    "channel_url_missing": ErrorType.OTHER,
    "charge_details_invalid": ErrorType.OTHER,
    "currency_invalid": ErrorType.OTHER,
    "currency_required": ErrorType.OTHER,
    "customer_already_exists": ErrorType.OTHER,
    "customer_email_invalid": ErrorType.OTHER,
    "customer_id_invalid": ErrorType.OTHER,
    "customer_not_found": ErrorType.OTHER,
    "customer_number_invalid": ErrorType.OTHER,
    "customer_plan_edit_failed": ErrorType.OTHER,
    "customer_plan_id_invalid": ErrorType.OTHER,
    "email_in_use": ErrorType.OTHER,
    "email_invalid": ErrorType.OTHER,
    "email_required": ErrorType.OTHER,
    "endpoint_invalid": ErrorType.OTHER,
    "fail_url_invalid": ErrorType.OTHER,
    "ip_address_invalid": ErrorType.OTHER,
    "metadata_key_invalid": ErrorType.OTHER,
    "no_authorization_enabled_processors_available": ErrorType.OTHER,
    "parameter_invalid": ErrorType.OTHER,
    "payment_invalid": ErrorType.OTHER,
    "payment_method_not_supported": ErrorType.OTHER,
    "payment_source_required": ErrorType.OTHER,
    "payment_type_invalid": ErrorType.OTHER,
    "processing_key_required": ErrorType.OTHER,
    "processing_value_required": ErrorType.OTHER,
    "recurring_plan_exists": ErrorType.OTHER,
    "recurring_plan_not_exist": ErrorType.OTHER,
    "recurring_plan_removal_failed": ErrorType.OTHER,
    "request_invalid": ErrorType.OTHER,
    "request_json_invalid": ErrorType.OTHER,
    "risk_enabled_required": ErrorType.OTHER,
    "server_api_not_allowed": ErrorType.OTHER,
    "source_email_invalid": ErrorType.OTHER,
    "source_email_required": ErrorType.OTHER,
    "source_id_invalid": ErrorType.OTHER,
    "source_id_or_email_required": ErrorType.OTHER,
    "source_id_required": ErrorType.OTHER,
    "source_id_unknown": ErrorType.OTHER,
    "source_invalid": ErrorType.OTHER,
    "source_or_destination_required": ErrorType.OTHER,
    "source_token_invalid": ErrorType.OTHER,
    "source_token_required": ErrorType.OTHER,
    "source_token_type_required": ErrorType.OTHER,
    "source_token_type_invalid": ErrorType.OTHER,
    "source_type_required": ErrorType.OTHER,
    "sub_entities_count_invalid": ErrorType.OTHER,
    "success_url_invalid": ErrorType.OTHER,
    "token_required": ErrorType.OTHER,
    "token_type_required": ErrorType.OTHER,
    "void_amount_invalid": ErrorType.OTHER,
    "refund_amount_exceeds_balance": ErrorType.REFUND_AMOUNT_EXCEEDS_BALANCE,
    "refund_authorization_declined": ErrorType.REFUND_DECLINED
}

# Mapping of Checkout.com numerical response codes to our error types
CHECKOUT_NUMERICAL_CODE_MAPPING = {
    # 20xxx Series - Generally Soft Declines / Informational
    "20001": ErrorType.REFERRAL,  # Refer to card issuer
    "20002": ErrorType.REFERRAL,  # Refer to card issuer - Special conditions
    "20003": ErrorType.CONFIGURATION_ERROR,  # Invalid merchant or service provider
    "20004": ErrorType.BLOCKED_CARD,  # Card should be captured
    "20005": ErrorType.REFUSED,  # Declined - Do not honour
    "20006": ErrorType.OTHER,  # Error / Invalid request parameters
    "20009": ErrorType.OTHER,  # Request in progress (treating as a final decline state if listed as error)
    "20012": ErrorType.OTHER,  # Invalid transaction
    "20013": ErrorType.INVALID_AMOUNT,  # Invalid value/amount
    "20014": ErrorType.INVALID_CARD,  # Invalid account number (no such number)
    "20015": ErrorType.NOT_SUPPORTED, # Transaction cannot be processed through debit network
    "20016": ErrorType.RESTRICTED_CARD,  # Card not initialised
    "20017": ErrorType.PAYMENT_CANCELLED_BY_CONSUMER,  # Customer cancellation
    "20018": ErrorType.OTHER, # Customer dispute (more of a post-transaction event, but if it's an error code at payment time)
    "20019": ErrorType.PAYMENT_CANCELLED, # Re-enter transaction Transaction has expired
    "20020": ErrorType.OTHER,  # Invalid response
    "20021": ErrorType.OTHER,  # No action taken (unable to back out prior transaction)
    "20022": ErrorType.ACQUIRER_ERROR,  # Suspected malfunction
    "20023": ErrorType.OTHER,  # Unacceptable transaction fee
    "20024": ErrorType.NOT_SUPPORTED, # File update not supported by the receiver
    "20025": ErrorType.OTHER, # Unable to locate record on file Account number is missing from the inquiry
    "20026": ErrorType.OTHER, # Duplicate file update record
    "20027": ErrorType.OTHER, # File update field edit error
    "20028": ErrorType.OTHER, # File is temporarily unavailable
    "20029": ErrorType.OTHER, # File update not successful
    "20030": ErrorType.OTHER,  # Format error
    "20031": ErrorType.NOT_SUPPORTED,  # Bank not supported by Switch
    "20032": ErrorType.OTHER, # Completed partially (typically a success state, but if listed as error)
    "20033": ErrorType.OTHER, # Previous scheme transaction ID invalid
    "20038": ErrorType.PIN_TRIES_EXCEEDED,  # Allowable PIN tries exceeded
    "20039": ErrorType.INVALID_CARD,  # No credit account
    "20040": ErrorType.NOT_SUPPORTED,  # Requested function not supported
    "20042": ErrorType.INVALID_AMOUNT, # No universal value/amount
    "20044": ErrorType.INVALID_CARD, # No investment account
    "20045": ErrorType.NOT_SUPPORTED, # The Issuer does not support fallback transactions of hybrid-card
    "20046": ErrorType.BANK_ERROR,  # Bank decline
    "20051": ErrorType.INSUFFICENT_FUNDS,  # Insufficient funds
    "20052": ErrorType.INVALID_CARD,  # No current (checking) account
    "20053": ErrorType.INVALID_CARD,  # No savings account
    "20054": ErrorType.EXPIRED_CARD,  # Expired card
    "20055": ErrorType.INVALID_PIN,  # Incorrect PIN PIN validation not possible
    "20056": ErrorType.INVALID_CARD,  # No card record
    "20057": ErrorType.NOT_SUPPORTED,  # Transaction not permitted to cardholder
    "20058": ErrorType.NOT_SUPPORTED,  # Transaction not permitted to terminal
    "20059": ErrorType.FRAUD,  # Suspected fraud
    "20060": ErrorType.REFERRAL,  # Card acceptor contact acquirer
    "20061": ErrorType.INSUFFICENT_FUNDS,  # Activity amount limit exceeded
    "20062": ErrorType.RESTRICTED_CARD,  # Restricted card
    "20063": ErrorType.FRAUD,  # Security violation
    "20064": ErrorType.OTHER, # Transaction does not fulfil AML requirement
    "20065": ErrorType.INSUFFICENT_FUNDS,  # Exceeds Withdrawal Frequency Limit
    "20066": ErrorType.REFERRAL,  # Card acceptor call acquirer security
    "20067": ErrorType.BLOCKED_CARD,  # Hard capture - Pick up card at ATM
    "20068": ErrorType.ACQUIRER_ERROR,  # Response received too late / Timeout
    "20072": ErrorType.RESTRICTED_CARD, # Account not yet activated
    "20075": ErrorType.PIN_TRIES_EXCEEDED,  # Allowable PIN-entry tries exceeded
    "20078": ErrorType.BLOCKED_CARD,  # Blocked at first use
    "20081": ErrorType.NOT_SUPPORTED, # Card is local use only
    "20082": ErrorType.CVC_INVALID,  # No security model / Negative CAM, dCVV, iCVV, or CVV results
    "20083": ErrorType.INVALID_CARD, # No accounts
    "20084": ErrorType.OTHER, # No PBF
    "20085": ErrorType.OTHER, # PBF update error
    "20086": ErrorType.ACQUIRER_ERROR,  # ATM malfunction Invalid authorization type
    "20087": ErrorType.INVALID_CARD,  # Bad track data (invalid CVV and/or expiry date)
    "20088": ErrorType.OTHER, # Unable to dispense/process
    "20089": ErrorType.OTHER, # Administration error
    "20090": ErrorType.ACQUIRER_ERROR,  # Cut-off in progress
    "20091": ErrorType.BANK_ERROR,  # Issuer unavailable or switch is inoperative
    "20092": ErrorType.ACQUIRER_ERROR,  # Destination cannot be found for routing
    "20093": ErrorType.NOT_SUPPORTED,  # Transaction cannot be completed; violation of law
    "20094": ErrorType.OTHER,  # Duplicate transmission / invoice
    "20095": ErrorType.OTHER,  # Reconcile error
    "20096": ErrorType.ACQUIRER_ERROR,  # System malfunction
    "20097": ErrorType.OTHER, # Reconciliation totals reset
    "20098": ErrorType.OTHER, # MAC error
    "20099": ErrorType.OTHER,  # Other / Unidentified responses
    "20197": ErrorType.OTHER,  # Catch-all for many sub-errors like CVV2 failure, transaction not supported. Mapping to OTHER due to its composite nature.
    "20100": ErrorType.INVALID_CARD,  # Invalid expiry date format
    "20101": ErrorType.INVALID_SOURCE_TOKEN, # No Account / No Customer (Token is incorrect or invalid)
    "20102": ErrorType.CONFIGURATION_ERROR,  # Invalid merchant / wallet ID
    "20103": ErrorType.NOT_SUPPORTED,  # Card type / payment method not supported
    "20104": ErrorType.OTHER,  # Gateway reject - Invalid transaction
    "20105": ErrorType.OTHER,  # Gateway reject - Violation
    "20106": ErrorType.NOT_SUPPORTED,  # Unsupported currency
    "20107": ErrorType.OTHER,  # Billing address is missing (Could be AVS_DECLINE if validation fails, but often a data validation before submission)
    "20108": ErrorType.REFUSED, # Declined - Updated cardholder available
    "20109": ErrorType.OTHER,  # Transaction already reversed (voided) Capture is larger than initial authorized value
    "20110": ErrorType.OTHER, # Authorization completed (Not an error, but if returned in error context)
    "20111": ErrorType.OTHER,  # Transaction already reversed
    "20112": ErrorType.CONFIGURATION_ERROR,  # Merchant not Mastercard SecureCode enabled
    "20113": ErrorType.OTHER, # Invalid property
    "20114": ErrorType.INVALID_SOURCE_TOKEN,  # Token is incorrect
    "20115": ErrorType.OTHER, # Missing / Invalid lifetime
    "20116": ErrorType.OTHER, # Invalid encoding
    "20117": ErrorType.CONFIGURATION_ERROR,  # Invalid API version
    "20118": ErrorType.OTHER,  # Transaction pending
    "20119": ErrorType.OTHER, # Invalid batch data and/or batch data is missing
    "20120": ErrorType.OTHER, # Invalid customer/user
    "20121": ErrorType.OTHER, # Transaction limit for merchant/terminal exceeded
    "20122": ErrorType.NOT_SUPPORTED, # Mastercard installments not supported
    "20123": ErrorType.OTHER, # Missing basic data: zip, addr, member
    "20124": ErrorType.CVC_INVALID,  # Missing CVV value, required for ecommerce transaction
    "20150": ErrorType.AUTHENTICATION_FAILURE,  # Card not 3D Secure (3DS) enabled
    "20151": ErrorType.AUTHENTICATION_FAILURE,  # Cardholder failed 3DS authentication
    "20152": ErrorType.AUTHENTICATION_FAILURE,  # Initial 3DS transaction not completed within 15 minutes
    "20153": ErrorType.AUTHENTICATION_FAILURE,  # 3DS system malfunction
    "20154": ErrorType.AUTHENTICATION_REQUIRED,  # 3DS authentication required
    "20155": ErrorType.AUTHENTICATION_FAILURE, # 3DS authentication service provided invalid authentication result
    "20156": ErrorType.NOT_SUPPORTED, # Requested function not supported by the acquirer
    "20157": ErrorType.CONFIGURATION_ERROR, # Invalid merchant configurations - Contact Support
    "20158": ErrorType.OTHER, # Refund validity period has expired
    "20159": ErrorType.AUTHENTICATION_FAILURE, # ACS Malfunction
    "20179": ErrorType.INVALID_CARD, # Lifecycle (Occurs when transaction has invalid card data)
    "20182": ErrorType.NOT_SUPPORTED, # Policy (Occurs when a transaction does not comply with card policy)
    "20183": ErrorType.FRAUD, # Security (Occurs when a transaction is suspected to be fraudulent)
    "20193": ErrorType.OTHER, # Invalid country code

    # 30xxx Series - Hard Declines
    "30004": ErrorType.BLOCKED_CARD,  # Pick up card (No fraud)
    "30007": ErrorType.BLOCKED_CARD,  # Pick up card - Special conditions
    "30015": ErrorType.INVALID_CARD,  # No such issuer
    "30016": ErrorType.NOT_SUPPORTED, # Issuer does not allow online gambling payout
    "30017": ErrorType.NOT_SUPPORTED,  # Issuer does not allow original credit transaction
    "30018": ErrorType.NOT_SUPPORTED, # Issuer does not allow money transfer payout
    "30019": ErrorType.NOT_SUPPORTED, # Issuer does not allow non-money transfer payout
    "30020": ErrorType.INVALID_AMOUNT,  # Invalid amount
    "30021": ErrorType.INSUFFICENT_FUNDS,  # Total amount limit reached
    "30022": ErrorType.OTHER,  # Total transaction count limit reached
    "30033": ErrorType.EXPIRED_CARD,  # Expired card - Pick up
    "30034": ErrorType.FRAUD,  # Suspected fraud - Pick up
    "30035": ErrorType.REFERRAL,  # Contact acquirer - Pick up
    "30036": ErrorType.RESTRICTED_CARD,  # Restricted card - Pick up
    "30037": ErrorType.REFERRAL,  # Call acquirer security - Pick up
    "30038": ErrorType.PIN_TRIES_EXCEEDED,  # Allowable PIN tries exceeded - Pick up
    "30041": ErrorType.BLOCKED_CARD,  # Lost card - Pick up
    "30043": ErrorType.FRAUD,  # Stolen card - Pick up
    "30044": ErrorType.NOT_SUPPORTED, # Transaction rejected - AMLD5
    "30045": ErrorType.NOT_SUPPORTED, # Invalid payout fund transfer type
    "30046": ErrorType.INVALID_CARD,  # Closed account

    # 4xxxx Series - Risk Responses
    "40101": ErrorType.FRAUD,  # Risk blocked transaction
    "40201": ErrorType.FRAUD,  # Gateway reject - card number blocklist
    "40202": ErrorType.FRAUD,  # Gateway reject - IP address blocklist
    "40203": ErrorType.FRAUD,  # Gateway reject - email blocklist
    "40204": ErrorType.FRAUD,  # Gateway reject - phone number blocklist
    "40205": ErrorType.FRAUD,  # Gateway Reject - BIN number blocklist
    "41101": ErrorType.FRAUD,  # Risk Blocked Transaction (Client-level rule)
    "41201": ErrorType.FRAUD,  # Decline list - Card number (Client-level)
    "41202": ErrorType.FRAUD,  # Decline list - BIN (Client-level)
    "41203": ErrorType.FRAUD,  # Decline list - Email address (Client-level)
    "41204": ErrorType.FRAUD,  # Decline list - Phone (Client-level)
    "41205": ErrorType.FRAUD,  # Decline list - Payment IP (Client-level) - using client as first seen
    "41206": ErrorType.FRAUD,  # Decline list - Email domain (Client-level)
    "41301": ErrorType.FRAUD,  # Fraud score exceeds threshold (Client-level)
    "42101": ErrorType.FRAUD,  # Risk Blocked Transaction (Entity-level rule)
    "42201": ErrorType.FRAUD,  # Decline list - Card number (Client-level)
    "42202": ErrorType.FRAUD,  # Decline list - BIN (Client-level)
    "42203": ErrorType.FRAUD,  # Decline list - Email address (Client-level)
    "42204": ErrorType.FRAUD,  # Decline list - Phone (Client-level)
    "42206": ErrorType.FRAUD,  # Decline list - Email domain (Client-level)
    "42301": ErrorType.FRAUD,  # Fraud score exceeds threshold
    "43101": ErrorType.FRAUD,  # Potential fraud risk
    "43102": ErrorType.FRAUD,  # Risk blocked transaction – {Rule group name} (Checkout.com-level)
    "43201": ErrorType.FRAUD,  # Decline list - Card number (Checkout.com-level)
    "43202": ErrorType.FRAUD,  # Decline list - BIN (Checkout.com-level)
    "43203": ErrorType.FRAUD,  # Decline list - Email address (Checkout.com-level)
    "43204": ErrorType.FRAUD,  # Decline list - Phone (Checkout.com-level)
    "43205": ErrorType.FRAUD,  # Decline list - Payment IP (Checkout.com-level)
    "43206": ErrorType.FRAUD,  # Decline list - Email domain (Checkout.com-level)
    "43301": ErrorType.FRAUD,  # Fraud score exceeds threshold (Checkout.com-level)
    "44301": ErrorType.AUTHENTICATION_REQUIRED,  # 3DS authentication required
}


class CheckoutClient:
    def __init__(self, private_key: str, processing_channel: str, is_test: bool, bt_api_key: str):
        self.api_key = private_key
        self.processing_channel = processing_channel
        self.base_url = "https://api.sandbox.checkout.com" if is_test else "https://api.checkout.com"
        self.request_client = RequestClient(bt_api_key)

    def _get_status_code(self, checkout_status: Optional[str]) -> TransactionStatusCode:
        """Map Checkout.com status to our status code."""
        if not checkout_status:
            return TransactionStatusCode.DECLINED
        return STATUS_CODE_MAPPING.get(checkout_status, TransactionStatusCode.DECLINED)

    def _transform_to_checkout_payload(self, request: TransactionRequest) -> Dict[str, Any]:
        """Transform SDK request to Checkout.com payload format."""
        
        payload: Dict[str, Any] = { 
            "amount": request.amount.value,
            "currency": request.amount.currency,
            "merchant_initiated": request.merchant_initiated,
            "processing_channel_id": self.processing_channel,
            "reference": request.reference
        }

        if request.metadata:
            payload["metadata"] = request.metadata

        if request.type:
            payload["payment_type"] = RECURRING_TYPE_MAPPING.get(request.type)

        if request. previous_network_transaction_id:
            payload["previous_payment_id"] = request. previous_network_transaction_id
        # Process source based on type
        if request.source.type == SourceType.PROCESSOR_TOKEN:
            payload["source"] = {
                "type": "id",
                "id": request.source.id
            }
        elif request.source.type in [SourceType.BASIS_THEORY_TOKEN, SourceType.BASIS_THEORY_TOKEN_INTENT]:
            # Add card data with Basis Theory expressions
            token_prefix = "token_intent" if request.source.type == SourceType.BASIS_THEORY_TOKEN_INTENT else "token"
            source_data: Dict[str, Any] = {
                "type": "card",
                "number": f"{{{{ {token_prefix}: {request.source.id} | json: '$.data.number'}}}}",
                "expiry_month": f"{{{{ {token_prefix}: {request.source.id} | json: '$.data.expiration_month'}}}}",
                "expiry_year": f"{{{{ {token_prefix}: {request.source.id} | json: '$.data.expiration_year'}}}}",
                "cvv": f"{{{{ {token_prefix}: {request.source.id} | json: '$.data.cvc'}}}}",
                "store_for_future_use": request.source.store_with_provider
            }
            payload["source"] = source_data

        # Add customer information if provided
        if request.customer:
            customer_data: Dict[str, Any] = {}
            if request.customer.first_name or request.customer.last_name:
                name_parts = []
                if request.customer.first_name:
                    name_parts.append(request.customer.first_name)
                if request.customer.last_name:
                    name_parts.append(request.customer.last_name)
                customer_data["name"] = " ".join(name_parts)

            if request.customer.email:
                customer_data["email"] = request.customer.email
            
            payload["customer"] = customer_data

            # Add billing address if provided
            if request.customer.address and "source" in payload:
                billing_address: Dict[str, str] = {}
                if request.customer.address.address_line1:
                    billing_address["address_line1"] = request.customer.address.address_line1
                if request.customer.address.address_line2:
                    billing_address["address_line2"] = request.customer.address.address_line2
                if request.customer.address.city:
                    billing_address["city"] = request.customer.address.city
                if request.customer.address.state:
                    billing_address["state"] = request.customer.address.state
                if request.customer.address.zip:
                    billing_address["zip"] = request.customer.address.zip
                if request.customer.address.country:
                    billing_address["country"] = request.customer.address.country
                
                source = cast(Dict[str, Any], payload["source"])
                source["billing_address"] = billing_address

        # Add statement descriptor if provided
        if request.statement_description and "source" in payload:
            source = cast(Dict[str, Any], payload["source"])
            billing_descriptor: Dict[str, str] = {}
            if request.statement_description.name:
                billing_descriptor["name"] = request.statement_description.name
            if request.statement_description.city:
                billing_descriptor["city"] = request.statement_description.city
            source["billing_descriptor"] = billing_descriptor

        # Add 3DS information if provided
        if request.three_ds:
            three_ds_data: Dict[str, Any] = {
                "enabled": True
            }

            if request.three_ds.authentication_value:
                three_ds_data["cryptogram"] = request.three_ds.authentication_value
            if request.three_ds.eci:
                three_ds_data["eci"] = request.three_ds.eci
            if request.three_ds.threeds_version or request.three_ds.version: # threeds_version from API, fallback to version
                three_ds_data["version"] = request.three_ds.threeds_version or request.three_ds.version
            if request.three_ds.ds_transaction_id: # ds_transaction_id in BT, xid in Checkout
                three_ds_data["xid"] = request.three_ds.ds_transaction_id
            if request.three_ds.authentication_status_code:
                three_ds_data["status"] = request.three_ds.authentication_status_code
            if request.three_ds.authentication_status_reason_code:
                three_ds_data["status_reason_code"] = request.three_ds.authentication_status_reason_code
            
            if request.three_ds.challenge_preference_code:
                challenge_indicator_mapping = {
                    "no-preference": "no_preference",
                    "no-challenge": "no_challenge_requested",
                    "challenge-requested": "challenge_requested",
                    "challenge-mandated": "challenge_requested_mandate"
                }
                checkout_challenge_indicator = challenge_indicator_mapping.get(request.three_ds.challenge_preference_code)
                if checkout_challenge_indicator: # Only add if a valid mapping exists
                    three_ds_data["challenge_indicator"] = checkout_challenge_indicator

            payload["3ds"] = three_ds_data

        # Override/merge any provider properties if specified
        if request.override_provider_properties:
            payload = always_merger.merge(payload, request.override_provider_properties)

        return payload

    def _transform_checkout_response(self, response_data: Dict[str, Any], request: TransactionRequest, headers: CaseInsensitiveDict, error_data: Optional[Dict[str, Any]] = None) -> TransactionResponse:
        """Transform Checkout.com response to our standardized format."""
        response_code = ResponseCode(
            category=CHECKOUT_NUMERICAL_CODE_MAPPING.get(str(response_data.get("response_code")), ErrorType.OTHER).category,
            code=CHECKOUT_NUMERICAL_CODE_MAPPING.get(str(response_data.get("response_code")), ErrorType.OTHER).code
        )

        if error_data and isinstance(error_data, dict):
            error_codes = error_data.get("error_codes", [])
            if error_codes and len(error_codes) > 0:
                first_error = str(error_codes[0])
                response_code = ResponseCode(
                    category=ERROR_CODE_MAPPING.get(first_error, ErrorType.OTHER).category,
                    code=ERROR_CODE_MAPPING.get(first_error, ErrorType.OTHER).code
                )

        return TransactionResponse(
            id=str(response_data.get("id")),
            reference=str(response_data.get("reference")),
            amount=Amount(
                value=int(str(response_data.get("amount", request.amount.value))),
                currency=str(response_data.get("currency", request.amount.currency))
            ),
            status=TransactionStatus(
                code=self._get_status_code(response_data.get("status", TransactionStatusCode.DECLINED)),
                provider_code=str(response_data.get("status", ""))
            ),
            response_code=response_code,
            source=TransactionSource(
                type=request.source.type,
                id=request.source.id,
                provisioned=ProvisionedSource(
                    id=str(response_data.get("source", {}).get("id"))
                ) if response_data.get("source", {}).get("id") else None
            ),
            full_provider_response=response_data,
            basis_theory_extras=_basis_theory_extras(headers),
            created_at=datetime.fromisoformat(response_data["processed_on"].split(".")[0] + "+00:00") if response_data.get("processed_on") else datetime.now(timezone.utc),
            network_transaction_id=response_data.get("scheme_id")
        )

    def _get_error_code(self, error: ErrorType) -> Dict[str, Any]:
        return {
            "category": error.category,
            "code": error.code
        }

    def _get_error_code_object(self, error: ErrorType) -> ErrorCode:
        return ErrorCode(
            category=error.category,
            code=error.code
        )

    def _transform_error_response_object(self, response, error_data=None, headers=None) -> ErrorResponse:
        """Transform error response from Checkout.com to SDK format."""
        error_codes = []
        provider_errors = error_data.get('error_codes', []) if error_data else []
        
        if response.status_code == 401:
            error_codes.append(self._get_error_code_object(ErrorType.INVALID_API_KEY))
        elif response.status_code == 403:
            error_codes.append(self._get_error_code_object(ErrorType.UNAUTHORIZED))
        elif response.status_code == 404:
            error_codes.append(self._get_error_code_object(ErrorType.REFUND_FAILED))
        elif error_data is not None:
            for error_code in error_data.get('error_codes', []):
                mapped_error = ERROR_CODE_MAPPING.get(error_code, ErrorType.OTHER)
                error_codes.append(self._get_error_code_object(mapped_error))

            if not error_codes:
                error_codes.append(self._get_error_code_object(ErrorType.OTHER))
        else:
            error_codes.append(self._get_error_code_object(ErrorType.OTHER))
        
        return ErrorResponse(
            error_codes=error_codes,
            provider_errors=provider_errors,
            basis_theory_extras=_basis_theory_extras(headers),
            full_provider_response=error_data
        )


    def create_transaction(self, request_data: TransactionRequest) -> TransactionResponse:
        """Process a payment transaction through Checkout.com's API directly or via Basis Theory's proxy."""
        validate_required_fields(request_data)
        # Transform request to Checkout.com format
        payload = self._transform_to_checkout_payload(request_data)

        # Set up common headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            # Make request to Checkout.com
            response = self.request_client.request(
                url=f"{self.base_url}/payments",
                method="POST",
                headers=headers,
                data=payload,
                use_bt_proxy=request_data.source.type != SourceType.PROCESSOR_TOKEN
            )

            response_data = response.json()
            
            print(f"Response data: {response_data}")
            
        except requests.exceptions.HTTPError as e:
            # Check if this is a BT error
            if hasattr(e, 'bt_error_response'):
                return e.bt_error_response
            
            try:
                error_data = e.response.json()

                if "card_expired" in error_data.get("error_codes", []) or "card_disabled" in error_data.get("error_codes", []):
                    return self._transform_checkout_response(error_data, request_data, e.response.headers, error_data)
            except:
                error_data = None

            raise TransactionError(self._transform_error_response_object(e.response, error_data, e.response.headers))

        # Transform response to SDK format
        return self._transform_checkout_response(response.json(), request_data, response.headers)

    def refund_transaction(self, refund_request: RefundRequest) -> RefundResponse:
        """
        Refund a payment transaction through Checkout.com's API.
        
        Args:
            refund_request (RefundRequest)
        Returns:
            Union[RefundResponse, ErrorResponse]: The refund response or error response
        """
        # Set up headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Prepare the refund payload
        payload = {
            "reference": refund_request.reference,
            "amount": refund_request.amount.value,
            "currency": refund_request.amount.currency
        }

        try:
            # Make request to Checkout.com
            response = self.request_client.request(
                url=f"{self.base_url}/payments/{refund_request.original_transaction_id}/refunds",
                method="POST",
                headers=headers,
                data=payload,
                use_bt_proxy=False  # Refunds don't need BT proxy
            )

            response_data = response.json()

            # Transform the response to a standardized format
            return RefundResponse(
                id=response_data.get('action_id'),
                reference=response_data.get('reference'),
                amount=Amount(value=response_data.get('amount'), currency=response_data.get('currency')),
                status=TransactionStatus(code=TransactionStatusCode.RECEIVED, provider_code=""),
                full_provider_response=response_data,
                created_at=datetime.now(timezone.utc),
                refunded_transaction_id=refund_request.original_transaction_id
            )

        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
            except:
                error_data = None

            raise TransactionError(self._transform_error_response_object(e.response, error_data, e.response.headers))
