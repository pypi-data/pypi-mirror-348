import enum

@enum.unique
class Broker(enum.StrEnum):
    MSTOCK = 'mstock'
    CHOICE = 'choice'
    DHAN = 'dhan'
    FIVEPAISA = 'fivepaisa'
    FIVEPAISA_XTS = 'fivepaisa-xts'
    FYERS = 'fyers'
    MOTILAL_OSWAL = 'mo'
    UPSTOX = 'upstox'
    ALICEBLUE = 'aliceblue'
    NUVAMA = 'nuvama'
    SHAREKHAN = 'sharekhan'
    ANGEL = 'angel'
    ZERODHA = 'zerodha'


@enum.unique
class BrokerRole(enum.StrEnum):
    OWNER = 'owner'
    READER = 'reader'
    EXECUTOR = 'executor'

@enum.unique
class BrokerAccountValidity(enum.StrEnum):
    EXPIRED = '-2'
    UNKNOWN = '-1'
    INFINITY = '0'

@enum.unique
class OrderTransactionType(enum.StrEnum):
    BUY = 'b'
    SELL = 's'

@enum.unique
class OrderProductType(enum.StrEnum):
    INTRADAY = 'intraday'
    NORMAL_ORDER = 'nrml'


@enum.unique
class OrderType(enum.StrEnum):    
    LIMIT = 'limit'
    MARKET = 'market'
    STOP_LOSS_LIMIT = 'sll'
    STOP_LOSS_MARKET = 'slm'

@enum.unique
class OrderStatus(enum.StrEnum):    
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    PARTIAL = 'partial'
    PENDING = 'pending'
    FAILED = 'failed'
    REJECTED = 'rejected'
    TRANSIT = 'transit'


@enum.unique
class OrderValidity(enum.StrEnum):    
    DAY = 'day'
    IOC = 'ioc'


