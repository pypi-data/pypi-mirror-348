# Built-in Modules
import typing

from dataclasses import dataclass


# Local Modules
from quantsapp._websocket import (
    OptionsMainWebsocket,
    _config as websocket_config,
)

from quantsapp._execution import (
    _models as execution_models,
    _types as execution_types,
)


# ----------------------------------------------------------------------------------------------------


@dataclass
class GetOrderLogs:

    ws: OptionsMainWebsocket
    payload: execution_models.GetOrderLogs

    # ---------------------------------------------------------------------------

    def get_logs(self) -> list[dict[str, typing.Any]]:  # TODO add detailed response
        """Get all logs related to a specific order"""

        api_log_data = self._get_api_data()

        return self._parse_data(api_log_data)

    # ---------------------------------------------------------------------------

    def _get_api_data(self) -> execution_types.OrderLogsListingApiResponseData:
        """Invoke the API to get the mapped ac details data"""

        return self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'get_order_api_log',
                'broker_clientid': self.payload.broker_client._api_str,  # type: ignore - private variable
                'q_usec': int(self.payload.q_usec.timestamp() * 1e6),  # Convert datetime to microseconds
                'instrument': self.payload.instrument._api_instr_str,  # type: ignore - private variable
            },
        ) # type: ignore

    # ---------------------------------------------------------------------------

    def _parse_data(self, api_log_data: execution_types.OrderLogsListingApiResponseData) -> list[dict[str, typing.Any]]:
        """Transform the structure to final format"""

        return api_log_data['order_apilog']