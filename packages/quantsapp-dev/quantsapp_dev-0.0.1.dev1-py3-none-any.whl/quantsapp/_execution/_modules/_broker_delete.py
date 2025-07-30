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


# ----------------------------------------------------------------------------------------------------


@dataclass
class DeleteBroker:

    ws: OptionsMainWebsocket
    payload: execution_models.DeleteBroker

    # ---------------------------------------------------------------------------

    def delete(self) -> bool:
        """Delete the Broker Account from Quantsapp, if exists"""

        delete_api_resp: execution_types.BrokerDeleteApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_LOGIN,
                'mode': 'delete_account',
                'broker': self.payload.broker_client.broker.value,
                'client_id': self.payload.broker_client.client_id,
            },
        ) # type: ignore

        if delete_api_resp['status'] != '1':
            raise generic_exceptions.BrokerDeletionFailed(delete_api_resp['msg'])

        return True