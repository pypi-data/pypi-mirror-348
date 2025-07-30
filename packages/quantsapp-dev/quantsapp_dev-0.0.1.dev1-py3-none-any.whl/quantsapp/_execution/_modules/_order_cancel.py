# Built-in Modules
from dataclasses import dataclass


# Local Modules
from quantsapp import (
    exceptions as generic_exceptions,
)
from quantsapp._websocket import (
    _config as websocket_config,
    OptionsMainWebsocket,
)
from quantsapp._execution import (
    _models as execution_models,
    _types as execution_types,
)


# ----------------------------------------------------------------------------------------------------


@dataclass
class CancelOrders:

    ws: OptionsMainWebsocket
    payload: execution_models.CancelOrders

    # ---------------------------------------------------------------------------

    def cancel_orders(self) -> execution_types.CancelOrdersResponse:
        """Cancel pending orders"""
        
        cancel_orders_resp: execution_types.CancelOrdersApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'cancel_orders',
                'order': {
                    order.broker_client._api_str: [  # type: ignore - private variable
                        {
                            'b_orderid': order_id.b_orderid,
                            'e_orderid': order_id.e_orderid,
                        }
                        for order_id in order.order_ids
                    ]
                    for order in self.payload.orders
                }
            },
        ) # type: ignore

        if cancel_orders_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersCancelFailed(cancel_orders_resp['msg'])
    
        return {
            'success': not cancel_orders_resp['has_failed'],
            'ref_id': cancel_orders_resp['q_ref_id_c'],
        }

    
# ----------------------------------------------------------------------------------------------------


@dataclass
class CancelAllOrders:

    ws: OptionsMainWebsocket
    payload: execution_models.CancelAllOrders

    # ---------------------------------------------------------------------------

    def cancel_all_orders(self) -> execution_types.CancelOrdersResponse:
        """Cancel all pending orders belongs to specific broker account"""
        
        cancel_all_orders_resp: execution_types.CancelOrdersApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'cancel_orders',
                'cancel_all': True,
                'broker_client': self.payload.broker_client._api_str,  # type: ignore - private variable
            },
        ) # type: ignore

        if cancel_all_orders_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersCancelFailed(cancel_all_orders_resp['msg'])
    
        return {
            'success': cancel_all_orders_resp['has_failed'],
            'ref_id': cancel_all_orders_resp['q_ref_id_c'],
        }

    # ---------------------------------------------------------------------------

  