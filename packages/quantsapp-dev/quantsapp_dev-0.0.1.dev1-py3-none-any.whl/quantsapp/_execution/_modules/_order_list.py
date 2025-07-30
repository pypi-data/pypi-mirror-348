# Built-in Modules
import json
import gzip
import base64
import typing
import contextlib

from dataclasses import dataclass


# Local Modules
from quantsapp._logger import qapp_logger
from quantsapp import (
    _models as generic_models,
    exceptions as generic_exceptions,
    _utils as generic_utils,
)
from quantsapp._websocket import (
    _config as websocket_config,
    OptionsMainWebsocket,
)
from quantsapp._execution import (
    _enums as execution_enums,
    _models as execution_models,
    _types as execution_types,
    _cache as execution_cache,
    _utils as execution_utils,
)


# ----------------------------------------------------------------------------------------------------


@dataclass
class GetOrders:

    ws: OptionsMainWebsocket
    payload: execution_models.ListOrders

    _cache_file_name: typing.ClassVar[str] = 'broker_orders.pkl'

    # ---------------------------------------------------------------------------

    def get_orders(self) -> typing.Iterator[execution_types.OrderListingData]:
        """Get the Orders of specific Broker Client in the requested order"""

        _is_cache_data = True

        # If caching not required or first time call, update orders form DB
        if (self.payload.from_cache is False) \
                or (self.payload.broker_client not in execution_cache.orders):
            self._update_orders()
            _is_cache_data = False

        if _is_cache_data:
            qapp_logger.debug('Sending cache order list data')

        # Send order records one by one
        yield from self._parse_record_to_client(execution_cache.orders[self.payload.broker_client])

    # ---------------------------------------------------------------------------

    def _update_orders(self) -> None:
        """Update the Orders of specific Broker Client from either local cache or api"""

        if self.payload.from_cache is True:
            # First try to get data from local file
            # if file not exists then download the new data from api and push it to cache
            with contextlib.suppress(Exception):
                execution_cache.orders = self._get_data_from_local_file()
                return None

        # Get it from api
        self._get_data_from_api()

    # ---------------------------------------------------------------------------

    def _get_data_from_local_file(self) -> dict[execution_models.BrokerClient, list[execution_types.OrderListingData]]:
        """Get the Mapped Brokers data from the local cache file"""

        _cache_broker_orders_data = generic_utils.get_local_file_cache_data(self.__class__._cache_file_name)

        qapp_logger.debug(f"Broker Orders returned from cache folder")

        return _cache_broker_orders_data

    # ---------------------------------------------------------------------------

    def _get_data_from_api(self) -> None:
        """Get the Orders of specific Broker Client from api"""


        self.__pagination_key: typing.Any = None

        while True:

            # Get the existing orders
            _tmp_orders = execution_cache.orders.setdefault(self.payload.broker_client, {})
            
            # Get the new orders
            raw_orders_data = self._get_api_data()

            # merge the new orders
            _tmp_orders |= GetOrders.parse_data_new(  # TODO change the name from 'parse_data_new' to 'parse_data' later
                order_data=raw_orders_data,
            )

            # If no more records found, then exit the loop
            if not self.__pagination_key:
                break

        # Saving local for caching purposes
        self.save_cache_data(execution_cache.orders)

        qapp_logger.debug(f"Orders updated for {self.payload.broker_client} from api")

    # ---------------------------------------------------------------------------

    def _get_api_data(self) -> list[execution_types.OrderListingApiResponseData]:
        """Invoke the API to get the Orders"""

        get_orders_resp: execution_types.GetOrdersAccountWiseApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'get_order_status',
                'sub_mode': 'account',
                'broker_clientid': [self.payload.broker_client._api_str],  # Only one account selection allowed at a time  # type: ignore
                'pagination_key': self.__pagination_key,
                'has_pagination': False,  # To get all data without pagination
            },
        ) # type: ignore

        if get_orders_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersListingFailed(get_orders_resp['msg'])

        # If more records avaialble, then set pagination key to get more records if required
        # if 'has_pagination' is set to False, there won't be any pagination, but still keep it for fail safe
        self.__pagination_key = get_orders_resp.get('pagination_key')

        return self._get_decompressed_orders_data(get_orders_resp)

    # ---------------------------------------------------------------------------

    def _get_decompressed_orders_data(self, get_orders_resp: execution_types.GetOrdersAccountWiseApiResponse) -> list[execution_types.OrderListingApiResponseData]:
        """Decompress the data if compressed"""

        orders_data = get_orders_resp['orders'] # type: ignore

        if get_orders_resp['gzip']:
            orders_data: list[execution_types.OrderListingApiResponseData] = json.loads(
                gzip.decompress(
                    data=base64.b64decode(orders_data) # type: ignore
                )
            )
        
        return orders_data

    # ---------------------------------------------------------------------------

    @staticmethod
    def parse_data_new(order_data: list[execution_types.OrderListingApiResponseData]) -> dict[str, execution_types.OrderListingData]:
        """Transform the structure to final format"""

        parsed_broker_data: dict[str, execution_types.OrderListingData] = {}

        for data in order_data:
            _tmp_order_ref_internal_id = f"{data['b_orderid']}|{data.get('e_orderid')}"

            if (_tmp_order_ref_internal_id not in parsed_broker_data) \
                    or (data.get('o_ctr', 0) >= parsed_broker_data[_tmp_order_ref_internal_id]['o_ctr']):  # only update if o_ctr counter is more than the previous one
                
                # TODO change this dict to pydantic model (if required)
                parsed_broker_data[_tmp_order_ref_internal_id] = {
                    'broker_client': execution_models.BrokerClient.from_api_str(data['broker_client']),
                    'b_orderid': data['b_orderid'],
                    'qty': data['qty'],
                    'price': data['price'],
                    'userid': data.get('userid', ''),
                    'instrument': generic_models.Instrument.from_api_str(data['instrument']),
                    'e_orderid': str(data.get('e_orderid', '')),
                    'o_ctr': data.get('o_ctr', 0),
                    'qty_filled': data.get('qty_filled', 0),
                    'stop_price': data.get('stop_price', 0),
                    'buy_sell': execution_enums.OrderTransactionType(data['buy_sell']),
                    'order_type': execution_enums.OrderType(data['order_type']),
                    'product_type': execution_enums.OrderProductType(data['product_type']),
                    'order_status': execution_enums.OrderStatus(data['order_status']),
                    'q_usec': execution_utils.convert_update_sec_to_datetime(data['q_usec']),
                    'b_usec_update': execution_utils.convert_update_sec_to_datetime(data['b_usec_update']),
                }

        return parsed_broker_data

    # ---------------------------------------------------------------------------

    def _parse_record_to_client(self, data: dict[str, execution_types.OrderListingData]) -> list[execution_types.OrderListingData]:
        """Transform the internal data to client data"""

        # Consider only the values, not the internal reference id
        _tmp = data.values()

        # Sort the records based on payload requested order
        _tmp = sorted(
            _tmp,
            key=lambda item: item['b_usec_update'],
            reverse=not self.payload.ascending,
        )

        return _tmp

    # ---------------------------------------------------------------------------

    @staticmethod
    def save_cache_data(data: dict[execution_models.BrokerClient, dict[str, execution_types.OrderListingData]]) -> None:
        """saving the orders data to local cache file"""

        generic_utils.put_local_file_cache_data(
            file_name=GetOrders._cache_file_name,
            data=data,
            success_log_msg='BrokerOrders pushed to cache file',
        )