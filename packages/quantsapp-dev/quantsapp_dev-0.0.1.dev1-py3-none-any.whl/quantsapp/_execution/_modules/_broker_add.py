# Built-in Modules
from dataclasses import dataclass


# Local Modules
from quantsapp import exceptions as generic_exceptions
from quantsapp._websocket import (
    _config as websocket_config,
    OptionsMainWebsocket,
)
from quantsapp._execution import (
    _models as execution_models,
    _types as execution_types,
)
from quantsapp._execution._modules._broker_login_data import (
    BrokerLoginData,
    broker_display_names,
)


# ----------------------------------------------------------------------------------------------------


@dataclass
class AddBroker:

    ws: OptionsMainWebsocket
    payload: execution_models.AddBroker

    # ---------------------------------------------------------------------------

    def login(self) -> bool:
        """Login to Broker Account"""

        self.broker_login_metadata = BrokerLoginData.broker_login_data

        self._validate_request()

        login_api_resp = self._login()

        if login_api_resp['status'] != '1':
            raise generic_exceptions.BrokerLoginFailed(login_api_resp['msg'])

        return True

    # ---------------------------------------------------------------------------

    def _validate_request(self) -> None:
        """Validate the request params to proceeding login process"""

        self._validate_active_broker()

    # ---------------------------------------------------------------------------

    def _validate_active_broker(self) -> None:
        """Check whether the broker is active"""

        if self.payload.broker.value not in self.broker_login_metadata:
            raise generic_exceptions.BrokerLoginNotAllowed(f"Broker ({broker_display_names[self.payload.broker]}) not allowed in API Login")

        if self.broker_login_metadata[self.payload.broker.value]['ui_login_only']:
            raise generic_exceptions.BrokerLoginNotAllowed(f"Broker ({broker_display_names[self.payload.broker]}) not allowed in API Login. Please use the Web/Mobile app to add the broker")

    # ---------------------------------------------------------------------------

    def _login(self) -> execution_types.BrokerLoginApiResponse:
        """Invoke the api to do broker login"""

        return self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_LOGIN,
                'mode': 'add_account',
                'broker': self.payload.broker.value,
                'delete_previous_users': self.payload.delete_previous_users,
                'update_owner': self.payload.update_owner,
                'login_type': self.broker_login_metadata[self.payload.broker.value]['login_types'][0],  # TODO check this to to make it more generic
                'credentials': self.payload.login_credentials.model_dump(),
            },
        ) # type: ignore

    # ---------------------------------------------------------------------------
