# Built-in Modules
from dataclasses import dataclass


# Local Modules
import quantsapp._master_data
from quantsapp import exceptions as generic_exceptions
from quantsapp._websocket import (
    _config as websocket_config,
    OptionsMainWebsocket,
)
from quantsapp._execution import (
    _models as execution_models,
    _types as execution_types,
    _cache as execution_cache,
)


# ----------------------------------------------------------------------------------------------------


@dataclass
class ModifyOrder:

    ws: OptionsMainWebsocket
    order: execution_models.ModifyOrder

    # ---------------------------------------------------------------------------

    def modify_order(self) -> bool:
        """Modify the existing order"""

        self._validate_data()

        
        modify_order_resp: execution_types.ModifyOrderApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'modify_order',
                'broker_client': self.order.broker_client._api_str,  # type: ignore - private variable
                'b_orderid': self.order.b_orderid,
                'e_orderid': self.order.e_orderid,
                'order': {
                    'qty': self.order.qty,
                    'price': self.order.price
                }
            },
        ) # type: ignore

        if modify_order_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersPlacingFailed(modify_order_resp['msg'])
    
        return True

    # ---------------------------------------------------------------------------

    def _validate_data(self) -> None:
        """validate the data which can't be done from the pydantic level(may be due to circular import Error)"""

        if not (_order_data := execution_cache.orders.get(self.order.broker_client, {}).get(f"{self.order.b_orderid}|{self.order.e_orderid}")):
            raise generic_exceptions.InvalidInputError('Broker Order Not found')

        _lot_size: int = quantsapp._master_data.MasterData.master_data['symbol_data'][_order_data['instrument'].symbol]['lot_size'][_order_data['instrument'].expiry]

        if self.order.qty % _lot_size != 0:
            raise generic_exceptions.InvalidInputError(f"Invalid Qty, should be multiple of {_lot_size} for {_order_data['instrument'].symbol!r}")
