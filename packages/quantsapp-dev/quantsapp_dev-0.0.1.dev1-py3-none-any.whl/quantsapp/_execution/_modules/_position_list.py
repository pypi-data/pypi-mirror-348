# Built-in Modules
import json
import gzip
import base64
import typing

from dataclasses import dataclass


# Local Modules
from quantsapp import exceptions as generic_exceptions
from quantsapp._websocket import (
    OptionsMainWebsocket,
    _config as websocket_config,
)
from quantsapp._execution import (
    _enums as execution_enums,
    _models as execution_models,
    _types as execution_types,
)


# ----------------------------------------------------------------------------------------------------

# TODO add caching for positions too

@dataclass
class GetPositions:

    ws: OptionsMainWebsocket
    payload: execution_models.GetPositions

    # ---------------------------------------------------------------------------

    def get_positions(self) -> dict[execution_models.BrokerClient, list[execution_types.PositionsAccountwiseListingData]]:
        """Get the positions of specific Broker Client in the requested order"""

        raw_positions_data = self._get_data()

        if not raw_positions_data:
            return {}

        # Send order records one by one
        return GetPositions.parse_data(raw_positions_data)


    # ---------------------------------------------------------------------------

    def _get_data(self) -> dict[str, list[execution_types.PositionsAccountwiseApiResponseData]]:
        """Invoke the API to get the positions combined"""

        get_positions_resp: execution_types.GetPositionsApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'get_positions_account_wise',
                'broker_clientids': [
                    broker_client._api_str  # type: ignore - private variable
                    for broker_client in self.payload.broker_clients
                ]
            },
        ) # type: ignore

        if get_positions_resp['status'] != '1':
            raise generic_exceptions.BrokerPositionsListingFailed(get_positions_resp['msg'])

        return self._get_positions_data(get_positions_resp)

    # ---------------------------------------------------------------------------

    def _get_positions_data(self, get_orders_resp: execution_types.GetPositionsApiResponse) -> dict[str, list[execution_types.PositionsAccountwiseApiResponseData]]:
        """Decompress the data if compressed"""

        positions_data = get_orders_resp['positions'] # type: ignore

        if get_orders_resp['gzip']:
            positions_data: dict[str, list[execution_types.PositionsAccountwiseApiResponseData]] = json.loads(
                gzip.decompress(
                    data=base64.b64decode(positions_data) # type: ignore
                )
            )
        
        return positions_data

    # ---------------------------------------------------------------------------

    @staticmethod
    def parse_data(position_data: dict[str, list[execution_types.PositionsAccountwiseApiResponseData]]) -> dict[execution_models.BrokerClient, list[execution_types.PositionsAccountwiseListingData]]:
        """Transform the structure to final format"""

        return {
            execution_models.BrokerClient.from_api_str(_broker_client): [
                {
                    'instrument': _position_data['instrument'],
                    'product_type': execution_enums.OrderProductType(_position_data['product_type']),
                    'buy_qty': _position_data['buy_qty'],
                    'buy_t_value': _position_data['buy_t_value'],
                    'sell_qty': _position_data['sell_qty'],
                    'sell_t_value': _position_data['sell_t_value'],
                    'p_ctr': _position_data['p_ctr'],
                }
                for _position_data in _positions_data
            ]
            for _broker_client, _positions_data in position_data.items()
        }


    # ---------------------------------------------------------------------------

    

# ----------------------------------------------------------------------------------------------------


@dataclass
class GetPositionsCombined:

    ws: OptionsMainWebsocket
    payload: execution_models.GetPositions

    # ---------------------------------------------------------------------------

    def get_positions(self) -> typing.Iterator[execution_types.PositionsCombinedListingData]:
        """Get the positions of specific Broker Client in the requested order"""


        self.__pagination_key: typing.Any = None

        while True:

            raw_positions_data = self._get_data()

            # Send order records one by one
            yield from GetPositionsCombined.parse_data(raw_positions_data)

            # If no more records found, then exit the loop
            if not self.__pagination_key:
                break

    # ---------------------------------------------------------------------------

    def _get_data(self) -> list[execution_types.PositionsCombinedApiResponseData]:
        """Invoke the API to get the positions combined"""

        get_positions_resp: execution_types.GetPositionsApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'get_positions',
                'broker_clientids': [
                    broker_client._api_str  # type: ignore - private variable
                    for broker_client in self.payload.broker_clients
                ]
            },
        ) # type: ignore

        if get_positions_resp['status'] != '1':
            raise generic_exceptions.BrokerPositionsListingFailed(get_positions_resp['msg'])

        return self._get_positions_data(get_positions_resp)

    # ---------------------------------------------------------------------------

    def _get_positions_data(self, get_orders_resp: execution_types.GetPositionsApiResponse) -> list[execution_types.PositionsCombinedApiResponseData]:
        """Decompress the data if compressed"""

        positions_data = get_orders_resp['positions'] # type: ignore

        if get_orders_resp['gzip']:
            positions_data: list[execution_types.PositionsCombinedApiResponseData] = json.loads(
                gzip.decompress(
                    data=base64.b64decode(positions_data) # type: ignore
                )
            )
        
        return positions_data

    # ---------------------------------------------------------------------------

    @staticmethod
    def parse_data(position_data: list[execution_types.PositionsCombinedApiResponseData]) -> typing.Iterator[execution_types.PositionsCombinedListingData]:
        """Transform the structure to final format"""

        for data in position_data:
            print(f"{data = }")
            yield {
                'instrument': data['instrument'],
                'product_type': execution_enums.OrderProductType(data['product_type']),
                'buy_qty': data['buy_qty'],
                'buy_t_value': data['buy_t_value'],
                'sell_qty': data['sell_qty'],
                'sell_t_value': data['sell_t_value'],
            }


    # ---------------------------------------------------------------------------

    
