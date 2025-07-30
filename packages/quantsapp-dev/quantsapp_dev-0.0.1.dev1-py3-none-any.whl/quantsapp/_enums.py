import enum


@enum.unique
class Exchange(enum.StrEnum):
    NSE_FNO = 'NSE-FO'


@enum.unique
class InstrumentType(enum.StrEnum):
    CALL = 'c'
    PUT = 'p'
    FUTURE = 'x'
    __OPTIONS = 'o'  # To be used only for internal purposes



@enum.unique
class AccountTypes(enum.StrEnum):
    FREE = 'free'
    PRO = 'pro'
    PRO_PLUS = 'pro_plus'



@enum.unique
class ErrorCodes(enum.StrEnum):

    # Input Error Codes
    INVALID_INPUT = 'QE-1'
    LOGIN_NOT_INITIATED = 'QE-2'

    # API Error Codes
    API_CONNECTION_ERROR = 'QE-API-1'
    INVALID_LOGIN_CREDENTIALS = 'QE-API-2'
    
    # Execution Error Codes
    NO_BROKER_ACCOUNTS_MAPPED = 'QE-EX-1'
    BROKER_LOGIN_NOT_ALLOWED = 'QE-EX-2'
    INVALID_BROKER_LOGIN_CREDENTIALS = 'QE-EX-3'
    BROKER_LOGIN_FAILED = 'QE-EX-4'
    BROKER_ACCOUNT_DELETION_FAILED = 'QE-EX-5'
    BROKER_ORDERS_LISTING_FAILED = 'QE-EX-6'
    BROKER_POSITIONS_LISTING_FAILED = 'QE-EX-7'
    BROKER_ORDERS_PLACING_FAILED = 'QE-EX-8'
    BROKER_ORDERS_CANCEL_FAILED = 'QE-EX-9'
    BROKER_ORDER_BOOK_UPDATE_FAILED = 'QE-EX-10'

    BROKER_WS_CONN_STATUS_FAILED = 'QE-EX-WS-1'
    BROKER_WS_RE_CONN_FAILED = 'QE-EX-WS-2'
