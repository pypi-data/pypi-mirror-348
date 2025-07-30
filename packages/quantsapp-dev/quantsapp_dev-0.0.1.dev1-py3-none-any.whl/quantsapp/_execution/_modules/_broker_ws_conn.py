# Built-in Modules
import datetime as dt
from dataclasses import dataclass


# Local Modules
from quantsapp import exceptions as generic_exceptions
from quantsapp._websocket import (
    _config as websocket_config,
    OptionsMainWebsocket,
)
from quantsapp._execution import (
    _types as execution_types,
)
from quantsapp import (
    payload as generic_payload,
    constants as generic_constants,
)


# ----------------------------------------------------------------------------------------------------


@dataclass
class BrokerWsConnectionStatus:

    ws: OptionsMainWebsocket
    payload: generic_payload.GetBrokerWebsocketConnectionStatus

    # ---------------------------------------------------------------------------

    def get_status(self) -> ...:
        """Get Broker websocket connection status"""

        broker_ws_conn_status_api_resp: execution_types.BrokerWsConnStatusApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'get_broker_ws_conn_status',
                'broker_client': self.payload.broker_client._api_str,  # type: ignore - private variable
            },
        ) # type: ignore

        if broker_ws_conn_status_api_resp['status'] != '1':
            raise generic_exceptions.BrokerWsConnectionStatusFailed(broker_ws_conn_status_api_resp['msg'])

        return {
            'ts_ping': self.convert_update_sec_to_datetime(broker_ws_conn_status_api_resp['ts_ping']),
            'ts_msg': self.convert_update_sec_to_datetime(broker_ws_conn_status_api_resp['ts_msg']),
            'ts_conn': self.convert_update_sec_to_datetime(broker_ws_conn_status_api_resp['ts_conn']),
        }

    # ---------------------------------------------------------------------------

    def convert_update_sec_to_datetime(self, ts: int, tz: dt.timezone = generic_constants.DT_ZONE_IST) -> dt.datetime | None:

        if ts:
            return dt.datetime.fromtimestamp(
                timestamp=ts,
                tz=tz,
            )
        else:
            return None

# ----------------------------------------------------------------------------------------------------


@dataclass
class BrokerWsReConnect:

    ws: OptionsMainWebsocket
    payload: generic_payload.BrokerWebsocketReConnect

    # ---------------------------------------------------------------------------

    def reconnect(self) -> bool:
        """Force reconnect to Broker Websocket"""

        broker_ws_re_conn_api_resp: execution_types.BrokerWsReConnApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'broker_ws_connect',
                'broker_client': self.payload.broker_client._api_str,  # type: ignore - private variable
            },
        ) # type: ignore

        if broker_ws_re_conn_api_resp['status'] != '1':
            raise generic_exceptions.BrokerWsReConnectionFailed(broker_ws_re_conn_api_resp['msg'])

        return True
