# Built-in Modules
import json
import time
import typing
import secrets
import threading
import datetime as dt


# Third-party Modules
import websocket


# Local Modules
from quantsapp._logger import qapp_logger
from quantsapp._version import __version__ as qapp_package_version
from quantsapp import (
    _enums as generic_enums,
    _utils as generic_utils,
)
from quantsapp._websocket import (
    QappWebsocket,
    _config as websocket_config,
    _constants as websocket_constants,
    _types as websocket_types,
    _models as websocket_models,
)

# ----------------------------------------------------------------------------------------------------


class OptionsMainWebsocket(QappWebsocket):

    _last_active_at: int = 0

    # ---------------------------------------------------------------------------

    def __init__(
            self,
            url: str,
            ws_conn_cond: threading.Condition,
        ) -> None:

        QappWebsocket.__init__(
            self,
            url=url,
            ws_conn_cond=ws_conn_cond,
            thread_name=self.__class__.__name__,
        )

        # Instance variables
        self._url = url
        self._ws_conn_cond = ws_conn_cond

        # For the api invocation usages
        self._responses: dict[str, typing.Any] = {}

        # Storing Websocket Session data
        self.ws_session_data: websocket_types.MainOptionsWsSessionDataApiResponse = None # type: ignore

        # To ensure active ws connection while calling api
        self._ws_conn_open = False 

    # ---------------------------------------------------------------------------

    def _initate_ws_conn(self) -> None:
        """Start making connection"""

        QappWebsocket.__init__(
            self,
            url=self._url,
            ws_conn_cond=self._ws_conn_cond,
            thread_name=self.__class__.__name__,
        )

    # ---------------------------------------------------------------------------

    def _ensure_active_ws_conn(self) -> None:
        """Make sure the ws connection is open"""

        # Websocket is already active
        if self._ws_conn_open:
            return None

        qapp_logger.debug(f"{self.__class__.__name__} connection is not active, reconnecting again.")

        # Start connection
        self._initate_ws_conn()

        # Wait till the connection happens properly
        with self._ws_conn_cond:
            self.start()
            self._ws_conn_cond.wait()

        # Reset value to active again
        self._ws_conn_open = True

    # ---------------------------------------------------------------------------

    # TODO check if this method required or not
    def on_reconnect(self, ws: websocket.WebSocket) -> None:
        qapp_logger.debug(f"AutoReconnect {self.__class__.__name__} -> {ws = }")

    # ---------------------------------------------------------------------------

    def on_message(self, ws: websocket.WebSocket, message: str | bytes) -> None:

        if isinstance(message, str):
            self._process_string_msg(json.loads(message))

        elif isinstance(message, bytes):
            # TODO code for handling this bytes data (Mostly notification data)
            ...

    # ---------------------------------------------------------------------------

    def on_error(self, ws: websocket.WebSocket, error: Exception) -> None:
        qapp_logger.error(f"Error on {self.__class__.__name__}")
        qapp_logger.error(f"{ws = }")
        qapp_logger.error(f"{error = }")

    # ---------------------------------------------------------------------------

    def on_pong(self, ws: websocket.WebSocket, message: str) -> None:
        OptionsMainWebsocket._last_active_at = int(time.time())

    # ---------------------------------------------------------------------------

    def on_close(self, ws: websocket.WebSocket, close_status_code: int, close_msg: str) -> None:
        self._ws_conn_open = False
        qapp_logger.debug(f"{self.__class__.__name__} closed -> {close_status_code = }, {close_msg = }")

    # ---------------------------------------------------------------------------

    @staticmethod
    def is_ws_active() -> bool:
        """Check the ws connection status with last pong time"""

        # Not even a single pong recevied
        if not OptionsMainWebsocket._last_active_at:
            return False

        # time interval between current time and last pong time less than the max pong skip time, then declare ws active
        if (int(time.time()) - OptionsMainWebsocket._last_active_at) < websocket_config.DEFAULT_PING_INTERVAL_SEC * websocket_config.MAX_PONG_SKIP_FOR_ACTIVE_STATUS:
            return True

        return False

    # ---------------------------------------------------------------------------

    def invoke_api(self, payload: dict[str, typing.Any]) -> dict[str, typing.Any]:
        """Invoke the api via sending payload msgs to Websocket"""

        # create a unique msg id for reference
        _msg_id = f"api_{qapp_package_version}_{secrets.token_hex(8)}"

        # Update the payload with other required details
        payload |= {
            'custom_key': _msg_id,
            'platform': 'api',
            'app': 'o',
            'country': 'in',
            'version': qapp_package_version,
            'sub_platform': 'uat',
        }


        with (_request_cond := threading.Condition()):

            self._responses[_msg_id] = {
                '_condition': _request_cond,
            }

            qapp_logger.debug(f"Lambda invocation request -> {payload}")

            self._ensure_active_ws_conn()

            _tic = time.perf_counter()
            # TODO Check for thread safetly on sending messages simultaneously
            self.ws.send(
                data=json.dumps(payload),
            )

            # self.ws.on_close  # TODO check why this added and

            _request_cond.wait()
            _toc = time.perf_counter()

        _api_response = self._responses.pop(_msg_id)

        # Remove the Threading condition, before sending to source
        del _api_response['_condition']

        qapp_logger.debug(f"Lambda invocation response ({_toc-_tic:0.4f}sec) -> {_api_response.keys()}")

        return _api_response

    # ---------------------------------------------------------------------------

    def _process_string_msg(self, ws_msg: ...) -> None:
        """Check for the api response and push it to the response dic and notify the condition"""

        if ws_msg.get('ws_msg_type') == 'qapp_api_gateway_options_etoken_authorized':
            self._process_conn_open_response(ws_msg)

            # Notify the other thread that the ws connected successfully and got the Master data also 
            # and ask them to proceed further
            with self.ws_conn_cond:
                self.ws_conn_cond.notify()
            
            # Set the last active conn status time
            OptionsMainWebsocket._last_active_at = int(time.time())

            qapp_logger.debug(f"{self.__class__.__name__} connected!!!")

            self._ws_conn_open = True

        # If there is no custom_msg, then it is not an lambda invocation reponse
        if 'custom_key' not in ws_msg:
            return None

        if ws_msg['custom_key'] in self._responses:
            self._process_lambda_invocation_resp_msg(ws_msg)

    # ---------------------------------------------------------------------------

    def _process_conn_open_response(self, ws_open_response: websocket_types.MainOptionsWsGeneralApiResponse) -> None:
        """Parse and Push the required data to memory to be used by other process"""

        qapp_logger.debug(f"{self.__class__.__name__} connection open resp={ws_open_response}")

        # Set the session data
        self.ws_session_data = ws_open_response['session_data']

        # Process the session data
        self._process_account_details()
        self._process_market_timings_data()

    # ---------------------------------------------------------------------------

    def _process_account_details(self) -> None:
        """Parse and Push the required account details to memory to be used by other process"""

        try:
            # Set account details for reference
            generic_utils._account_details['ac_data'] = websocket_models.AccountDetails(  # type: ignore - Private member reference
                API_KEY=self.ws_session_data['api_key'],
                USER_ID=self.ws_session_data['user_id'],
                AC_TYPE=generic_enums.AccountTypes(self.ws_session_data['ac_details']['in']['ac_type']),
            )
        
        except Exception as er:
            import traceback
            print(traceback.format_exc())
            raise er

        # Set etoken for reference
        websocket_constants.MAIN_OPTIONS_WS_ETOKEN = self.ws_session_data['etoken']

        # Set other versions for reference
        websocket_config.WebsocketVersions.SECURITY_MASTER = self.ws_session_data['versions']['security_master']
        websocket_config.WebsocketVersions.BROKERS_LOGIN_CONFIG = int(self.ws_session_data['versions']['brokers_login_config'])

    # ---------------------------------------------------------------------------

    def _process_market_timings_data(self) -> None:
        """Parse and Push the market timings data to memory to be used by other process"""

        nse_fno_market_timings: websocket_types.MainOptionsWsMarketTimingsApiResponse = self.ws_session_data['market_timings'][generic_enums.Exchange.NSE_FNO.value.lower()] # type: ignore

        generic_utils.MarketTimings.is_open_today = nse_fno_market_timings['is_open_today']

        if nse_fno_market_timings['is_open_today']:
            generic_utils.MarketTimings.dt_open = dt.datetime.fromisoformat(nse_fno_market_timings['open'])  # type: ignore
            generic_utils.MarketTimings.dt_close = dt.datetime.fromisoformat(nse_fno_market_timings['close'])  # type: ignore

    # ---------------------------------------------------------------------------

    def _process_lambda_invocation_resp_msg(self, ws_msg: ...) -> None:
        """Check for the api response and push it to the response dic and notify the condition"""

        with self._responses[ws_msg['custom_key']]['_condition']:
            # Update the recevied response for the request custom_key
            self._responses[ws_msg['custom_key']] |= ws_msg
            self._responses[ws_msg['custom_key']]['_condition'].notify()

        
