# Built-in Modules
import typing

from dataclasses import dataclass


# Local Modules
from quantsapp._websocket import (
    OptionsMainWebsocket,
    _types as websocket_types,
)

from quantsapp._api_helper import (
    _config as api_helper_config,
    _models as api_helper_models,
)

# ----------------------------------------------------------------------------------------------------

@dataclass
class ApiHelper:

    ws: OptionsMainWebsocket

    # ---------------------------------------------------------------------------

    def __post_init__(self) -> None:
        """Initiate empty list of requests to proceed invocation"""

        self._requests: list[api_helper_models.ApiRequest] = []

    # ---------------------------------------------------------------------------

    def add_request(self, request: api_helper_models.ApiRequest) -> None:
        """Add request to get invoked"""

        self._requests.append(request)

    # ---------------------------------------------------------------------------

    def invoke_single_api(self, request: dict[str, typing.Any]) -> dict[str, typing.Any]:
        """Invoke the api helper with single request to get data"""

        # invoke api
        db_resp: websocket_types.MainOptionsWsApiHelperClientApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': api_helper_config.WS_ACTION_KEY,
                'requests': [
                    request
                ],
            },
        ) # type: ignore

        if db_resp['status'] != '1':
            raise ValueError('TODO handle this properly')

        return db_resp['responses'][0]

    # ---------------------------------------------------------------------------

    def invoke_consolidated_api(self) -> None:
        """Invoke the api helper with the added requests to get data"""

        if not self._requests:
            return None

        # invoke api
        db_resp: websocket_types.MainOptionsWsApiHelperClientApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': api_helper_config.WS_ACTION_KEY,
                'requests': [
                    _request.api_request
                    for _request in self._requests
                ],
            },
        ) # type: ignore

        if db_resp['status'] != '1':
            raise ValueError('TODO handle this properly')

        # Parse the responses recived on API
        self._parse_responses(db_resp['responses'])

    # ---------------------------------------------------------------------------

    def _parse_responses(self, responses: ...) -> ...:
        """Invoke the callback function to the respective responses to parse it"""

        for _request, _response in zip(self._requests, responses):
            _request.callback(_response)