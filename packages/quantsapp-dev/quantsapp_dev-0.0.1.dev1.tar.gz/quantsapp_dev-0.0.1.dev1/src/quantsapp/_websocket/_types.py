# Built-in Modules
import typing
import collections.abc


# Local Modules
from quantsapp import _types as generic_types
from quantsapp._execution import _types as execution_types


# -- Websocket ---------------------------------------------------------------------------------------

class WaitCondition(typing.TypedDict):
    wait_condition: collections.abc.Callable[[], bool]
    notify_condition: typing.Optional[collections.abc.Callable[[], None]]
    sleep_sec: int


# -- Main Websocket ----------------------------------------------------------------------------------

ApiResponseStatus = typing.Literal['0', '1']


class MainOptionsWsMarketTimingsApiResponse(typing.TypedDict):
    """sample
    {
        'open': '2025-05-09T09:15:00+05:30',
        'close': '2025-05-09T15:30:00+05:30',
        'is_open_today': True
    }
    """
    open: generic_types.DateTimeIso
    close: generic_types.DateTimeIso
    is_open_today: bool


class MainOptionsWsAccountTypeApiResponse(typing.TypedDict):
    """sample
    {
        'ac_type': 'pro_plus'
    }
    """
    ac_type: generic_types.AccountType


class MainOptionsWsSessionDataVersionsApiResponse(typing.TypedDict):
    """sample
    ```
    {
        'brokers_login_config': '1',
        'security_master': '1',
    }
    """
    brokers_login_config: str
    security_master: str

class MainOptionsWsSessionDataApiResponse(typing.TypedDict):
    """sample
    ```
    {
        'market_timings': {
            'nse-fo': MainOptionsWsMarketTimingsApiResponse
        },
        'ac_details': {
            'in': MainOptionsWsAccountTypeApiResponse
        },
        'client_setting': '23'  # TODO change this to client_master_version -> master {server_version: int, client_version: int}
        'etoken': 'spW48ZXL0uFa497+iWFvnX3vLW8NoSEYc6nHVwPllXMhDtBMS0kiVwbudTfIT5jMBZ3M8vHy3T1OydgFEPBAmZFS1Po8UJ6ZGNeZklTHSFZ4hv49jQaHKLec6ax04jQC+0zkijO2rnft/JS/brFrQzJ7SpXznxnGJ6w8ClX4zoE/zwxFDb0kAkot86mOcJCkmDO6Ui11QmCteQ7JZVmvrPoEfHF424eAU9pp6MHuflZhtm26GM5/vN5zuTNfrcuRZ',
        'user_id': '622594',
        'api_key': 'u7IoXQbITjy5992_fSSIsg',
        'market_data': 'Gzipped pickled data'
        'versions': MainOptionsWsSessionDataVersionsApiResponse,

        # TODO send the master json version data and download if required from api_client_helper

        # Remove this
        'session_validity': 0,
        
    }
    """
    market_timings: dict[generic_types.Exchange, MainOptionsWsMarketTimingsApiResponse]
    ac_details: dict[generic_types.Country, MainOptionsWsAccountTypeApiResponse]
    user_id: generic_types.NumericString
    etoken: str
    api_key: str
    market_data: bytes
    versions: MainOptionsWsSessionDataVersionsApiResponse


class MainOptionsWsGeneralApiResponse(typing.TypedDict):
    """sample
    {
        'status': '1',
        'msg': 'success',
        'ws_msg_type': 'qapp_api_gateway_options_etoken_authorized',
        'session_data': MainOptionsWsSessionDataApiResponse
    }
    """
    status: ApiResponseStatus
    msg: str
    ws_msg_type: typing.Literal[
        'qapp_api_gateway_options_success_api_request',
        'qapp_api_gateway_options_failure_api_request',
        'qapp_api_gateway_options_invalid_route',
    ]
    session_data: MainOptionsWsSessionDataApiResponse


    



class MainOptionsWsApiHelperClientApiResponse(typing.TypedDict):
    """sample
    ```
    {
        'status': '1',
        'msg': str,
        'responses': [
            {}
        ],
        'custom_key': str,
        'routeKey': str,
        'ws_msg_type': 'qapp_api_gateway_options_success_api_request',
    }
    """
    status: ApiResponseStatus
    msg: str
    responses: list[execution_types.BrokerLoginDbData]
    custom_key: str
    routeKey: str
    ws_msg_type: typing.Literal[
        'qapp_api_gateway_options_success_api_request',
        'qapp_api_gateway_options_failure_api_request',
    ]


class BrokerOrderUpdateRawWsData(typing.TypedDict):
    """sample
    ```
    {
        "ac": "mstock,MA6232931",
        "b_orderid": "31822505096618",
        "e_orderid": "1600000149834342",
        "q_ref_id": 29,
        "qty_filled": 0,
        "qty": 75,
        "instrument": "NIFTY:15-May-25:c:25500",
        "bs": "b",
        "price": 1.1,
        "price_filled": 1.1,
        "b_usec_update": 1746778008000000,
        "product_type": "nrml",
        "order_status": "pending",
        "o_ctr": 2,
        "userid": 622594,
        "order_type": "limit",
        "q_usec": 1746777894829010,
        "stop_price": 0.0
    }
    """

    ac: str
    b_orderid: str
    e_orderid: str
    q_ref_id: int
    qty_filled: int
    qty: int
    instrument: str
    bs: typing.Literal['b', 's']
    price: float
    price_filled: float
    b_usec_update: int
    product_type: execution_types.BrokerOrderProductType
    order_status: execution_types.OrderStatus
    o_ctr: int
    userid: int
    order_type: execution_types.OrderTypes
    q_usec: int
    stop_price: float