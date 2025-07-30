# Built-in Modules
import json
import gzip
import base64

from dataclasses import dataclass


# Local Modules
from quantsapp import (
    exceptions as generic_exceptions,  # TODO move all execeptions to specific folder
    payload as generic_payload,
)
from quantsapp._websocket import (
    _config as websocket_config,
    OptionsMainWebsocket,
)
from quantsapp._execution import (
    _types as execution_types,
)

from quantsapp._execution._modules._order_list import GetOrders
from quantsapp._execution._modules._position_list import GetPositionsCombined


# ----------------------------------------------------------------------------------------------------


@dataclass
class OrderBookUpdate:

    ws: OptionsMainWebsocket
    payload: generic_payload.UpdateOrderBook

    # ---------------------------------------------------------------------------

    def update(self) -> ...:
        """Get the Orders of specific Broker Client in the requested order"""

        update_order_book_data = self._get_api_data()

        # Send order records one by one
        return self._parse_data(update_order_book_data)

    # ---------------------------------------------------------------------------

    def _get_api_data(self) -> execution_types.UpdateOrderBookApiResponse:
        """Invoke the API to update the Order Book"""

        update_order_book_resp: execution_types.UpdateOrderBookApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'update_orderbook',
                'broker_clientid': [self.payload.broker_client._api_str],  # type: ignore - private variable
                'screen': self.payload.update_on,
            },
        ) # type: ignore

        if update_order_book_resp['status'] != '1':
            raise generic_exceptions.BrokerOrderBookUpdateFailed(update_order_book_resp['msg'])

        return update_order_book_resp

    # ---------------------------------------------------------------------------

    def _parse_data(self, order_book_update_data: execution_types.UpdateOrderBookApiResponse) -> ...:
        """Transform the structure to final format"""

        _final_data = {
            'trade_msg': order_book_update_data['trade_msg'],
            'trade_status': order_book_update_data['trade_status'],
            'positions_msg': order_book_update_data['positions_msg'],
            'positions_status': order_book_update_data['positions_status'],
        }

        # Process Orders data
        if self.payload.update_on == 'orders':
            orders_data = order_book_update_data['orders_response']['orders'] # type: ignore
            if order_book_update_data['orders_response']['gzip']:
                orders_data: list[execution_types.OrderListingApiResponseData] = json.loads(
                    gzip.decompress(
                        data=base64.b64decode(orders_data) # type: ignore
                    )
                )
            _final_data['orders_response'] = GetOrders.parse_data( # type: ignore
                order_data=orders_data,
                ascending=True,
            )
        
        # Process Positions data
        elif self.payload.update_on == 'positions':
            positions_data = order_book_update_data['positions_response']['positions'] # type: ignore
            if order_book_update_data['positions_response']['gzip']:
                positions_data: list[execution_types.PositionsCombinedApiResponseData] = json.loads(
                    gzip.decompress(
                        data=base64.b64decode(positions_data) # type: ignore
                    )
                )
            _final_data['positions_response'] = list( # type: ignore
                GetPositionsCombined.parse_data(
                    position_data=positions_data,
                )
            )

        return _final_data


    # ---------------------------------------------------------------------------

    
