# Built-in Modules
import time

from dataclasses import dataclass


# Local Modules
from quantsapp import (
    _enums as generic_enums,
    constants as generic_constants,
    exceptions as generic_exceptions,
)
from quantsapp._websocket import (
    OptionsMainWebsocket,
    _config as websocket_config,
)
from quantsapp._execution import (
    _enums as execution_enums,
    _models as execution_models,
    _types as execution_types,
)
from quantsapp._version import __version__ as qapp_package_version


# ----------------------------------------------------------------------------------------------------


@dataclass
class PlaceOrder:

    ws: OptionsMainWebsocket
    order: execution_models.PlaceOrder

    # ---------------------------------------------------------------------------

    def place_order(self) -> execution_types.PlaceOrdersResponse:
        """Get the Orders of specific Broker Client in the requested order"""

        parsed_orders = self._parse_order()

        return self._place_order(parsed_orders)

    # ---------------------------------------------------------------------------

    def _parse_order(self) -> execution_types.PlaceOrderApiPayload:
        """Transform the structure to final format"""

        parsed_order: execution_types.PlaceOrderApiPayload = {
            'accounts': { # type: ignore
                broker_ac.broker_client._api_str: broker_ac.lot_multiplier  # type: ignore - private variable
                for broker_ac in self.order.broker_accounts
            },
            'exchange': self.order.exchange.value,
            'product': self.order.product.value,
            'order_type': self.order.order_type.value,
            'validity': self.order.validity.value,
        }

        parsed_legs = []

        for leg in self.order.legs:
            _curr_parsed_leg: execution_types.PlaceOrderLegApiPayload = {
                'qty': leg.qty,
                'symbol': leg.instrument.symbol,
                'price': leg.price,
                'expiry': leg.instrument._api_expiry_str,  # type: ignore - private variable
                'buy_sell': leg.transaction_type.value, # type: ignore
            }

            if leg.instrument.instrument_type == generic_enums.InstrumentType.FUTURE:
                _curr_parsed_leg['segment'] = generic_enums.InstrumentType.FUTURE.value
            else:
                _curr_parsed_leg['segment'] = generic_enums.InstrumentType._InstrumentType__OPTIONS # type: ignore
                _curr_parsed_leg['opt_type'] = leg.instrument.instrument_type.value
                _curr_parsed_leg['strike'] = leg.instrument.strike
        
            if self.order.order_type == execution_enums.OrderType.STOP_LOSS_LIMIT:
                _curr_parsed_leg['stop_price'] = leg.stop_price

            parsed_legs.append(_curr_parsed_leg) # type: ignore


        parsed_order['legs'] = parsed_legs

        return parsed_order

    # ---------------------------------------------------------------------------

    def _place_order(self, orders_to_place: execution_types.PlaceOrderApiPayload) -> execution_types.PlaceOrdersResponse:
        """Invoke the API to get the Orders"""

        place_orders_resp: execution_types.PlaceOrderApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'place_order',
                'order': orders_to_place,
                'page_id': f"python_sdk_{qapp_package_version}",
                'ui_orderid': f"{generic_constants.API_KEY}_{int(time.time()*1000)}",
            },
        ) # type: ignore

        if place_orders_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersPlacingFailed(place_orders_resp['msg'])
    
        return {
            'success': not place_orders_resp['has_failed'],
            'ref_id': place_orders_resp['q_ref_id'],
        }

    # ---------------------------------------------------------------------------

    
