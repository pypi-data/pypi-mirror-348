# Built-in Modules
import sys
import typing
import atexit
import secrets
import threading
import contextlib
import datetime as dt
import collections.abc

from dataclasses import dataclass
from urllib.parse import urlparse, urlencode


# Local Modules
from quantsapp._version import __version__ as qapp_package_version
from quantsapp._logger import qapp_logger
from quantsapp._master_data import MasterData

from quantsapp import _utils as generic_utils


from quantsapp._websocket import (
    OptionsMainWebsocket,
    OptionsBrokerOrderUpdatesWebsocket,
)

from quantsapp._execution._modules._broker_login_data import BrokerLoginData
from quantsapp._execution import (
    _models as execution_models,
    _types as execution_types,
    _cache as execution_cache,
)
from quantsapp._execution._modules import (
    AddBroker,
    DeleteBroker,
    GetBrokers,
    GetMappedBrokers,

    OrderBookUpdate,

    BrokerWsConnectionStatus,
    BrokerWsReConnect,

    GetOrders,
    PlaceOrder,
    ModifyOrder,
    GetOrderLogs,
    CancelOrders,
    CancelAllOrders,

    GetPositions,
    GetPositionsCombined,
)

from quantsapp._api_helper import ApiHelper

# ----------------------------------------------------------------------------------------------------

@dataclass
class Execution:

    session_id: str
    order_updates_callback: typing.Optional[collections.abc.Callable[[execution_models.BrokerOrderUpdateWsData], typing.Any]] = None

    # ---------------------------------------------------------------------------

    def __post_init__(self) -> None:

        self.ws_responses: dict[str, typing.Any] = {}

        self.__connect_main_ws()

        self.__connect_broker_order_updates_ws()

        self.__preprocess()

    # ---------------------------------------------------------------------------

    def __connect_main_ws(self) -> None:
        """Connect to Options Websocket to get api data"""

        # TODO change this to config
        query_params = {
            'ws_msg_type': 'api_client_login',
            'api_jwt': self.session_id,
            'portal': 'api',
            'sub_portal': 'python_sdk',
            'python_version': sys.version,
            'version': qapp_package_version,
            'country': 'in',
            # 'master_data': '1',
            'uid': generic_utils.get_mac_address(),
            'ref_id': f"{dt.datetime.now(dt.UTC):%d%m%Y}-{secrets.token_urlsafe(16)}",
        }

        url = 'wss://server-uat.quantsapp.com'

        url += ('&' if urlparse(url).query else '?') + urlencode(query_params)


        _ws_conn_condition = threading.Condition()
        self.ws_main = OptionsMainWebsocket(
            url=url,
            ws_conn_cond=_ws_conn_condition,
        )

        with _ws_conn_condition:
            self.ws_main.start()
            _ws_conn_condition.wait()

        # On exiting the python code, close the main ws
        # TODO change the logic of handling the ws connections
        atexit.register(self.__close_ws)

    # ---------------------------------------------------------------------------

    def __connect_broker_order_updates_ws(self) -> None:
        """Connect to Broker Order updates websocket to get Realtime order updates"""

        if not self.__should_connect_broker_order_updates_ws():
            return None

        query_params = {
            'ws_msg_type': 'etoken',
            'etoken': self.ws_main.ws_session_data['etoken'],
            'portal': 'api',
            'sub_portal': 'python_sdk',
            'python_version': sys.version,
            'version': qapp_package_version,
            'country': 'in',
            'uid': generic_utils.get_mac_address(),
            'ref_id': f"{dt.datetime.now(dt.UTC):%d%m%Y}-{secrets.token_urlsafe(16)}",
        }

        # url = 'wss://server.quantsapp.com/order-updates'
        # url = 'ws://13.235.128.71:5130/order-updates'
        url = 'wss://server-uat.quantsapp.com/order-updates'

        url += ('&' if urlparse(url).query else '?') + urlencode(query_params)


        _ws_conn_condition = threading.Condition()
        self.ws_broker_orders = OptionsBrokerOrderUpdatesWebsocket(
            url=url,
            ws_conn_cond=_ws_conn_condition,
            order_updates_callback=self.order_updates_callback, # type: ignore
        )

        with _ws_conn_condition:
            self.ws_broker_orders.start()
            _ws_conn_condition.wait()

    # ---------------------------------------------------------------------------

    def __should_connect_broker_order_updates_ws(self) -> bool:
        """Check whether to Connect Broker Order updates websocket to get Realtime order updates"""
        
        if not self.order_updates_callback:
            qapp_logger.debug(f"Broker Update Callback func not passed, so don't need to connect to {OptionsBrokerOrderUpdatesWebsocket.__name__}")
            return False

        if not OptionsBrokerOrderUpdatesWebsocket.should_connect_broker_order_updates_ws():
            qapp_logger.debug(f"Trading not allowed, so don't need to connect to {OptionsBrokerOrderUpdatesWebsocket.__name__}")
            return False

        return True

    # ---------------------------------------------------------------------------

    def __close_ws(self) -> None:

        _close_ws = ('ws_main', 'ws_broker_orders')

        for ws_name in _close_ws:
            with contextlib.suppress(Exception):
                if hasattr(self, ws_name):
                    getattr(self, ws_name).close_ws()

    # ---------------------------------------------------------------------------

    def __preprocess(self) -> None:
        """Do preprocess after connected to websocket"""

        self._api_helper = ApiHelper(ws=self.ws_main)

        # Master data should be processed first, 
        # as it is the based for all other preprocessing
        self.__update_master_data()

        self.__update_get_available_brokers()

        # Invoke the api helper with consolidated requests
        self._api_helper.invoke_consolidated_api()

        # # Do other preprocessing
        # for name in sorted(dir(self)):
        #     if name.startswith(f"_{self.__class__.__name__}__preprocess_"):
        #         method = getattr(self, name)
        #         method()

    # ---------------------------------------------------------------------------

    def __update_master_data(self) -> None:
        """Download and update master data to memory"""

        # Get the master data and push it to memory
        MasterData().update_master_data(
            api_helper=self._api_helper,
        )

    # ---------------------------------------------------------------------------

    def __update_get_available_brokers(self) -> None:
        """Download and update the broker login data to memory"""

        BrokerLoginData().update_broker_login_data(
            api_helper=self._api_helper,
        )

    # ---------------------------------------------------------------------------

    def __preprocess_get_mapped_brokers(self) -> None: # type: ignore
        """Get the mapped brokers"""

        # TODO get the client_settings version from Bridge lambda 
        # Do one single call to get all data like master, client settings etc... and parse it
        # create a separate logic to consolidate the requests

        execution_cache.mapped_brokers = GetMappedBrokers(
            ws=self.ws_main,
            payload=execution_models.ListMappedBrokers(
                revalidate_token=True,
                from_cache=False,
            ),
        ).list_brokers()

    # ---------------------------------------------------------------------------

    # def __preprocess_get_orders(self) -> None: # type: ignore
    #     """Get orders of all mapped valid brokers"""

    #     # TODO check with sir, since this version no. is not available

    #     for _broker, _broker_data in execution_cache.mapped_brokers['brokers'].items():
            
    #         # # Don't consider the broker accounts which is not validated
    #         # if not _broker_data['valid']:
    #         #     continue

    #         # Orders are getting pushed to cache from inside GetOrders().update_orders()
    #         GetOrders(
    #             ws=self.ws_main,
    #             payload=generic_payload.ListOrders(
    #                 broker_client=execution_models.BrokerClient(
    #                     broker=_broker,
    #                     client_id=_broker_data['client_id'],
    #                 ),
    #             ),
    #         ).update_orders()

    # ---------------------------------------------------------------------------

    def list_available_brokers(self, payload: typing.Optional[execution_models.ListAvailableBrokers] = None) -> execution_types.ListAvailableBrokersResponse:
        """list the brokers based on login mode (ui only & code based)"""

        return GetBrokers(
            ws=self.ws_main,
            payload=payload or execution_models.ListAvailableBrokers(),
        ).list_available_brokers()

    # ---------------------------------------------------------------------------

    def list_mapped_brokers(self, payload: typing.Optional[execution_models.ListMappedBrokers] = None) -> execution_types.ListBrokersResponse:
        """list the brokers based on login mode (ui only & code based)"""

        return GetMappedBrokers(
            ws=self.ws_main,
            payload=payload or execution_models.ListMappedBrokers(),
        ).list_brokers()

    # ---------------------------------------------------------------------------

    # TODO remove this later as not needed.
    # def check_client_id(self, broker: execution_enums.Broker, client_id: str) -> execution_types.ClientCheckResponse:
    #     """
    #         Check whether the client exists or not

    #         And whether the user has access to it or not
    #     """

    #     return ClientInfo(
    #         ws=self.ws_main,
    #         broker=broker,
    #         client_id=client_id,
    #     ).check_client()

    # # ---------------------------------------------------------------------------

    def add_broker(self, payload: execution_models.AddBroker) -> bool:
        """
            Check whether the client exists or not

            And whether the user has access to it or not
        """

        return AddBroker(
            ws=self.ws_main,
            payload=payload,
        ).login()

    # ---------------------------------------------------------------------------

    def delete_broker(self, payload: execution_models.DeleteBroker) -> bool:
        """Delete the broker account from Quantsapp, if exists"""

        return DeleteBroker(
            ws=self.ws_main,
            payload=payload
        ).delete()

    # ---------------------------------------------------------------------------

    # filter  # TODO add a genreic filter
    def get_orders(self, payload: execution_models.ListOrders) -> typing.Iterator[execution_types.OrderListingData]:
        """Retreive the orders"""

        return GetOrders(
            ws=self.ws_main,
            payload=payload,
        ).get_orders()

    # ---------------------------------------------------------------------------

    def place_order(self, payload: execution_models.PlaceOrder) -> execution_types.PlaceOrdersResponse:
        """Place orders"""

        return PlaceOrder(
            ws=self.ws_main,
            order=payload,
        ).place_order()

    # ---------------------------------------------------------------------------

    def modify_order(self, order: execution_models.ModifyOrder) -> bool:
        """Modify existing order"""

        return ModifyOrder(
            ws=self.ws_main,
            order=order,
        ).modify_order()

    # ---------------------------------------------------------------------------

    def cancel_orders(self, payload: execution_models.CancelOrders) -> execution_types.CancelOrdersResponse:
        """Cancel specific orders from specific broker accounts"""

        return CancelOrders(
            ws=self.ws_main,
            payload=payload,
        ).cancel_orders()

    # ---------------------------------------------------------------------------

    def cancel_all_orders(self, payload: execution_models.CancelAllOrders) -> execution_types.CancelOrdersResponse:
        """Cancel specific orders from specific broker accounts"""

        return CancelAllOrders(
            ws=self.ws_main,
            payload=payload,
        ).cancel_all_orders()

    # ---------------------------------------------------------------------------

    def get_positions(self, payload: execution_models.GetPositions) -> dict[execution_models.BrokerClient, list[execution_types.PositionsAccountwiseListingData]]:
        """Get positions combinely from the specific broker accounts"""

        return GetPositions(
            ws=self.ws_main,
            payload=payload,
        ).get_positions()

    # ---------------------------------------------------------------------------

    def get_positions_combined(self, payload: execution_models.GetPositions) -> typing.Iterator[execution_types.PositionsCombinedListingData]:
        """Get positions combinely from the specific broker accounts"""

        return GetPositionsCombined(
            ws=self.ws_main,
            payload=payload,
        ).get_positions()

    # ---------------------------------------------------------------------------

    def get_order_api_log(self, payload: execution_models.GetOrderLogs) -> ...:
        """Get specific order logs from broker end"""

        return GetOrderLogs(
            ws=self.ws_main,
            payload=payload,
        ).get_logs()

    # ---------------------------------------------------------------------------

    def get_broker_websocket_conn_status(self, payload: execution_models.GetBrokerWebsocketConnectionStatus) -> ...:
        """Get Broker websocket connection status"""

        return BrokerWsConnectionStatus(
            ws=self.ws_main,
            payload=payload,
        ).get_status()

    # ---------------------------------------------------------------------------

    def broker_websocket_reconnect(self, payload: execution_models.BrokerWebsocketReConnect) -> bool:
        """Force reconnect to broker ws"""

        return BrokerWsReConnect(
            ws=self.ws_main,
            payload=payload,
        ).reconnect()

    # ---------------------------------------------------------------------------

    def update_order_book(self, payload: execution_models.UpdateOrderBook) -> ...:
        """Resync the order book data """

        return OrderBookUpdate(
            ws=self.ws_main,
            payload=payload,
        ).update()
