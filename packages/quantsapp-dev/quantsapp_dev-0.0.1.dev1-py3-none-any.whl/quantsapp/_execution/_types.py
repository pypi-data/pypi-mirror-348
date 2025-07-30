# Built-in Modules
import typing
import datetime as dt


# Local Modules
from quantsapp import (
    _enums as generic_enums,
    _models as generic_models,
    _types as generic_types,
)
from quantsapp._execution import (
    _enums as execution_enums,
    _models as execution_models,
)


# ----------------------------------------------------------------------------------------------------

Brokers = typing.Literal[
    'mstock',
    'choice',
    'dhan',
    'fivepaisa',
    'fyers',
    'mo',
    'upstox',
    'aliceblue',
    'nuvama',
    'sharekhan',
    'angel',
    'fivepaisa-xts',
    'zerodha',
]

ApiResponseStatus = typing.Literal['0', '1']

BrokerRoles = typing.Literal['owner', 'reader','executor']

# -- Broker Listing ----------------------------------------------------------------------------------


# region Broker Listing

class ListAvailableBrokersResponse(typing.TypedDict):
    access_token_login: list[execution_enums.Broker | str]
    oauth_login: list[execution_enums.Broker | str]


ListBrokersApiIndividualDataMarginResponse = typing.TypedDict(
    'ListBrokersApiIndividualDataMarginResponse',
    {
        'dt': generic_types.DateTime,
        'NSE-FO': generic_types.NumericString,
    },
)
"""sample
```
{
    "dt": "02-May-25 02:18:50",
    "NSE-FO": "1534.53"
}
"""


class ListBrokersApiIndividualDataResponse(typing.TypedDict):
    """sample
    ```
    {
        "broker": "fivepaisa",
        "client_id": "50477264",
        "role": "executor",
        "name": "SHUBHRA",
        "validity": "02-May-25 23:59:59",
        "valid": true,
        "margin": ListBrokersApiIndividualDataMarginResponse
    }
    """
    broker: Brokers
    client_id: str
    role: BrokerRoles
    name: str
    validity: generic_types.DateTime | typing.Literal['0', '-1', '-2']
    valid: bool
    margin: ListBrokersApiIndividualDataMarginResponse


class ListBrokersApiResponse(typing.TypedDict):
    """sample
    ```
    {
        "status": "1",
        "msg": "No accounts available" | "success",
        "routeKey": "broker_login",
        "custom_key": "access_expiry_config",
        "ws_msg_type": "qapp_api_gateway_options_success_api_request"

        # Only available if accounts are mapped
        "data": [
            ListBrokersApiIndividualDataResponse,
        ],
        "version": "9",
        "next_margin_dt_utc": "02-May-25 02:33:50",
    }
    """
    status: ApiResponseStatus
    msg: str

    # Only present if accounts already mapped
    data: list[ListBrokersApiIndividualDataResponse]
    version: generic_types.NumericString
    next_margin_dt_utc: generic_types.DateTime


class ListBrokersIndividualBrokerData(typing.TypedDict):
    client_id: str
    margin: ListBrokersApiIndividualDataMarginResponse
    name: str
    role: BrokerRoles
    valid: bool
    validity: dt.datetime | execution_enums.BrokerAccountValidity


class ListBrokersResponse(typing.TypedDict):
    brokers: dict[execution_enums.Broker, ListBrokersIndividualBrokerData]
    version: int
    next_margin: dt.datetime

# endregion


# -- Broker Login DB Data ----------------------------------------------------------------------------


# region Broker Login DB Data

BrokerOrderProductType = typing.Literal['NRML', 'INTRADAY']
BrokerOrderExecutionType = typing.Literal['LIMIT', 'MARKET', 'SL-L']
BrokerOrderValidity = typing.Literal['IOC', 'DAY']

class OrderBrokerLoginDbData(typing.TypedDict):
    exe_type: BrokerOrderExecutionType
    product_type: BrokerOrderProductType
    validity: BrokerOrderValidity

class IndividualBrokerLoginDbData(typing.TypedDict):
    """sample
    ```
    {
        "mstock": {
            "name": "Mstock",
            "ui_login_only": true,
            "order": {
                "exe_type": [
                    "LIMIT",
                    "MARKET",
                    "SL-L"
                ],
                "product_type": [
                    "NRML",
                    "INTRADAY"
                ],
                "validity": [
                    "IOC",
                    "DAY"
                ]
            },
            "is_live": false,
            "login_types": ["totp", "login"],
            "index": "1"
        }
    }
    """
    name: str
    ui_login_only: bool
    is_live: bool
    index: generic_types.NumericString
    order: OrderBrokerLoginDbData
    login_types: typing.Literal['login', 'totp']

BrokerLoginDbData = dict[Brokers, IndividualBrokerLoginDbData]

class BrokerLoginDbVersionData(typing.TypedDict):
    data: dict[Brokers, IndividualBrokerLoginDbData] | str
    version: int

class BrokerLoginDbDataApiResponse(typing.TypedDict):
    """sample
    ```
    {
        'status': '1',
        'msg': str,
        'broker_login_data': str | BrokerLoginDbData,
    }
    """
    status: ApiResponseStatus
    msg: str
    broker_login_data: BrokerLoginDbVersionData

# endregion


# -- Client Info -------------------------------------------------------------------------------------


# region Client Info


class ClientCheckApiResponse(typing.TypedDict):
    """sample
    ```
    # Account not exists
    {
        'status': '1',
        'msg': 'Account available to add',
        'redirect_url': str,
        'webhook_url': str,
        'exists': False,
    }

    # Account exists and user has access to it
    {
        'status': '1',
        'msg': 'You already have an Approved role of EXECUTOR',
        'redirect_url': str,
        'webhook_url': str,
        'exists': True,
        'ac_role': 'executor',
    }

    # Account exists and user not having access to it
    {
        'status': '1',
        'msg': 'Account exists, Request access',
        'redirect_url': str,
        'webhook_url': str,
        'exists': True,
    }
    """
    status: ApiResponseStatus
    msg: str
    redirect_url: str
    webhook_url: str
    exists: bool

    # Only if account exists and user has access to it
    ac_role: BrokerRoles


class ClientCheckResponse(typing.TypedDict):
    is_account_exists: bool
    msg: str
    
    # Only if account exists and user has access to it
    role: typing.NotRequired[execution_enums.BrokerRole]


# endregion


# -- Broker Login ------------------------------------------------------------------------------------

class BrokerLoginApiResponse(typing.TypedDict):
    status: ApiResponseStatus
    msg: str

class BrokerDeleteApiResponse(typing.TypedDict):
    status: ApiResponseStatus
    msg: str
    version: generic_types.NumericString
    global_version: generic_types.NumericString


class DhanBrokerLoginCredentials(typing.TypedDict):
    access_token: str

class ChoiceBrokerLoginCredentials(typing.TypedDict):
    mobile: str
    client_access_token: str

BrokerLoginCredentials = typing.Union[
    DhanBrokerLoginCredentials,
    ChoiceBrokerLoginCredentials,
]


class BrokerWsConnStatusApiResponse(typing.TypedDict):
    """Sample
    ```
    {
        "status": "1",
        "msg": "Connected",
        "ts_ping": 1747129266,
        "ts_msg": 1747126860,
        "ts_conn": 0,
    }
    """
    status: ApiResponseStatus
    msg: str
    ts_ping: int
    ts_msg: int
    ts_conn: int


class BrokerWsReConnApiResponse(typing.TypedDict):
    """Sample
    ```
    {
        "status": "1",
        "msg": "Connected",
    }
    """
    status: ApiResponseStatus
    msg: str

# -- Broker Orders -----------------------------------------------------------------------------------

Exchanges = typing.Literal[
    'NSE-FO',
]

OrderTypes = typing.Literal[
    'limit',
    'market',
    'sll',  # Stop Loss Limit (Both price)
    'slm',  # Stop Loss Market (only trigger price)
]

OrderTransactionTypes = typing.Literal[
    'b',  # Buy
    's',  # Sell
]

OrderSegments = typing.Literal[
    'o',  # Options
    'x',  # Future
]

OrderOptionTypes = typing.Literal[
    'c',
    'p',
]

ProductTypes = typing.Literal[
    'intraday',
    'nrml',  # Normal order
]

OrderStatus = typing.Literal[
    'completed',
    'pending',
    'partial',
    'cancelled',
    'failed',
    'rejected',
    'transit',
]

OrderValidity = typing.Literal[
    'day',
    'ioc',  # Immediate or Cancelled
]

class OrderListingData(typing.TypedDict):
    """sample
    ```
    {
        'broker_client': 'mstock,MA6232931',
        'b_orderid': '33422505073382',
        'qty': 75,
        'price': 1.2,
        'buy_sell': execution_enums.Order,
        'instrument': 'NIFTY:15-May-25:c:25500',
        'order_type': execution_enums.OrderType,
        'product_type': 'nrml',
        'q_usec': 1746596369775443,
        'userid': 622594,
        'order_status': 'pending',
        'b_usec_update': 1746596370000000,
        'e_orderid': 1600000075847609,
        'o_ctr': 1,  # TODO update on realtime ws, update only when the counter is higher than existing
        'qty_filled': 0,
        'stop_price': 0.0
    }
    """
    # broker_client: str
    broker_client: execution_models.BrokerClient
    b_orderid: generic_types.NumericString  # Broker OrderID when placing order
    qty: int
    price: float
    buy_sell: execution_enums.OrderTransactionType
    # instrument: str
    instrument: generic_models.Instrument
    order_type: execution_enums.OrderType
    product_type: execution_enums.OrderProductType
    q_usec: dt.datetime  # Quantsapp Order Send Timestamp in ms
    userid: int  # User ID of client who placed the order
    order_status: execution_enums.OrderStatus
    b_usec_update: dt.datetime  # Broker Order Updation Timestamp in ms
    e_orderid: str  # Exchange OrderID when placing order
    o_ctr: int  # Order Update counter
    qty_filled: int
    stop_price: float


class OrderListingApiResponseData(typing.TypedDict):
    """sample
    ```
    {
        'broker_client': 'mstock,MA6232931',
        'b_orderid': '33422505073382',
        'qty': 75,
        'price': 1.2,
        'buy_sell': 'b',
        'instrument': 'NIFTY:15-May-25:c:25500',
        'order_type': 'limit',
        'product_type': 'nrml',
        'q_usec': 1746596369775443,
        'userid': 622594,
        'order_status': 'pending',
        'b_usec_update': 1746596370000000,
        'e_orderid': 1600000075847609,
        'o_ctr': 1,
        'qty_filled': 0,
        'stop_price': 0.0
    }
    """
    broker_client: str
    b_orderid: generic_types.NumericString  # BrokerID when placing order
    qty: int
    price: float
    buy_sell: typing.Literal['b', 's']
    instrument: str
    order_type: OrderTypes
    product_type: ProductTypes
    q_usec: int  # Quantsapp Order Send Timestamp in ms
    userid: int  # User ID of client who placed the order
    order_status: OrderStatus
    b_usec_update: int  # Broker Order Updation Timestamp in ms
    e_orderid: int  # Another BrokerID when placing order
    o_ctr: int  # Order Update counter
    qty_filled: int
    stop_price: float


class OrderLogsListingApiResponseData(typing.TypedDict):
    """sample
    ```
    {
        'status': '1',
        'msg': 'success',
        'order_apilog': [
            {
                'http_code': 200,
                'b_response': '{"res": [{"status": true, "message": "SUCCESS", "errorcode": "", "data": {"script": "NIFTY2551525500CE", "orderid": "31622505137802", "uniqueorderid": "31622505137802"}}]}',
                'q_msg': 'success',
                'q_usec': 1747114712000000
            }
        ],
    }
    """
    status: ApiResponseStatus
    msg: str
    order_apilog: list[dict[str, typing.Any]]


class GetOrdersAccountWiseApiResponse(typing.TypedDict):
    """sample
    ```
    {
        'status': '1',
        'msg': 'success',
        'gzip': True,
        'orders': 'H4sIAOsVG2gC/02Qy27DIBBFfyVinUSYZ+xdN5WySFfdVFWFbEwrFPwIDAur6r+XsdsorGDunTPDff8mXZyuLhobvBuBNDsyJJjsdX95UoyzmldkvyOdmWLvou/RwLlgTFJJNecnhvINliJoWa5z9NaVR3Vk2JcXk1wI2Nah048JYh7+Rr2cn1/fmkoeLu1yYLKxDZOSUjSu8wwsM8JI8IMHsuKnPlu4C2McwrqByclZnKuFkrXiqtZaCsGLVpRtc1XWrsUdnqCFnJAyu7H349f2UwSZPPctuAeeptspFvcQRqW2spYnoRWtEW4sRJS2YMynD8GhF3tLtrP5z4ge6c/HL86ik8+DAQAA',
        'pagination_key': typing.Any  # Optional, only available if more records are there (current limit is 100)
    }
    """
    status: ApiResponseStatus
    msg: str
    gzip: bool
    orders: str | list[OrderListingApiResponseData]
    pagination_key: typing.Optional[typing.Any]



class BrokerOrderIds(typing.TypedDict):
    """sample
    ```
    {
        'b_orderid': '32422505083020',
        'e_order_id': '1600000051220406',
    }
    """
    b_orderid: str
    e_order_id: str | int


class PlaceOrderBrokerAccountsPayload(typing.TypedDict):
    """sample
    ```
    {
        'broker': quantsapp.Broker.MSTOCK,
        'client_id': 'MA6232931',
        'lot_multiplier': 1,  # Default is 1
    }
    """
    
    broker: execution_enums.Broker
    client_id: str
    lot_multiplier: typing.Optional[int]

class PlaceOrderLegPayload(typing.TypedDict):
    """sample
    ```
    {
        'qty': 75,
        'price': 1.1,
        'symbol': 'NIFTY',
        'expiry': dt.datetime(year=2025, month=5, day=15),
        'instrument_type': quantsapp.InstrumentType.CALL_OPTIONS,
        'strike': 22500,  # Only for call or put options
        'transaction_type': quantsapp.OrderTransactionType.BUY
    }
    """
    qty: int
    price: float
    symbol: str
    expiry: dt.datetime
    instrument_type: generic_enums.InstrumentType
    transaction_type: OrderTransactionTypes

    # Only for Options
    strike: typing.Optional[int | float]


class PlaceOrdersPayload(typing.TypedDict):
    """sample
    ```
    {
        'broker_accounts': [
            PlaceOrderBrokerAccountsPayload
        ],
        'exchange': quantsapp.Exchange.NSE_FNO,
        'product': quantsapp.OrderProductType.NORMAL_ORDER,
        'order_type': quantsapp.OrderType.LIMIT,
        'validity': quantsapp.OrderValidity.DAY,
        "legs": [
            PlaceOrderLegData
        ]
    }
    """
    broker_accounts: list[PlaceOrderBrokerAccountsPayload]
    exchange: generic_enums.Exchange
    product: execution_enums.OrderProductType
    order_type: execution_enums.OrderType
    validity: execution_enums.OrderValidity
    legs: list[PlaceOrderLegPayload]

class PlaceOrderLegApiPayload(typing.TypedDict):
    """sample
    ```
    {
        "qty": 75,
        "price": 1.1,
        "symbol": "NIFTY",
        "segment": "o",
        "opt_type": "c",
        "expiry": "15-May-25",
        "strike": 25500,
        "buy_sell": "b"
    }
    """
    qty: int
    price: float
    symbol: str
    segment: OrderSegments
    expiry: str
    buy_sell: OrderTransactionTypes

    # Only for Options
    opt_type: typing.Optional[OrderOptionTypes]
    strike: typing.Optional[float | int]


class PlaceOrderApiPayload(typing.TypedDict):
    """sample
    ```
    {
        "accounts": {
            "mstock,MA6232931": 1
        },
        "exchange": "NSE-FO",
        "product": "nrml",
        "order_type": "limit",
        "validity": "day",
        "legs": [
            PlaceOrderLegData
        ]
    }
    """
    accounts: dict[str, int]
    exchange: Exchanges
    product: ProductTypes
    order_type: OrderTypes
    validity: OrderValidity
    legs: list[PlaceOrderLegApiPayload]

class PlaceOrderApiResponse(typing.TypedDict):
    """sample
    ```
    {
        'status': '1',
        'msg': 'success',
        'has_failed': True,
        'q_ref_id': 8,
    }
    """
    status: ApiResponseStatus
    msg: str

    has_failed: bool
    q_ref_id: int



class PlaceOrdersResponse(typing.TypedDict):
    """sample
    ```
    {
        'success': bool,
        'ref_id': 8
    }
    """
    success: bool
    ref_id: int

class ModifyOrderApiResponse(typing.TypedDict):
    """sample
    ```
    {
        "status": "1",
        "msg": "Modified !",    
    }
    """
    status: ApiResponseStatus
    msg: str



class CancelOrdersPayload(typing.TypedDict):
    """sample
    ```
    {
        'broker': quantsapp.Broker.MSTOCK,
        'client_id': 'MA6232931',
        'order_ids': [
            BrokerOrderIds,
        ]
    }
    """
    broker: execution_enums.Broker
    client_id: str
    order_ids: list[BrokerOrderIds]



class CancelOrdersApiPayload(typing.TypedDict):
    """sample
    ```
    {
        "action": "broker_orders",
        "mode": "cancel_orders",
        "order": {
            "mstock,MA6232931": [
                {
                    "b_orderid": "32422505083020",
                    "e_orderid": 1600000051220406
                }
            ]
        },
    }
    """
    ...



class CancelOrdersApiResponse(typing.TypedDict):
    """sample
    ```
    {
        "status": "1",
        "msg": "success",
        "has_failed": false,
        "q_ref_id_c": 15
    }
    """
    status: ApiResponseStatus
    msg: str

    has_failed: bool
    q_ref_id_c: int


class CancelOrdersResponse(typing.TypedDict):
    """sample
    ```
    {
        'success': bool,
        'ref_id': 8
    }
    """
    success: bool
    ref_id: int


class GetPositionsPayload(typing.TypedDict):
    """sample
    ```
    {
        'broker': quantsapp.Broker.MSTOCK,
        'client_id': 'MA6232931',
    }
    """
    broker: execution_enums.Broker
    client_id: str



class PositionsCombinedApiResponseData(typing.TypedDict):
    """sample
    ```
    {
        'instrument': 'NIFTY:15-May-25:c:25200',
        'product_type': 'nrml',
        'buy_qty': 75,
        'buy_t_value': 581.25,
        'sell_qty': 75,
        'sell_t_value': 570
    }
    """
    instrument: str
    product_type: ProductTypes
    buy_qty: int
    buy_t_value: int | float
    sell_qty: int
    sell_t_value: int | float

class PositionsAccountwiseApiResponseData(typing.TypedDict):
    """sample
    ```
    {
        'mstock,MA6232931': [
            {
                'instrument': 'NIFTY:15-May-25:c:25900',
                'product_type': 'nrml',
                'buy_qty': 75,
                'buy_t_value': 93.75,
                'sell_qty': 75,
                'sell_t_value': 86.25
                'p_ctr': 3,
            },
        ]
    }
    """
    instrument: str  # TODO change this to instrument type
    product_type: ProductTypes
    buy_qty: int
    buy_t_value: int | float
    sell_qty: int
    sell_t_value: int | float
    p_ctr: int


class GetPositionsApiResponse(typing.TypedDict):
    """sample
    ```
    {
        "status": "1",
        "msg": "success",
        "gzip": true,
        "positions": "H4sIABvKIWgC/4uuVsrMKy4pKs1NzStRslJQ8vN0C4m0MjTV9U2s1DUytUq2MjI1MjBQ0lFQKijKTylNLokvqSxIBSnNK8rNAYknlVbGF5ZUAoXMTaHckviyxJxSkCpTC0M9I5BwcWpODrIyMB9JnblBbSwAX3B17I4AAAA=",
    }
    """
    status: ApiResponseStatus
    msg: str
    gzip: bool
    positions: str | list[PositionsCombinedApiResponseData | PositionsAccountwiseApiResponseData]




class PositionsAccountwiseListingData(typing.TypedDict):
    """sample
    ```
    {
        'instrument': 'NIFTY:15-May-25:c:25200',
        'product_type': 'nrml',
        'buy_qty': 75,
        'buy_t_value': 581.25,
        'sell_qty': 75,
        'sell_t_value': 570
        'p_ctr': 3,  # TODO same logic as o_ctr, Check whether position data coming on order updates ws (This will come once order got completed)
    }
    """

    instrument: str
    product_type: execution_enums.OrderProductType
    buy_qty: int
    buy_t_value: int | float
    sell_qty: int
    sell_t_value: int | float
    p_ctr: int



class PositionsCombinedListingData(typing.TypedDict):
    """sample
    ```
    {
        'instrument': 'NIFTY:15-May-25:c:25200',
        'product_type': 'nrml',
        'buy_qty': 75,
        'buy_t_value': 581.25,
        'sell_qty': 75,
        'sell_t_value': 570
    }
    """

    instrument: str
    product_type: execution_enums.OrderProductType
    buy_qty: int
    buy_t_value: int | float
    sell_qty: int
    sell_t_value: int | float



class UpdateOrderBookApiResponse(typing.TypedDict):
    """sample
    ```
    {
        "status": "1",
        "msg": "Orderbook Updated !",
        "orders_response": {
            "status": "1",
            "msg": "success",
            "gzip": true,
            "orders": "H4sIAJ4pI2gC/72Su07DMBSGX6Xy3Fa+5DhONhYkhjKxIISs1DGS1VxaxxkixLvj45YKEAMhEp7sc/5z+T/56ZXsde9r611NyhURAjgHCkxkheBkvSJ73x+s16ZxtgsoaYfQm8N6dyO54IVgSaTHwRo9Husq2ChieZYzLhUUNB2UjJMebNNgiz3W2E9zmUwyViiqsgJkTLtuCH5sL0Pv724fHksGm101bTiUpuQAlGKfXpvgo0bgHTvqIVRhHLDMVJ2JM21NrskwHXFD0rjWBQwfvTMYoVsK6dnXowlXXefbBmWnZPFnb6cwxUQO56t+cWlkbBkDsersUUawRfa2Xn1HzvkHcsXpUuSczkUuhMoY/RPybDHyfA7yz96WIWfygjxXdOEvZ7jaPOQUJCiVdv/3X8627NfEv1qbQ/z5HYpc1iFYBAAA"
        },
        "trade_status": "1",
        "trade_msg": "Tradebook Updated !",
        "positions_status": "1",
        "positions_msg": "Positions Updated !",
    }
    {
        "status": "1",
        "msg": "Orderbook Updated !",
        "positions_response": {
            "status": "1",
            "msg": "success",
            "gzip": true,
            "positions": "H4sIANUpI2gC/4uOBQApu0wNAgAAAA=="
        },
        "trade_status": "1",
        "trade_msg": "Tradebook Updated !",
        "positions_status": "1",
        "positions_msg": "Positions Updated !",
    }
    """
    status: ApiResponseStatus
    msg: str
    trade_status: str
    trade_msg: str
    positions_status: str
    positions_msg: str

    orders_response: typing.Optional[GetOrdersAccountWiseApiResponse]
    positions_response: typing.Optional[GetPositionsApiResponse]