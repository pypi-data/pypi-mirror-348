from quantsapp import _enums as generic_enums

# -- Input Exceptions --------------------------------------------------------------------------------


class InvalidInputError(Exception):
    """Quantsapp Custom exception for Invalid Input from client"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.INVALID_INPUT


class LoginNotInitiatedError(Exception):
    """Quantsapp Custom exception for login not initiated by client"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.LOGIN_NOT_INITIATED



# -- API exceptions ----------------------------------------------------------------------------------

class APIConnectionError(Exception):
    """Quantsapp Custom exception for Invalid Login Credentials"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.API_CONNECTION_ERROR


class InvalidLoginCredentials(Exception):
    """Quantsapp Custom exception for Invalid Login Credentials"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.INVALID_LOGIN_CREDENTIALS



# -- Execution exceptions ----------------------------------------------------------------------------

class NoBrokerAccountsMapped(Exception):
    """Quantsapp Custom exception for No broker accounts mapped"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.NO_BROKER_ACCOUNTS_MAPPED


class BrokerLoginNotAllowed(Exception):
    """Quantsapp Custom exception for Broker login not allowed on API services"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.NO_BROKER_ACCOUNTS_MAPPED


class InvalidBrokerLoginParams(Exception):
    """Quantsapp Custom exception for invalid credentials for Broker login"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.INVALID_BROKER_LOGIN_CREDENTIALS

class BrokerLoginFailed(Exception):
    """Quantsapp Custom exception for Broker login failed from API"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.BROKER_LOGIN_FAILED

class BrokerDeletionFailed(Exception):
    """Quantsapp Custom exception for Broker account deletion failed from API"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.BROKER_ACCOUNT_DELETION_FAILED

class BrokerWsConnectionStatusFailed(Exception):
    """Quantsapp Custom exception for Broker Websocket Connection Status failed from API"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.BROKER_WS_CONN_STATUS_FAILED

class BrokerWsReConnectionFailed(Exception):
    """Quantsapp Custom exception for Broker Websocket Connection Status failed from API"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.BROKER_WS_RE_CONN_FAILED

class BrokerOrdersListingFailed(Exception):
    """Quantsapp Custom exception for Broker account order listing failed from API"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.BROKER_ORDERS_LISTING_FAILED

class BrokerOrderBookUpdateFailed(Exception):
    """Quantsapp Custom exception for Broker account order listing failed from API"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.BROKER_ORDER_BOOK_UPDATE_FAILED

class BrokerPositionsListingFailed(Exception):
    """Quantsapp Custom exception for Broker account order listing failed from API"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.BROKER_POSITIONS_LISTING_FAILED

class BrokerOrdersPlacingFailed(Exception):
    """Quantsapp Custom exception for Broker account order placing failed from API"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.BROKER_ORDERS_PLACING_FAILED

class BrokerOrdersCancelFailed(Exception):
    """Quantsapp Custom exception for Broker orders cancel failed from API"""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = generic_enums.ErrorCodes.BROKER_ORDERS_CANCEL_FAILED