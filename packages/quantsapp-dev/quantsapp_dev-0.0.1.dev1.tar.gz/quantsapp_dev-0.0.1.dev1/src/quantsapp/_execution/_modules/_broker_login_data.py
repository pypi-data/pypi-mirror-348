# Built-in Modules
import contextlib


# Third-party Modules


# Local Modules
from quantsapp._logger import qapp_logger
from quantsapp._execution import (
    _enums as execution_enums,
    _types as execution_types,
)
from quantsapp._websocket import _config as websocket_config
from quantsapp._api_helper import (
    ApiHelper,
    _models as api_helper_models,
)
from quantsapp import _utils as generic_utils

# ----------------------------------------------------------------------------------------------------

class BrokerLoginData:

    broker_login_data: execution_types.BrokerLoginDbData = None # type: ignore
    _cache_file_name = 'broker_login.pkl'

    # ---------------------------------------------------------------------------

    def update_broker_login_data(self, api_helper: ApiHelper) -> None:
        """asd"""

        self.api_helper = api_helper

        if _tmp_broker_login_data_resp :=  self._get_broker_login_data():
            BrokerLoginData.broker_login_data = _tmp_broker_login_data_resp

    # ---------------------------------------------------------------------------

    def _get_broker_login_data(self) -> execution_types.BrokerLoginDbData | None:
        """asd"""

        # First try to get data from local file
        # if file not exists or the version mismatch with version got from Main Options WS,
        # then download the new data from api and push it to cache
        with contextlib.suppress(Exception):
            return self._get_broker_login_data_from_local_file()

        self._add_get_broker_login_data_request_to_api_helper()

    # ---------------------------------------------------------------------------

    def _get_broker_login_data_from_local_file(self) -> execution_types.BrokerLoginDbData:
        """Get the Broker Login data from the local cache file"""

        _cache_broker_login_data = generic_utils.get_local_file_cache_data(self._cache_file_name)
        
        if _cache_broker_login_data['version'] != websocket_config.WebsocketVersions.BROKERS_LOGIN_CONFIG:
            qapp_logger.debug(f"BrokerLoginData version mismatch (file_version={_cache_broker_login_data['version']}, ws_version={websocket_config.WebsocketVersions.BROKERS_LOGIN_CONFIG})")
            raise ReferenceError('Version mismatch!')

        qapp_logger.debug(f"BrokerLoginData with version ({_cache_broker_login_data['version']}) returned from cache folder")

        return _cache_broker_login_data['data']

    # ---------------------------------------------------------------------------

    def _add_get_broker_login_data_request_to_api_helper(self) -> None:
        """
            Add the request to api_helper data retreival,
            which will consolidate all requests and send a single request to optimize the query
        """

        self.api_helper.add_request(
            request=api_helper_models.ApiRequest(
                api_request={
                    'mode': 'execution',
                    'sub_mode': 'get_broker_login_data',
                    'params': {
                        'version': websocket_config.WebsocketVersions.BROKERS_LOGIN_CONFIG,
                    },
                },
                callback=BrokerLoginData.parse_broker_login_data_from_api_response,
            ),
        )

    # ---------------------------------------------------------------------------

    @staticmethod
    def parse_broker_login_data_from_api_response(broker_login_data_api_response: execution_types.BrokerLoginDbDataApiResponse) -> None:
        """Parse the master data recieved on API response"""

        _tmp_broker_login_data = broker_login_data_api_response['broker_login_data']

        # Gzip if required
        if isinstance(_tmp_broker_login_data['data'], str):
            _tmp_broker_login_data['data'] = generic_utils.gzip_decompress_response_data(_tmp_broker_login_data['data'])

        # TODO parse the raw data to enums whatever required

        # Saving local for caching purposes
        generic_utils.put_local_file_cache_data(
            file_name=BrokerLoginData._cache_file_name,
            data={
                'data': _tmp_broker_login_data['data'],
                'version': _tmp_broker_login_data['version'],
            },
            success_log_msg=f"BrokerLoginData downloaded and pushed to cache file with version ({_tmp_broker_login_data['version']})",
        )

        BrokerLoginData.broker_login_data = _tmp_broker_login_data['data']

# ----------------------------------------------------------------------------------------------------

# Auto reload, when required
broker_display_names: dict[execution_enums.Broker, str] = {}

def create_broker_display_names(data: execution_types.BrokerLoginDbData) -> None:
    """
        Create a DisplayName dict for each broker based on the data from DB
        Set the created enum on the enums file so that it can be used for further references
    """

    global broker_display_names

    # TODO create own metaclass for enum to do operations like in, etc...
    _available_enum_brokers = execution_enums.Broker._value2member_map_

    broker_display_names = {
        execution_enums.Broker(broker_name): broker_data['name']
        for broker_name, broker_data in data.items()
        if broker_name in _available_enum_brokers

    }
