import logging
import json
import asyncio
import time
import os
import uuid  # For X-Request-ID
from typing import Dict, Any, List, Optional, Union, Tuple, Type

# Import HTTP client library (ensure it's installed: pip install httpx)
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    # Define dummy types if library not available, to allow schema definition
    httpx = type('httpx', (object,), {'AsyncClient': type('AsyncClient', (object,), {}), 'RequestError': type('RequestError', (Exception,), {}), 'HTTPStatusError': type('HTTPStatusError', (Exception,), {'request': None, 'response': None})})
    logger = logging.getLogger(__name__) # Define logger if httpx import fails early
    logger.warning("httpx library not found. Please install it using 'pip install httpx'")

# Assuming base_node structure exists
# from .base_node import ( # Use relative import if in a package
from base_node import ( # Use direct import if running as a script/module directly
    BaseNode, NodeSchema, NodeParameter, NodeParameterType,
    NodeValidationError, NodeRegistry
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Fiken Specific Enums ---

class FikenOperation:
    """
    Defines all documented operations for the Fiken API Node (v2).
    Format: ACTION_RESOURCE(_SUBRESOURCE) or VERB_RESOURCE(_SUBRESOURCE)
    """
    # User Info
    GET_USER_INFO = "GET_USER_INFO"

    # Companies
    GET_COMPANIES = "GET_COMPANIES"
    GET_COMPANY = "GET_COMPANY"

    # Accounts
    GET_ACCOUNTS = "GET_ACCOUNTS"
    GET_ACCOUNT = "GET_ACCOUNT"
    GET_ACCOUNT_BALANCES = "GET_ACCOUNT_BALANCES"
    GET_ACCOUNT_BALANCE = "GET_ACCOUNT_BALANCE"

    # Bank Accounts
    GET_BANK_ACCOUNTS = "GET_BANK_ACCOUNTS"
    CREATE_BANK_ACCOUNT = "CREATE_BANK_ACCOUNT"
    GET_BANK_ACCOUNT = "GET_BANK_ACCOUNT"

    # Contacts
    GET_CONTACTS = "GET_CONTACTS"
    CREATE_CONTACT = "CREATE_CONTACT"
    GET_CONTACT = "GET_CONTACT"
    UPDATE_CONTACT = "UPDATE_CONTACT"
    DELETE_CONTACT = "DELETE_CONTACT"
    UPLOAD_CONTACT_ATTACHMENT = "UPLOAD_CONTACT_ATTACHMENT"
    GET_CONTACT_PERSONS = "GET_CONTACT_PERSONS"
    CREATE_CONTACT_PERSON = "CREATE_CONTACT_PERSON"
    GET_CONTACT_PERSON = "GET_CONTACT_PERSON"
    UPDATE_CONTACT_PERSON = "UPDATE_CONTACT_PERSON"
    DELETE_CONTACT_PERSON = "DELETE_CONTACT_PERSON"

    # Groups
    GET_GROUPS = "GET_GROUPS"

    # Products
    CREATE_PRODUCT_SALES_REPORT = "CREATE_PRODUCT_SALES_REPORT"
    GET_PRODUCTS = "GET_PRODUCTS"
    CREATE_PRODUCT = "CREATE_PRODUCT"
    GET_PRODUCT = "GET_PRODUCT"
    UPDATE_PRODUCT = "UPDATE_PRODUCT"
    DELETE_PRODUCT = "DELETE_PRODUCT"

    # Journal Entries
    GET_JOURNAL_ENTRIES = "GET_JOURNAL_ENTRIES"
    CREATE_GENERAL_JOURNAL_ENTRY = "CREATE_GENERAL_JOURNAL_ENTRY"
    GET_JOURNAL_ENTRY = "GET_JOURNAL_ENTRY"
    GET_JOURNAL_ENTRY_ATTACHMENTS = "GET_JOURNAL_ENTRY_ATTACHMENTS"
    UPLOAD_JOURNAL_ENTRY_ATTACHMENT = "UPLOAD_JOURNAL_ENTRY_ATTACHMENT"

    # Transactions
    GET_TRANSACTIONS = "GET_TRANSACTIONS"
    GET_TRANSACTION = "GET_TRANSACTION"

    # Invoices
    GET_INVOICES = "GET_INVOICES"
    CREATE_INVOICE = "CREATE_INVOICE"
    GET_INVOICE = "GET_INVOICE"
    UPDATE_INVOICE = "UPDATE_INVOICE" # PATCH
    GET_INVOICE_ATTACHMENTS = "GET_INVOICE_ATTACHMENTS"
    UPLOAD_INVOICE_ATTACHMENT = "UPLOAD_INVOICE_ATTACHMENT"
    SEND_INVOICE = "SEND_INVOICE"
    GET_INVOICE_COUNTER = "GET_INVOICE_COUNTER"
    SET_INVOICE_COUNTER = "SET_INVOICE_COUNTER"
    GET_INVOICE_DRAFTS = "GET_INVOICE_DRAFTS"
    CREATE_INVOICE_DRAFT = "CREATE_INVOICE_DRAFT"
    GET_INVOICE_DRAFT = "GET_INVOICE_DRAFT"
    UPDATE_INVOICE_DRAFT = "UPDATE_INVOICE_DRAFT"
    DELETE_INVOICE_DRAFT = "DELETE_INVOICE_DRAFT"
    GET_INVOICE_DRAFT_ATTACHMENTS = "GET_INVOICE_DRAFT_ATTACHMENTS"
    UPLOAD_INVOICE_DRAFT_ATTACHMENT = "UPLOAD_INVOICE_DRAFT_ATTACHMENT"
    CREATE_INVOICE_FROM_DRAFT = "CREATE_INVOICE_FROM_DRAFT"

    # Credit Notes
    GET_CREDIT_NOTES = "GET_CREDIT_NOTES"
    CREATE_FULL_CREDIT_NOTE = "CREATE_FULL_CREDIT_NOTE"
    CREATE_PARTIAL_CREDIT_NOTE = "CREATE_PARTIAL_CREDIT_NOTE"
    GET_CREDIT_NOTE = "GET_CREDIT_NOTE"
    SEND_CREDIT_NOTE = "SEND_CREDIT_NOTE"
    GET_CREDIT_NOTE_COUNTER = "GET_CREDIT_NOTE_COUNTER"
    SET_CREDIT_NOTE_COUNTER = "SET_CREDIT_NOTE_COUNTER"
    GET_CREDIT_NOTE_DRAFTS = "GET_CREDIT_NOTE_DRAFTS"
    CREATE_CREDIT_NOTE_DRAFT = "CREATE_CREDIT_NOTE_DRAFT"
    GET_CREDIT_NOTE_DRAFT = "GET_CREDIT_NOTE_DRAFT"
    UPDATE_CREDIT_NOTE_DRAFT = "UPDATE_CREDIT_NOTE_DRAFT"
    DELETE_CREDIT_NOTE_DRAFT = "DELETE_CREDIT_NOTE_DRAFT"
    GET_CREDIT_NOTE_DRAFT_ATTACHMENTS = "GET_CREDIT_NOTE_DRAFT_ATTACHMENTS"
    UPLOAD_CREDIT_NOTE_DRAFT_ATTACHMENT = "UPLOAD_CREDIT_NOTE_DRAFT_ATTACHMENT"
    CREATE_CREDIT_NOTE_FROM_DRAFT = "CREATE_CREDIT_NOTE_FROM_DRAFT"

    # Offers
    GET_OFFERS = "GET_OFFERS"
    GET_OFFER = "GET_OFFER"
    GET_OFFER_COUNTER = "GET_OFFER_COUNTER"
    SET_OFFER_COUNTER = "SET_OFFER_COUNTER"
    GET_OFFER_DRAFTS = "GET_OFFER_DRAFTS"
    CREATE_OFFER_DRAFT = "CREATE_OFFER_DRAFT"
    GET_OFFER_DRAFT = "GET_OFFER_DRAFT"
    UPDATE_OFFER_DRAFT = "UPDATE_OFFER_DRAFT"
    DELETE_OFFER_DRAFT = "DELETE_OFFER_DRAFT"
    GET_OFFER_DRAFT_ATTACHMENTS = "GET_OFFER_DRAFT_ATTACHMENTS"
    UPLOAD_OFFER_DRAFT_ATTACHMENT = "UPLOAD_OFFER_DRAFT_ATTACHMENT"
    CREATE_OFFER_FROM_DRAFT = "CREATE_OFFER_FROM_DRAFT"

    # Order Confirmations
    GET_ORDER_CONFIRMATIONS = "GET_ORDER_CONFIRMATIONS"
    GET_ORDER_CONFIRMATION = "GET_ORDER_CONFIRMATION"
    GET_ORDER_CONFIRMATION_COUNTER = "GET_ORDER_CONFIRMATION_COUNTER"
    SET_ORDER_CONFIRMATION_COUNTER = "SET_ORDER_CONFIRMATION_COUNTER"
    CREATE_INVOICE_DRAFT_FROM_ORDER_CONFIRMATION = "CREATE_INVOICE_DRAFT_FROM_ORDER_CONFIRMATION"
    GET_ORDER_CONFIRMATION_DRAFTS = "GET_ORDER_CONFIRMATION_DRAFTS"
    CREATE_ORDER_CONFIRMATION_DRAFT = "CREATE_ORDER_CONFIRMATION_DRAFT"
    GET_ORDER_CONFIRMATION_DRAFT = "GET_ORDER_CONFIRMATION_DRAFT"
    UPDATE_ORDER_CONFIRMATION_DRAFT = "UPDATE_ORDER_CONFIRMATION_DRAFT"
    DELETE_ORDER_CONFIRMATION_DRAFT = "DELETE_ORDER_CONFIRMATION_DRAFT"
    GET_ORDER_CONFIRMATION_DRAFT_ATTACHMENTS = "GET_ORDER_CONFIRMATION_DRAFT_ATTACHMENTS"
    UPLOAD_ORDER_CONFIRMATION_DRAFT_ATTACHMENT = "UPLOAD_ORDER_CONFIRMATION_DRAFT_ATTACHMENT"
    CREATE_ORDER_CONFIRMATION_FROM_DRAFT = "CREATE_ORDER_CONFIRMATION_FROM_DRAFT"

    # Sales
    GET_SALES = "GET_SALES"
    CREATE_SALE = "CREATE_SALE"
    GET_SALE = "GET_SALE"
    SET_SALE_SETTLED = "SET_SALE_SETTLED" # PATCH
    DELETE_SALE = "DELETE_SALE" # PATCH
    GET_SALE_ATTACHMENTS = "GET_SALE_ATTACHMENTS"
    UPLOAD_SALE_ATTACHMENT = "UPLOAD_SALE_ATTACHMENT"
    GET_SALE_PAYMENTS = "GET_SALE_PAYMENTS"
    CREATE_SALE_PAYMENT = "CREATE_SALE_PAYMENT"
    GET_SALE_PAYMENT = "GET_SALE_PAYMENT"
    GET_SALE_DRAFTS = "GET_SALE_DRAFTS"
    CREATE_SALE_DRAFT = "CREATE_SALE_DRAFT"
    GET_SALE_DRAFT = "GET_SALE_DRAFT"
    UPDATE_SALE_DRAFT = "UPDATE_SALE_DRAFT"
    DELETE_SALE_DRAFT = "DELETE_SALE_DRAFT"
    GET_SALE_DRAFT_ATTACHMENTS = "GET_SALE_DRAFT_ATTACHMENTS"
    UPLOAD_SALE_DRAFT_ATTACHMENT = "UPLOAD_SALE_DRAFT_ATTACHMENT"
    CREATE_SALE_FROM_DRAFT = "CREATE_SALE_FROM_DRAFT"

    # Purchases
    GET_PURCHASES = "GET_PURCHASES"
    CREATE_PURCHASE = "CREATE_PURCHASE"
    GET_PURCHASE = "GET_PURCHASE"
    DELETE_PURCHASE = "DELETE_PURCHASE" # PATCH
    GET_PURCHASE_ATTACHMENTS = "GET_PURCHASE_ATTACHMENTS"
    UPLOAD_PURCHASE_ATTACHMENT = "UPLOAD_PURCHASE_ATTACHMENT"
    GET_PURCHASE_PAYMENTS = "GET_PURCHASE_PAYMENTS"
    CREATE_PURCHASE_PAYMENT = "CREATE_PURCHASE_PAYMENT"
    GET_PURCHASE_PAYMENT = "GET_PURCHASE_PAYMENT"
    GET_PURCHASE_DRAFTS = "GET_PURCHASE_DRAFTS"
    CREATE_PURCHASE_DRAFT = "CREATE_PURCHASE_DRAFT"
    GET_PURCHASE_DRAFT = "GET_PURCHASE_DRAFT"
    UPDATE_PURCHASE_DRAFT = "UPDATE_PURCHASE_DRAFT"
    DELETE_PURCHASE_DRAFT = "DELETE_PURCHASE_DRAFT"
    GET_PURCHASE_DRAFT_ATTACHMENTS = "GET_PURCHASE_DRAFT_ATTACHMENTS"
    UPLOAD_PURCHASE_DRAFT_ATTACHMENT = "UPLOAD_PURCHASE_DRAFT_ATTACHMENT"
    CREATE_PURCHASE_FROM_DRAFT = "CREATE_PURCHASE_FROM_DRAFT"

    # Inbox
    GET_INBOX_DOCUMENTS = "GET_INBOX_DOCUMENTS"
    UPLOAD_INBOX_DOCUMENT = "UPLOAD_INBOX_DOCUMENT"
    GET_INBOX_DOCUMENT = "GET_INBOX_DOCUMENT"

    # Projects
    GET_PROJECTS = "GET_PROJECTS"
    CREATE_PROJECT = "CREATE_PROJECT"
    GET_PROJECT = "GET_PROJECT"
    UPDATE_PROJECT = "UPDATE_PROJECT" # PATCH
    DELETE_PROJECT = "DELETE_PROJECT"


class FikenAuthenticationMethod:
    PERSONAL_API_TOKEN = "personal_api_token"
    OAUTH2 = "oauth2" # Schema defined, but execution not fully implemented


class FikenNode(BaseNode):
    """
    Node for interacting with the Fiken Accounting API (v2).
    Supports all documented operations like retrieving companies, managing contacts,
    invoices, purchases, products, journal entries, etc.
    Primarily uses Personal API Tokens for authentication. OAuth2 support is defined
    in the schema but requires external flow management for token acquisition/refresh.
    Note: Fiken API has rate limits (1 concurrent request, ~4 req/sec).
    """
    # Base URL for Fiken API v2
    BASE_URL = "https://api.fiken.no/api/v2"

    # Mapping from Operation Enum to (HTTP_METHOD, URL_TEMPLATE)
    # Placeholders: {companySlug}, {resourceId}, {subResourceId}
    _OPERATION_MAP: Dict[str, Tuple[str, str]] = {
        # User Info
        FikenOperation.GET_USER_INFO: ("GET", "/user"),
        # Companies
        FikenOperation.GET_COMPANIES: ("GET", "/companies"),
        FikenOperation.GET_COMPANY: ("GET", "/companies/{companySlug}"),
        # Accounts
        FikenOperation.GET_ACCOUNTS: ("GET", "/companies/{companySlug}/accounts"),
        FikenOperation.GET_ACCOUNT: ("GET", "/companies/{companySlug}/accounts/{resourceId}"),
        FikenOperation.GET_ACCOUNT_BALANCES: ("GET", "/companies/{companySlug}/accountBalances"),
        FikenOperation.GET_ACCOUNT_BALANCE: ("GET", "/companies/{companySlug}/accountBalances/{resourceId}"),
        # Bank Accounts
        FikenOperation.GET_BANK_ACCOUNTS: ("GET", "/companies/{companySlug}/bankAccounts"),
        FikenOperation.CREATE_BANK_ACCOUNT: ("POST", "/companies/{companySlug}/bankAccounts"),
        FikenOperation.GET_BANK_ACCOUNT: ("GET", "/companies/{companySlug}/bankAccounts/{resourceId}"),
        # Contacts
        FikenOperation.GET_CONTACTS: ("GET", "/companies/{companySlug}/contacts"),
        FikenOperation.CREATE_CONTACT: ("POST", "/companies/{companySlug}/contacts"),
        FikenOperation.GET_CONTACT: ("GET", "/companies/{companySlug}/contacts/{resourceId}"),
        FikenOperation.UPDATE_CONTACT: ("PUT", "/companies/{companySlug}/contacts/{resourceId}"),
        FikenOperation.DELETE_CONTACT: ("DELETE", "/companies/{companySlug}/contacts/{resourceId}"),
        FikenOperation.UPLOAD_CONTACT_ATTACHMENT: ("POST", "/companies/{companySlug}/contacts/{resourceId}/attachments"),
        FikenOperation.GET_CONTACT_PERSONS: ("GET", "/companies/{companySlug}/contacts/{resourceId}/contactPerson"),
        FikenOperation.CREATE_CONTACT_PERSON: ("POST", "/companies/{companySlug}/contacts/{resourceId}/contactPerson"),
        FikenOperation.GET_CONTACT_PERSON: ("GET", "/companies/{companySlug}/contacts/{resourceId}/contactPerson/{subResourceId}"),
        FikenOperation.UPDATE_CONTACT_PERSON: ("PUT", "/companies/{companySlug}/contacts/{resourceId}/contactPerson/{subResourceId}"),
        FikenOperation.DELETE_CONTACT_PERSON: ("DELETE", "/companies/{companySlug}/contacts/{resourceId}/contactPerson/{subResourceId}"),
        # Groups
        FikenOperation.GET_GROUPS: ("GET", "/companies/{companySlug}/groups"),
        # Products
        FikenOperation.CREATE_PRODUCT_SALES_REPORT: ("POST", "/companies/{companySlug}/products/salesReport"),
        FikenOperation.GET_PRODUCTS: ("GET", "/companies/{companySlug}/products"),
        FikenOperation.CREATE_PRODUCT: ("POST", "/companies/{companySlug}/products"),
        FikenOperation.GET_PRODUCT: ("GET", "/companies/{companySlug}/products/{resourceId}"),
        FikenOperation.UPDATE_PRODUCT: ("PUT", "/companies/{companySlug}/products/{resourceId}"),
        FikenOperation.DELETE_PRODUCT: ("DELETE", "/companies/{companySlug}/products/{resourceId}"),
        # Journal Entries
        FikenOperation.GET_JOURNAL_ENTRIES: ("GET", "/companies/{companySlug}/journalEntries"),
        FikenOperation.CREATE_GENERAL_JOURNAL_ENTRY: ("POST", "/companies/{companySlug}/generalJournalEntries"),
        FikenOperation.GET_JOURNAL_ENTRY: ("GET", "/companies/{companySlug}/journalEntries/{resourceId}"),
        FikenOperation.GET_JOURNAL_ENTRY_ATTACHMENTS: ("GET", "/companies/{companySlug}/journalEntries/{resourceId}/attachments"),
        FikenOperation.UPLOAD_JOURNAL_ENTRY_ATTACHMENT: ("POST", "/companies/{companySlug}/journalEntries/{resourceId}/attachments"),
        # Transactions
        FikenOperation.GET_TRANSACTIONS: ("GET", "/companies/{companySlug}/transactions"),
        FikenOperation.GET_TRANSACTION: ("GET", "/companies/{companySlug}/transactions/{resourceId}"),
        # Invoices
        FikenOperation.GET_INVOICES: ("GET", "/companies/{companySlug}/invoices"),
        FikenOperation.CREATE_INVOICE: ("POST", "/companies/{companySlug}/invoices"),
        FikenOperation.GET_INVOICE: ("GET", "/companies/{companySlug}/invoices/{resourceId}"),
        FikenOperation.UPDATE_INVOICE: ("PATCH", "/companies/{companySlug}/invoices/{resourceId}"),
        FikenOperation.GET_INVOICE_ATTACHMENTS: ("GET", "/companies/{companySlug}/invoices/{resourceId}/attachments"),
        FikenOperation.UPLOAD_INVOICE_ATTACHMENT: ("POST", "/companies/{companySlug}/invoices/{resourceId}/attachments"),
        FikenOperation.SEND_INVOICE: ("POST", "/companies/{companySlug}/invoices/send"),
        FikenOperation.GET_INVOICE_COUNTER: ("GET", "/companies/{companySlug}/invoices/counter"),
        FikenOperation.SET_INVOICE_COUNTER: ("POST", "/companies/{companySlug}/invoices/counter"),
        FikenOperation.GET_INVOICE_DRAFTS: ("GET", "/companies/{companySlug}/invoices/drafts"),
        FikenOperation.CREATE_INVOICE_DRAFT: ("POST", "/companies/{companySlug}/invoices/drafts"),
        FikenOperation.GET_INVOICE_DRAFT: ("GET", "/companies/{companySlug}/invoices/drafts/{resourceId}"),
        FikenOperation.UPDATE_INVOICE_DRAFT: ("PUT", "/companies/{companySlug}/invoices/drafts/{resourceId}"),
        FikenOperation.DELETE_INVOICE_DRAFT: ("DELETE", "/companies/{companySlug}/invoices/drafts/{resourceId}"),
        FikenOperation.GET_INVOICE_DRAFT_ATTACHMENTS: ("GET", "/companies/{companySlug}/invoices/drafts/{resourceId}/attachments"),
        FikenOperation.UPLOAD_INVOICE_DRAFT_ATTACHMENT: ("POST", "/companies/{companySlug}/invoices/drafts/{resourceId}/attachments"),
        FikenOperation.CREATE_INVOICE_FROM_DRAFT: ("POST", "/companies/{companySlug}/invoices/drafts/{resourceId}/createInvoice"),
        # Credit Notes
        FikenOperation.GET_CREDIT_NOTES: ("GET", "/companies/{companySlug}/creditNotes"),
        FikenOperation.CREATE_FULL_CREDIT_NOTE: ("POST", "/companies/{companySlug}/creditNotes/full"),
        FikenOperation.CREATE_PARTIAL_CREDIT_NOTE: ("POST", "/companies/{companySlug}/creditNotes/partial"),
        FikenOperation.GET_CREDIT_NOTE: ("GET", "/companies/{companySlug}/creditNotes/{resourceId}"),
        FikenOperation.SEND_CREDIT_NOTE: ("POST", "/companies/{companySlug}/creditNotes/send"),
        FikenOperation.GET_CREDIT_NOTE_COUNTER: ("GET", "/companies/{companySlug}/creditNotes/counter"),
        FikenOperation.SET_CREDIT_NOTE_COUNTER: ("POST", "/companies/{companySlug}/creditNotes/counter"),
        FikenOperation.GET_CREDIT_NOTE_DRAFTS: ("GET", "/companies/{companySlug}/creditNotes/drafts"),
        FikenOperation.CREATE_CREDIT_NOTE_DRAFT: ("POST", "/companies/{companySlug}/creditNotes/drafts"),
        FikenOperation.GET_CREDIT_NOTE_DRAFT: ("GET", "/companies/{companySlug}/creditNotes/drafts/{resourceId}"),
        FikenOperation.UPDATE_CREDIT_NOTE_DRAFT: ("PUT", "/companies/{companySlug}/creditNotes/drafts/{resourceId}"),
        FikenOperation.DELETE_CREDIT_NOTE_DRAFT: ("DELETE", "/companies/{companySlug}/creditNotes/drafts/{resourceId}"),
        FikenOperation.GET_CREDIT_NOTE_DRAFT_ATTACHMENTS: ("GET", "/companies/{companySlug}/creditNotes/drafts/{resourceId}/attachments"),
        FikenOperation.UPLOAD_CREDIT_NOTE_DRAFT_ATTACHMENT: ("POST", "/companies/{companySlug}/creditNotes/drafts/{resourceId}/attachments"),
        FikenOperation.CREATE_CREDIT_NOTE_FROM_DRAFT: ("POST", "/companies/{companySlug}/creditNotes/drafts/{resourceId}/createCreditNote"),
        # Offers
        FikenOperation.GET_OFFERS: ("GET", "/companies/{companySlug}/offers"),
        FikenOperation.GET_OFFER: ("GET", "/companies/{companySlug}/offers/{resourceId}"),
        FikenOperation.GET_OFFER_COUNTER: ("GET", "/companies/{companySlug}/offers/counter"),
        FikenOperation.SET_OFFER_COUNTER: ("POST", "/companies/{companySlug}/offers/counter"),
        FikenOperation.GET_OFFER_DRAFTS: ("GET", "/companies/{companySlug}/offers/drafts"),
        FikenOperation.CREATE_OFFER_DRAFT: ("POST", "/companies/{companySlug}/offers/drafts"),
        FikenOperation.GET_OFFER_DRAFT: ("GET", "/companies/{companySlug}/offers/drafts/{resourceId}"),
        FikenOperation.UPDATE_OFFER_DRAFT: ("PUT", "/companies/{companySlug}/offers/drafts/{resourceId}"),
        FikenOperation.DELETE_OFFER_DRAFT: ("DELETE", "/companies/{companySlug}/offers/drafts/{resourceId}"),
        FikenOperation.GET_OFFER_DRAFT_ATTACHMENTS: ("GET", "/companies/{companySlug}/offers/drafts/{resourceId}/attachments"),
        FikenOperation.UPLOAD_OFFER_DRAFT_ATTACHMENT: ("POST", "/companies/{companySlug}/offers/drafts/{resourceId}/attachments"),
        FikenOperation.CREATE_OFFER_FROM_DRAFT: ("POST", "/companies/{companySlug}/offers/drafts/{resourceId}/createOffer"),
        # Order Confirmations
        FikenOperation.GET_ORDER_CONFIRMATIONS: ("GET", "/companies/{companySlug}/orderConfirmations"),
        FikenOperation.GET_ORDER_CONFIRMATION: ("GET", "/companies/{companySlug}/orderConfirmations/{resourceId}"),
        FikenOperation.GET_ORDER_CONFIRMATION_COUNTER: ("GET", "/companies/{companySlug}/orderConfirmations/counter"),
        FikenOperation.SET_ORDER_CONFIRMATION_COUNTER: ("POST", "/companies/{companySlug}/orderConfirmations/counter"),
        FikenOperation.CREATE_INVOICE_DRAFT_FROM_ORDER_CONFIRMATION: ("POST", "/companies/{companySlug}/orderConfirmations/{resourceId}/createInvoiceDraft"),
        FikenOperation.GET_ORDER_CONFIRMATION_DRAFTS: ("GET", "/companies/{companySlug}/orderConfirmations/drafts"),
        FikenOperation.CREATE_ORDER_CONFIRMATION_DRAFT: ("POST", "/companies/{companySlug}/orderConfirmations/drafts"),
        FikenOperation.GET_ORDER_CONFIRMATION_DRAFT: ("GET", "/companies/{companySlug}/orderConfirmations/drafts/{resourceId}"),
        FikenOperation.UPDATE_ORDER_CONFIRMATION_DRAFT: ("PUT", "/companies/{companySlug}/orderConfirmations/drafts/{resourceId}"),
        FikenOperation.DELETE_ORDER_CONFIRMATION_DRAFT: ("DELETE", "/companies/{companySlug}/orderConfirmations/drafts/{resourceId}"),
        FikenOperation.GET_ORDER_CONFIRMATION_DRAFT_ATTACHMENTS: ("GET", "/companies/{companySlug}/orderConfirmations/drafts/{resourceId}/attachments"),
        FikenOperation.UPLOAD_ORDER_CONFIRMATION_DRAFT_ATTACHMENT: ("POST", "/companies/{companySlug}/orderConfirmations/drafts/{resourceId}/attachments"),
        FikenOperation.CREATE_ORDER_CONFIRMATION_FROM_DRAFT: ("POST", "/companies/{companySlug}/orderConfirmations/drafts/{resourceId}/createOrderConfirmation"),
        # Sales
        FikenOperation.GET_SALES: ("GET", "/companies/{companySlug}/sales"),
        FikenOperation.CREATE_SALE: ("POST", "/companies/{companySlug}/sales"),
        FikenOperation.GET_SALE: ("GET", "/companies/{companySlug}/sales/{resourceId}"),
        FikenOperation.SET_SALE_SETTLED: ("PATCH", "/companies/{companySlug}/sales/{resourceId}/settled"),
        FikenOperation.DELETE_SALE: ("PATCH", "/companies/{companySlug}/sales/{resourceId}/delete"),
        FikenOperation.GET_SALE_ATTACHMENTS: ("GET", "/companies/{companySlug}/sales/{resourceId}/attachments"),
        FikenOperation.UPLOAD_SALE_ATTACHMENT: ("POST", "/companies/{companySlug}/sales/{resourceId}/attachments"),
        FikenOperation.GET_SALE_PAYMENTS: ("GET", "/companies/{companySlug}/sales/{resourceId}/payments"),
        FikenOperation.CREATE_SALE_PAYMENT: ("POST", "/companies/{companySlug}/sales/{resourceId}/payments"),
        FikenOperation.GET_SALE_PAYMENT: ("GET", "/companies/{companySlug}/sales/{resourceId}/payments/{subResourceId}"),
        FikenOperation.GET_SALE_DRAFTS: ("GET", "/companies/{companySlug}/sales/drafts"),
        FikenOperation.CREATE_SALE_DRAFT: ("POST", "/companies/{companySlug}/sales/drafts"),
        FikenOperation.GET_SALE_DRAFT: ("GET", "/companies/{companySlug}/sales/drafts/{resourceId}"),
        FikenOperation.UPDATE_SALE_DRAFT: ("PUT", "/companies/{companySlug}/sales/drafts/{resourceId}"),
        FikenOperation.DELETE_SALE_DRAFT: ("DELETE", "/companies/{companySlug}/sales/drafts/{resourceId}"),
        FikenOperation.GET_SALE_DRAFT_ATTACHMENTS: ("GET", "/companies/{companySlug}/sales/drafts/{resourceId}/attachments"),
        FikenOperation.UPLOAD_SALE_DRAFT_ATTACHMENT: ("POST", "/companies/{companySlug}/sales/drafts/{resourceId}/attachments"),
        FikenOperation.CREATE_SALE_FROM_DRAFT: ("POST", "/companies/{companySlug}/sales/drafts/{resourceId}/createSale"),
        # Purchases
        FikenOperation.GET_PURCHASES: ("GET", "/companies/{companySlug}/purchases"),
        FikenOperation.CREATE_PURCHASE: ("POST", "/companies/{companySlug}/purchases"),
        FikenOperation.GET_PURCHASE: ("GET", "/companies/{companySlug}/purchases/{resourceId}"),
        FikenOperation.DELETE_PURCHASE: ("PATCH", "/companies/{companySlug}/purchases/{resourceId}/delete"),
        FikenOperation.GET_PURCHASE_ATTACHMENTS: ("GET", "/companies/{companySlug}/purchases/{resourceId}/attachments"),
        FikenOperation.UPLOAD_PURCHASE_ATTACHMENT: ("POST", "/companies/{companySlug}/purchases/{resourceId}/attachments"),
        FikenOperation.GET_PURCHASE_PAYMENTS: ("GET", "/companies/{companySlug}/purchases/{resourceId}/payments"),
        FikenOperation.CREATE_PURCHASE_PAYMENT: ("POST", "/companies/{companySlug}/purchases/{resourceId}/payments"),
        FikenOperation.GET_PURCHASE_PAYMENT: ("GET", "/companies/{companySlug}/purchases/{resourceId}/payments/{subResourceId}"),
        FikenOperation.GET_PURCHASE_DRAFTS: ("GET", "/companies/{companySlug}/purchases/drafts"),
        FikenOperation.CREATE_PURCHASE_DRAFT: ("POST", "/companies/{companySlug}/purchases/drafts"),
        FikenOperation.GET_PURCHASE_DRAFT: ("GET", "/companies/{companySlug}/purchases/drafts/{resourceId}"),
        FikenOperation.UPDATE_PURCHASE_DRAFT: ("PUT", "/companies/{companySlug}/purchases/drafts/{resourceId}"),
        FikenOperation.DELETE_PURCHASE_DRAFT: ("DELETE", "/companies/{companySlug}/purchases/drafts/{resourceId}"),
        FikenOperation.GET_PURCHASE_DRAFT_ATTACHMENTS: ("GET", "/companies/{companySlug}/purchases/drafts/{resourceId}/attachments"),
        FikenOperation.UPLOAD_PURCHASE_DRAFT_ATTACHMENT: ("POST", "/companies/{companySlug}/purchases/drafts/{resourceId}/attachments"),
        FikenOperation.CREATE_PURCHASE_FROM_DRAFT: ("POST", "/companies/{companySlug}/purchases/drafts/{resourceId}/createPurchase"),
        # Inbox
        FikenOperation.GET_INBOX_DOCUMENTS: ("GET", "/companies/{companySlug}/inbox"),
        FikenOperation.UPLOAD_INBOX_DOCUMENT: ("POST", "/companies/{companySlug}/inbox"),
        FikenOperation.GET_INBOX_DOCUMENT: ("GET", "/companies/{companySlug}/inbox/{resourceId}"),
        # Projects
        FikenOperation.GET_PROJECTS: ("GET", "/companies/{companySlug}/projects"),
        FikenOperation.CREATE_PROJECT: ("POST", "/companies/{companySlug}/projects"),
        FikenOperation.GET_PROJECT: ("GET", "/companies/{companySlug}/projects/{resourceId}"),
        FikenOperation.UPDATE_PROJECT: ("PATCH", "/companies/{companySlug}/projects/{resourceId}"),
        FikenOperation.DELETE_PROJECT: ("DELETE", "/companies/{companySlug}/projects/{resourceId}"),
    }

    # Define operation-parameter mapping as a class attribute
    # Lists required/relevant parameters for each operation
    _operation_parameters = {
        # --- User ---
        "GET_USER_INFO": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken"],
        # --- Companies ---
        "GET_COMPANIES": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "queryParams"], # Query supports pagination/sorting
        "GET_COMPANY": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug"],
        # --- Accounts ---
        "GET_ACCOUNTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports filtering
        "GET_ACCOUNT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_ACCOUNT_BALANCES": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/filtering
        "GET_ACCOUNT_BALANCE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        # --- Bank Accounts ---
        "GET_BANK_ACCOUNTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/filtering
        "CREATE_BANK_ACCOUNT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_BANK_ACCOUNT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        # --- Contacts ---
        "GET_CONTACTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/sorting/filtering
        "CREATE_CONTACT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_CONTACT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPDATE_CONTACT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "DELETE_CONTACT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPLOAD_CONTACT_ATTACHMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "filePath", "fileName", "queryParams"], # Query can specify filename, description
        "GET_CONTACT_PERSONS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "CREATE_CONTACT_PERSON": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "GET_CONTACT_PERSON": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "subResourceId"],
        "UPDATE_CONTACT_PERSON": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "subResourceId", "requestBody"],
        "DELETE_CONTACT_PERSON": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "subResourceId"],
        # --- Groups ---
        "GET_GROUPS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug"],
        # --- Products ---
        "CREATE_PRODUCT_SALES_REPORT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_PRODUCTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/filtering
        "CREATE_PRODUCT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_PRODUCT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPDATE_PRODUCT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "DELETE_PRODUCT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        # --- Journal Entries ---
        "GET_JOURNAL_ENTRIES": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/filtering
        "CREATE_GENERAL_JOURNAL_ENTRY": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_JOURNAL_ENTRY": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_JOURNAL_ENTRY_ATTACHMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPLOAD_JOURNAL_ENTRY_ATTACHMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "filePath", "fileName", "queryParams"], # Query can specify filename, description
        # --- Transactions ---
        "GET_TRANSACTIONS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/filtering
        "GET_TRANSACTION": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        # --- Invoices ---
        "GET_INVOICES": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/filtering
        "CREATE_INVOICE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_INVOICE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPDATE_INVOICE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "GET_INVOICE_ATTACHMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPLOAD_INVOICE_ATTACHMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "filePath", "fileName", "queryParams"], # Query can specify filename, description
        "SEND_INVOICE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_INVOICE_COUNTER": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug"],
        "SET_INVOICE_COUNTER": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_INVOICE_DRAFTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination
        "CREATE_INVOICE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_INVOICE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPDATE_INVOICE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "DELETE_INVOICE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_INVOICE_DRAFT_ATTACHMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPLOAD_INVOICE_DRAFT_ATTACHMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "filePath", "fileName", "queryParams"], # Query can specify filename, description
        "CREATE_INVOICE_FROM_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        # --- Credit Notes ---
        "GET_CREDIT_NOTES": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/filtering
        "CREATE_FULL_CREDIT_NOTE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "CREATE_PARTIAL_CREDIT_NOTE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_CREDIT_NOTE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "SEND_CREDIT_NOTE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_CREDIT_NOTE_COUNTER": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug"],
        "SET_CREDIT_NOTE_COUNTER": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_CREDIT_NOTE_DRAFTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination
        "CREATE_CREDIT_NOTE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_CREDIT_NOTE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPDATE_CREDIT_NOTE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "DELETE_CREDIT_NOTE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_CREDIT_NOTE_DRAFT_ATTACHMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPLOAD_CREDIT_NOTE_DRAFT_ATTACHMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "filePath", "fileName", "queryParams"],
        "CREATE_CREDIT_NOTE_FROM_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
         # --- Offers ---
        "GET_OFFERS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination
        "GET_OFFER": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_OFFER_COUNTER": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug"],
        "SET_OFFER_COUNTER": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_OFFER_DRAFTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination
        "CREATE_OFFER_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_OFFER_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPDATE_OFFER_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "DELETE_OFFER_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_OFFER_DRAFT_ATTACHMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPLOAD_OFFER_DRAFT_ATTACHMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "filePath", "fileName", "queryParams"],
        "CREATE_OFFER_FROM_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        # --- Order Confirmations ---
        "GET_ORDER_CONFIRMATIONS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination
        "GET_ORDER_CONFIRMATION": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_ORDER_CONFIRMATION_COUNTER": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug"],
        "SET_ORDER_CONFIRMATION_COUNTER": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "CREATE_INVOICE_DRAFT_FROM_ORDER_CONFIRMATION": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_ORDER_CONFIRMATION_DRAFTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination
        "CREATE_ORDER_CONFIRMATION_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_ORDER_CONFIRMATION_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPDATE_ORDER_CONFIRMATION_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "DELETE_ORDER_CONFIRMATION_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_ORDER_CONFIRMATION_DRAFT_ATTACHMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPLOAD_ORDER_CONFIRMATION_DRAFT_ATTACHMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "filePath", "fileName", "queryParams"],
        "CREATE_ORDER_CONFIRMATION_FROM_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        # --- Sales ---
        "GET_SALES": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/filtering
        "CREATE_SALE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_SALE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "SET_SALE_SETTLED": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"], # Body likely specifies settled status
        "DELETE_SALE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_SALE_ATTACHMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPLOAD_SALE_ATTACHMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "filePath", "fileName", "queryParams"],
        "GET_SALE_PAYMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "CREATE_SALE_PAYMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "GET_SALE_PAYMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "subResourceId"],
        "GET_SALE_DRAFTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination
        "CREATE_SALE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_SALE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPDATE_SALE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "DELETE_SALE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_SALE_DRAFT_ATTACHMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPLOAD_SALE_DRAFT_ATTACHMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "filePath", "fileName", "queryParams"],
        "CREATE_SALE_FROM_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        # --- Purchases ---
        "GET_PURCHASES": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/sorting/filtering
        "CREATE_PURCHASE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_PURCHASE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "DELETE_PURCHASE": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_PURCHASE_ATTACHMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPLOAD_PURCHASE_ATTACHMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "filePath", "fileName", "queryParams"],
        "GET_PURCHASE_PAYMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "CREATE_PURCHASE_PAYMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "GET_PURCHASE_PAYMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "subResourceId"],
        "GET_PURCHASE_DRAFTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination
        "CREATE_PURCHASE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_PURCHASE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPDATE_PURCHASE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "DELETE_PURCHASE_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "GET_PURCHASE_DRAFT_ATTACHMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPLOAD_PURCHASE_DRAFT_ATTACHMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "filePath", "fileName", "queryParams"],
        "CREATE_PURCHASE_FROM_DRAFT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        # --- Inbox ---
        "GET_INBOX_DOCUMENTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/sorting/filtering
        "UPLOAD_INBOX_DOCUMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "filePath", "fileName", "queryParams"], # Query can specify filename, description, etc.
        "GET_INBOX_DOCUMENT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        # --- Projects ---
        "GET_PROJECTS": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "queryParams"], # Query supports pagination/filtering
        "CREATE_PROJECT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "requestBody"],
        "GET_PROJECT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
        "UPDATE_PROJECT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId", "requestBody"],
        "DELETE_PROJECT": ["operation", "authenticationMethod", "personalApiToken", "oauthAccessToken", "companySlug", "resourceId"],
    }

    def __init__(self, sandbox_timeout: Optional[int] = None):
        super().__init__(sandbox_timeout=sandbox_timeout)
        if not HTTPX_AVAILABLE:
            raise ImportError("FikenNode requires the 'httpx' library. Please install it.")
        # Consider initializing the client here or per-request if timeouts/proxies change
        # self.client = httpx.AsyncClient(timeout=30.0) # Example initialization

    def get_schema(self) -> NodeSchema:
        """Return the schema definition for the Fiken node."""
        return NodeSchema(
            node_type="fiken",
            version="2.0.0", # Aligns with API version
            description="Interacts with the Fiken Accounting API v2",
            parameters=[
                # Core parameters
                NodeParameter(
                    name="operation",
                    type=NodeParameterType.STRING,
                    description="The Fiken API operation to perform",
                    required=True,
                    enum=[op.value for op in FikenOperation] # Use enum values
                ),
                NodeParameter(
                    name="authenticationMethod",
                    type=NodeParameterType.STRING,
                    description="Authentication method to use",
                    required=True,
                    enum=[auth.value for auth in FikenAuthenticationMethod],
                    default=FikenAuthenticationMethod.PERSONAL_API_TOKEN
                ),
                NodeParameter(
                    name="personalApiToken",
                    type=NodeParameterType.STRING,
                    description="Fiken Personal API Token (used if authenticationMethod is personal_api_token)",
                    required=False # Required based on authenticationMethod
                ),
                NodeParameter(
                    name="oauthAccessToken",
                    type=NodeParameterType.STRING,
                    description="Fiken OAuth2 Access Token (used if authenticationMethod is oauth2)",
                    required=False # Required based on authenticationMethod
                ),
                NodeParameter(
                    name="companySlug",
                    type=NodeParameterType.STRING,
                    description="The unique slug identifying the Fiken company (required for most operations)",
                    required=False # Required based on operation
                ),

                # Identifiers
                NodeParameter(
                    name="resourceId",
                    type=NodeParameterType.STRING,
                    description="Identifier for the primary resource (e.g., contactId, invoiceId, productId, accountCode, draftId)",
                    required=False # Required based on operation
                ),
                 NodeParameter(
                    name="subResourceId",
                    type=NodeParameterType.STRING,
                    description="Identifier for a nested resource (e.g., contactPersonId, paymentId)",
                    required=False # Required based on operation
                ),

                # Data and Files
                NodeParameter(
                    name="requestBody",
                    type=NodeParameterType.OBJECT, # Use OBJECT for JSON payloads
                    description="JSON data payload for POST, PUT, PATCH requests",
                    required=False # Required based on operation
                ),
                 NodeParameter(
                    name="filePath",
                    type=NodeParameterType.STRING,
                    description="Path to the file to upload for attachment/inbox operations",
                    required=False # Required based on operation
                ),
                 NodeParameter(
                    name="fileName",
                    type=NodeParameterType.STRING,
                    description="Optional filename for the uploaded file (defaults to original filename)",
                    required=False
                ),

                # Querying
                NodeParameter(
                    name="queryParams",
                    type=NodeParameterType.OBJECT,
                    description="Key-value pairs for URL query parameters (pagination, filtering, sorting)",
                    required=False
                ),
            ],

            # Define outputs for the node
            outputs={
                "status": NodeParameterType.STRING, # 'success' or 'error'
                "result": NodeParameterType.ANY,    # Parsed JSON response or success message
                "error": NodeParameterType.STRING,   # Error message if status is 'error'
                "statusCode": NodeParameterType.NUMBER, # HTTP status code
                "responseHeaders": NodeParameterType.OBJECT # Response headers (e.g., Location, pagination)
            },

            # Add metadata
            tags=["accounting", "fiken", "erp", "api"],
            author="System" # Or your name/organization
        )

    def get_operation_parameters(self, operation: str) -> List[Dict[str, Any]]:
        """Get parameters relevant to a specific Fiken operation."""
        param_names = self._operation_parameters.get(operation, [])
        all_params = self.get_schema().parameters

        operation_params = []
        for param in all_params:
            if param.name in param_names:
                param_dict = {
                    "name": param.name,
                    "type": param.type.value if hasattr(param.type, 'value') else str(param.type),
                    "description": param.description,
                    "required": param.required # Note: Actual requirement might depend on context (e.g., auth method)
                }
                if hasattr(param, 'default') and param.default is not None:
                    param_dict["default"] = param.default
                if hasattr(param, 'enum') and param.enum:
                    param_dict["enum"] = param.enum
                operation_params.append(param_dict)

        return operation_params

    def validate_custom(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Custom validation based on the operation and parameters."""
        params = node_data.get("params", {})
        operation = params.get("operation")
        auth_method = params.get("authenticationMethod")

        if not operation:
            raise NodeValidationError("Fiken 'operation' is required.")
        if not auth_method:
            raise NodeValidationError("Fiken 'authenticationMethod' is required.")

        # Validate Authentication
        if auth_method == FikenAuthenticationMethod.PERSONAL_API_TOKEN:
            if not params.get("personalApiToken"):
                raise NodeValidationError("Fiken 'personalApiToken' is required for personal_api_token authentication.")
        elif auth_method == FikenAuthenticationMethod.OAUTH2:
            if not params.get("oauthAccessToken"):
                 raise NodeValidationError("Fiken 'oauthAccessToken' is required for oauth2 authentication.")
        else:
            raise NodeValidationError(f"Invalid authenticationMethod: {auth_method}")

        # Validate common requirements based on operation map
        if operation in self._OPERATION_MAP:
            method, url_template = self._OPERATION_MAP[operation]

            # Check for companySlug
            if "{companySlug}" in url_template and not params.get("companySlug"):
                raise NodeValidationError(f"Fiken 'companySlug' is required for operation '{operation}'.")

            # Check for resourceId
            if "{resourceId}" in url_template and not params.get("resourceId"):
                raise NodeValidationError(f"Fiken 'resourceId' is required for operation '{operation}'. Provide the relevant ID (e.g., contactId, invoiceId).")

            # Check for subResourceId
            if "{subResourceId}" in url_template and not params.get("subResourceId"):
                 raise NodeValidationError(f"Fiken 'subResourceId' is required for operation '{operation}'. Provide the relevant nested ID (e.g., contactPersonId, paymentId).")

            # Check for requestBody
            if method in ["POST", "PUT", "PATCH"] and not url_template.endswith("/attachments"): # Attachments use files, not JSON body
                # Some POST/PATCH might not *strictly* require a body (e.g., create from draft, send),
                # but it's safer to require it generally for data modification ops.
                # Check specific operations that might be exceptions.
                is_attachment_upload = "ATTACHMENT" in operation.upper() or operation in [
                    FikenOperation.UPLOAD_INBOX_DOCUMENT
                ]
                is_action_without_body = operation in [
                     FikenOperation.CREATE_INVOICE_FROM_DRAFT,
                     FikenOperation.CREATE_CREDIT_NOTE_FROM_DRAFT,
                     FikenOperation.CREATE_OFFER_FROM_DRAFT,
                     FikenOperation.CREATE_ORDER_CONFIRMATION_FROM_DRAFT,
                     FikenOperation.CREATE_SALE_FROM_DRAFT,
                     FikenOperation.CREATE_PURCHASE_FROM_DRAFT,
                     FikenOperation.CREATE_INVOICE_DRAFT_FROM_ORDER_CONFIRMATION,
                     FikenOperation.DELETE_SALE, # Uses PATCH but no body expected
                     FikenOperation.DELETE_PURCHASE, # Uses PATCH but no body expected
                     FikenOperation.SET_SALE_SETTLED, # Uses PATCH, might require simple body? Check docs. Assume yes for now.
                ]

                if not is_attachment_upload and not is_action_without_body and not params.get("requestBody"):
                     raise NodeValidationError(f"Fiken 'requestBody' (JSON object) is required for operation '{operation}'.")
                elif not is_attachment_upload and not is_action_without_body and not isinstance(params.get("requestBody"), dict):
                    raise NodeValidationError(f"Fiken 'requestBody' must be a JSON object for operation '{operation}'.")

            # Check for filePath for uploads
            is_upload_operation = "UPLOAD_" in operation.upper() or operation == FikenOperation.UPLOAD_INBOX_DOCUMENT
            if is_upload_operation:
                file_path = params.get("filePath")
                if not file_path:
                    raise NodeValidationError(f"Fiken 'filePath' is required for upload operation '{operation}'.")
                if not isinstance(file_path, str):
                     raise NodeValidationError(f"Fiken 'filePath' must be a string path.")
                if not os.path.exists(file_path):
                    raise NodeValidationError(f"File not found at specified filePath: {file_path}")
                if not os.path.isfile(file_path):
                     raise NodeValidationError(f"Specified filePath is not a file: {file_path}")

        else:
            raise NodeValidationError(f"Unknown Fiken operation specified: {operation}")

        return {} # No errors found

    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the Fiken API request."""
        start_time = time.monotonic()
        if not HTTPX_AVAILABLE:
            return self._format_error_output("httpx library is not installed.")

        try:
            # Validate schema and custom rules
            params = self.validate_schema(node_data)
            self.validate_custom(node_data) # Run custom validation again on validated params

            operation = params.get("operation")
            auth_method = params.get("authenticationMethod")
            request_id = str(uuid.uuid4()) # Generate unique request ID

            # --- Get Operation Details ---
            if operation not in self._OPERATION_MAP:
                return self._format_error_output(f"Operation '{operation}' not implemented in _OPERATION_MAP.")
            http_method, url_template = self._OPERATION_MAP[operation]

            # --- Build URL ---
            url = self._build_url(url_template, params)
            query_params = params.get("queryParams") # Keep as dict

            # --- Build Headers ---
            headers = self._build_headers(auth_method, params, request_id)

            # --- Prepare Request Data/Files ---
            request_content = None
            request_files = None
            request_data = None # For form-encoded (not used here currently)

            is_upload = "UPLOAD_" in operation.upper() or operation == FikenOperation.UPLOAD_INBOX_DOCUMENT
            if http_method in ["POST", "PUT", "PATCH"] and not is_upload:
                # Check if body is expected
                if params.get("requestBody"):
                    try:
                        request_content = json.dumps(params["requestBody"]).encode('utf-8')
                        headers["Content-Type"] = "application/json"
                    except (TypeError, json.JSONDecodeError) as json_err:
                        return self._format_error_output(f"Invalid JSON in requestBody: {json_err}")
            elif is_upload:
                file_path = params.get("filePath")
                file_name = params.get("fileName") or os.path.basename(file_path)
                try:
                    # httpx expects files in a specific format: {'file': (filename, file_obj, content_type)}
                    # Fiken attachment endpoints seem to take file directly, maybe with form data?
                    # Let's try sending as multipart/form-data with 'file' as the key.
                    # Query params like 'filename' and 'description' might be needed for some uploads.
                    file_obj = open(file_path, 'rb')
                    # We need to close the file later
                    request_files = {'file': (file_name, file_obj, 'application/octet-stream')} # Generic content type
                    # Fiken docs don't explicitly state multipart, but it's common for uploads.
                    # If this fails, might need raw binary PUT/POST. Test required.
                    # Remove explicit Content-Type header for httpx to set multipart correctly
                    headers.pop("Content-Type", None)

                except IOError as e:
                    return self._format_error_output(f"Error opening file {file_path}: {e}")
                except Exception as e: # Catch other potential errors during file prep
                    if 'file_obj' in locals() and file_obj: file_obj.close() # Ensure cleanup
                    return self._format_error_output(f"Error preparing file for upload: {e}")


            # --- Make Request ---
            async with httpx.AsyncClient(timeout=60.0) as client: # Use context manager for client
                try:
                    logger.info(f"Executing Fiken Operation: {operation} ({http_method} {url}) RequestID: {request_id}")
                    response = await client.request(
                        method=http_method,
                        url=url,
                        headers=headers,
                        params=query_params,
                        content=request_content, # Use content for raw bytes (JSON)
                        files=request_files,     # Use files for multipart uploads
                        # data=request_data # Use data for form-encoded
                    )

                    # Raise exceptions for 4xx/5xx errors
                    response.raise_for_status()

                    # --- Process Response ---
                    response_headers = dict(response.headers)
                    status_code = response.status_code

                    # Handle successful responses (200, 201, 204 No Content)
                    if status_code in [200, 201]:
                        try:
                            result_data = response.json()
                        except json.JSONDecodeError:
                            # Handle cases where response is successful but not JSON
                            result_data = response.text
                    elif status_code == 204: # No Content for DELETE etc.
                         result_data = {"message": "Operation successful (No Content)"}
                    else:
                        # Should have been caught by raise_for_status, but handle defensively
                         result_data = response.text


                    logger.info(f"Fiken Operation {operation} completed successfully (Status: {status_code}) RequestID: {request_id}")
                    return {
                        "status": "success",
                        "result": result_data,
                        "error": None,
                        "statusCode": status_code,
                        "responseHeaders": response_headers
                    }

                except httpx.HTTPStatusError as e:
                    error_body = "<no response body>"
                    try:
                        error_body = e.response.read().decode()
                    except Exception:
                        pass # Ignore if reading fails
                    error_message = f"HTTP Error {e.response.status_code}: {e.request.url}. Response: {error_body}"
                    logger.error(f"Fiken Operation {operation} failed. RequestID: {request_id}. Error: {error_message}", exc_info=True)
                    return self._format_error_output(error_message, e.response.status_code, dict(e.response.headers))

                except httpx.RequestError as e:
                    error_message = f"Request Error for {e.request.url}: {str(e)}"
                    logger.error(f"Fiken Operation {operation} failed. RequestID: {request_id}. Error: {error_message}", exc_info=True)
                    return self._format_error_output(error_message)

                except Exception as e:
                    error_message = f"Unexpected error during Fiken API call: {str(e)}"
                    logger.error(f"Fiken Operation {operation} failed unexpectedly. RequestID: {request_id}. Error: {error_message}", exc_info=True)
                    return self._format_error_output(error_message)

                finally:
                    # Ensure uploaded file is closed
                    if request_files and 'file' in request_files:
                        try:
                           request_files['file'][1].close()
                        except Exception as close_err:
                           logger.warning(f"Error closing uploaded file: {close_err}")

        except NodeValidationError as e:
            logger.error(f"Validation failed for Fiken node: {str(e)}")
            return self._format_error_output(f"Validation Error: {str(e)}", 400)
        except Exception as e:
            error_message = f"Internal error in Fiken node execution: {str(e)}"
            logger.error(error_message, exc_info=True)
            return self._format_error_output(error_message, 500)

    def _build_url(self, url_template: str, params: Dict[str, Any]) -> str:
        """Constructs the full API URL from the template and parameters."""
        url = self.BASE_URL + url_template
        url = url.replace("{companySlug}", params.get("companySlug", ""))
        url = url.replace("{resourceId}", params.get("resourceId", ""))
        url = url.replace("{subResourceId}", params.get("subResourceId", ""))
        # Clean up potential double slashes if IDs are missing, though validation should prevent this.
        url = url.replace("//", "/").rstrip("/")
        return url

    def _build_headers(self, auth_method: str, params: Dict[str, Any], request_id: str) -> Dict[str, str]:
        """Builds the necessary request headers."""
        headers = {
            "Accept": "application/json",
            # "Content-Type": "application/json", # Set dynamically based on content/files
            "X-Request-ID": request_id
        }
        if auth_method == FikenAuthenticationMethod.PERSONAL_API_TOKEN:
            token = params.get("personalApiToken")
            headers["Authorization"] = f"Bearer {token}"
        elif auth_method == FikenAuthenticationMethod.OAUTH2:
            token = params.get("oauthAccessToken")
            headers["Authorization"] = f"Bearer {token}"

        return headers

    def _format_error_output(self, error_message: str, status_code: Optional[int] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Creates a standardized error output dictionary."""
        return {
            "status": "error",
            "result": None,
            "error": error_message,
            "statusCode": status_code,
            "responseHeaders": headers or {}
        }


# Register with NodeRegistry (assuming NodeRegistry is globally accessible)
try:
    NodeRegistry.register("fiken", FikenNode)
    logger.info("Registered node type: fiken")
except NameError:
     logger.warning("NodeRegistry not found. Skipping registration of FikenNode.")
except Exception as e:
    logger.error(f"Error registering Fiken node: {str(e)}")

# Example Usage (for testing purposes)
async def main():
    if not HTTPX_AVAILABLE:
        print("httpx not installed, cannot run example.")
        return

    # --- Configuration (Replace with your actual data) ---
    FIKEN_API_TOKEN = os.environ.get("FIKEN_API_TOKEN") # Get from environment variable
    FIKEN_COMPANY_SLUG = os.environ.get("FIKEN_COMPANY_SLUG") # Get from environment variable

    if not FIKEN_API_TOKEN or not FIKEN_COMPANY_SLUG:
        print("Please set FIKEN_API_TOKEN and FIKEN_COMPANY_SLUG environment variables to run the example.")
        return

    fiken_node = FikenNode()

    # --- Example 1: Get Companies (Requires only token) ---
    node_data_get_companies = {
        "id": "fiken",
        "type": "FikenNode",
        "params": {
            "operation": FikenOperation.GET_COMPANIES,
            "authenticationMethod": FikenAuthenticationMethod.PERSONAL_API_TOKEN,
            "personalApiToken": FIKEN_API_TOKEN,
            "queryParams": {"page": 0, "pageSize": 5} # Example pagination
        }
    }
    print("\n--- Getting Companies ---")
    result_companies = await fiken_node.execute(node_data_get_companies)
    print(json.dumps(result_companies, indent=2))

    # --- Example 2: Get Contacts for a specific company ---
    node_data_get_contacts = {
        "id": "fiken2",
        "type": "fiken",
        "params": {
            "operation": FikenOperation.GET_CONTACTS,
            "authenticationMethod": FikenAuthenticationMethod.PERSONAL_API_TOKEN,
            "personalApiToken": FIKEN_API_TOKEN,
            "companySlug": FIKEN_COMPANY_SLUG,
             "queryParams": {"pageSize": 10, "sortBy": "name asc"} # Example filter/sort
        }
    }
    print("\n--- Getting Contacts ---")
    result_contacts = await fiken_node.execute(node_data_get_contacts)
    print(json.dumps(result_contacts, indent=2))

    # --- Example 3: Create a Contact (Requires Body) ---
    node_data_create_contact = {
         "id": "fiken3",
         "type": "fiken",
         "params": {
             "operation": FikenOperation.CREATE_CONTACT,
             "authenticationMethod": FikenAuthenticationMethod.PERSONAL_API_TOKEN,
             "personalApiToken": FIKEN_API_TOKEN,
             "companySlug": FIKEN_COMPANY_SLUG,
             "requestBody": {
                 "name": f"API Test Contact {int(time.time())}",
                 "email": f"test.contact.{int(time.time())}@example.com",
                 "customer": True
                 # Add other required/optional fields as per Fiken Schema
             }
         }
     }
    print("\n--- Creating Contact ---")
    result_create = await fiken_node.execute(node_data_create_contact)
    print(json.dumps(result_create, indent=2))

    # --- Example 4: Upload an Inbox Document (Requires File Path) ---
    # Create a dummy file for upload
    dummy_file_path = "dummy_invoice.pdf"
    try:
        with open(dummy_file_path, "w") as f:
            f.write("This is a dummy PDF content.")

        node_data_upload_inbox = {
            "id": "fiken4",
            "type": "fiken",
            "params": {
                "operation": FikenOperation.UPLOAD_INBOX_DOCUMENT,
                "authenticationMethod": FikenAuthenticationMethod.PERSONAL_API_TOKEN,
                "personalApiToken": FIKEN_API_TOKEN,
                "companySlug": FIKEN_COMPANY_SLUG,
                "filePath": dummy_file_path,
                "fileName": "api_uploaded_invoice.pdf", # Optional custom name
                "queryParams": {"description": "Uploaded via API Node"} # Example query param
            }
        }
        print("\n--- Uploading Inbox Document ---")
        result_upload = await fiken_node.execute(node_data_upload_inbox)
        print(json.dumps(result_upload, indent=2))
    except Exception as e:
        print(f"Error during upload example: {e}")
    finally:
        if os.path.exists(dummy_file_path):
            os.remove(dummy_file_path) # Clean up dummy file

if __name__ == "__main__":
    # To run the example:
    # 1. Install httpx: pip install httpx
    # 2. Save this code as fiken_node.py
    # 3. Save base_node.py (or ensure it's importable)
    # 4. Set environment variables:
    #    export FIKEN_API_TOKEN="your_actual_fiken_api_token"
    #    export FIKEN_COMPANY_SLUG="your_actual_fiken_company_slug"
    # 5. Run: python fiken_node.py
    asyncio.run(main())