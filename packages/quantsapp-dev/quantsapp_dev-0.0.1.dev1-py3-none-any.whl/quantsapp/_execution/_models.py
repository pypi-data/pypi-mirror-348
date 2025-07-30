# Built-in Modules
import typing
import datetime as dt


# Third-party Modules
from pydantic import (
    Field,
    BaseModel,
    StrictStr,
    PositiveInt,
    PositiveFloat,
    model_validator,
    computed_field,
)


# Local Modules
import quantsapp._master_data
from quantsapp.exceptions import InvalidInputError
from quantsapp._execution import (
    _config as execution_config,
    _enums as execution_enums,
)
from quantsapp import (
    _enums as generic_enums,
    _models as generic_models,
)


# ----------------------------------------------------------------------------------------------------

class BrokerClient(BaseModel, frozen=True):

    broker: execution_enums.Broker
    client_id: StrictStr

    # ---------------------------------------------------------------------------

    @computed_field
    @property
    def _api_str(self) -> str:
        """String representation to be used on API level conversions
            'fivpaisa,x123'
        """

        return f"{self.broker},{self.client_id}"
    
    # ---------------------------------------------------------------------------

    @classmethod
    def from_api_str(cls, broker_client: str) -> typing.Self:
        """Convert API String representation of broker client to Instance Model
            'mstock,MA6232931'
        """

        _broker, client_id = broker_client.split(',')

        return cls(
            broker=execution_enums.Broker(_broker),
            client_id=client_id,
        )


# ----------------------------------------------------------------------------------------------------


class DhanBrokerLoginCredentials(BaseModel, frozen=True):
    access_token: str

class ChoiceBrokerLoginCredentials(BaseModel, frozen=True):
    mobile: str  # TODO add validation of mobile no. if required, Discuss with Shubham sir
    client_access_token: str

class AddBroker(BaseModel, frozen=True):
    broker: execution_enums.Broker
    login_credentials: DhanBrokerLoginCredentials | ChoiceBrokerLoginCredentials
    delete_previous_users: bool = Field(default=False)
    update_owner: bool = Field(default=False)

    # ---------------------------------------------------------------------------

    @model_validator(mode='after')
    def validate_login_credentials(self: typing.Self) -> typing.Self:

        match self.broker:
            case execution_enums.Broker.DHAN:
                if not isinstance(self.login_credentials, DhanBrokerLoginCredentials):
                    raise InvalidInputError(f"Invalid login credentials for {self.broker.value} broker, pls use 'quantaspp.payload.DhanBrokerLoginCredentials'")
            case execution_enums.Broker.CHOICE:
                if not isinstance(self.login_credentials, ChoiceBrokerLoginCredentials):
                    raise InvalidInputError(f"Invalid login credentials for {self.broker.value} broker, pls use 'quantaspp.payload.ChoiceBrokerLoginCredentials'")
            case _:
                raise InvalidInputError(f"Invalid Broker for 'access_token' login!")

        return self


class DeleteBroker(BaseModel, frozen=True):
    broker_client: BrokerClient


class ListAvailableBrokers(BaseModel, frozen=True):
    name_type: typing.Literal['enum', 'str'] = Field(
        default=execution_config.DEFAULT_LIST_AVAILABLE_BROKER_NAME_TYPE,
    )

class ListMappedBrokers(BaseModel, frozen=True):
    revalidate_token: bool = Field(default=False)
    from_cache: bool = Field(default=True)


class PlaceOrderBrokerAccounts(BaseModel, frozen=True):
    broker_client: BrokerClient
    lot_multiplier: PositiveInt = Field(gt=0, default=1)



class PlaceOrderLeg(BaseModel, frozen=True):
    qty: PositiveInt = Field(gt=0)
    price: PositiveFloat = Field(
        ge=0,
        default=0,  # For market order don't need to pass it
    )
    instrument: generic_models.Instrument
    transaction_type: execution_enums.OrderTransactionType

    # Only present for stop loss limit order
    stop_price: typing.Optional[PositiveFloat] = Field(
        ge=0,
        default=None,
    )

    # ---------------------------------------------------------------------------

    @model_validator(mode='before')
    @classmethod
    def validate_place_order_leg(cls, data: typing.Any) -> typing.Any:

        _lot_size: PositiveInt = quantsapp._master_data.MasterData.master_data['symbol_data'][data['instrument'].symbol]['lot_size'][data['instrument'].expiry]

        if data['qty'] % _lot_size != 0:
            raise InvalidInputError(f"Invalid Qty, should be multiple of {_lot_size} for {data['instrument'].symbol!r}")

        return data


class PlaceOrder(BaseModel, frozen=True):
    broker_accounts: list[PlaceOrderBrokerAccounts]
    exchange: generic_enums.Exchange
    product: execution_enums.OrderProductType
    order_type: execution_enums.OrderType
    validity: execution_enums.OrderValidity
    legs: list[PlaceOrderLeg]

    # ---------------------------------------------------------------------------

    @model_validator(mode='after')
    def validate_stop_loss_limit_price_on_all_legs(self: typing.Self) -> typing.Self:

        for leg in self.legs:
            if (self.order_type == execution_enums.OrderType.STOP_LOSS_LIMIT):
                if not leg.stop_price:
                    raise InvalidInputError(f"stop_price should be for Stop Loss Limit Order")
                if leg.price <= leg.stop_price:
                    raise InvalidInputError(f"price({leg.price}) should be less than stop_price({leg.stop_price}) for Stop Loss Limit Order")

        return self


class ModifyOrder(BaseModel, frozen=True):
    broker_client: BrokerClient
    b_orderid: str
    e_orderid: str
    qty: PositiveInt = Field(gt=0)
    price: PositiveFloat


class ListOrders(BaseModel, frozen=True):
    broker_client: BrokerClient
    ascending: bool = Field(default=False)
    from_cache: bool = Field(default=True)


class CancelOrderIds(BaseModel, frozen=True):
    b_orderid: str
    e_orderid: str

class CancelIndividualBrokerOrder(BaseModel, frozen=True):
    broker_client: BrokerClient
    order_ids: list[CancelOrderIds]

class CancelOrders(BaseModel, frozen=True):
    orders: list[CancelIndividualBrokerOrder]

class CancelAllOrders(BaseModel, frozen=True):
    broker_client: BrokerClient


class GetOrderLogs(BaseModel, frozen=True):
    broker_client: BrokerClient
    instrument: generic_models.Instrument
    q_usec: dt.datetime


class GetBrokerWebsocketConnectionStatus(BaseModel, frozen=True):
    broker_client: BrokerClient

class BrokerWebsocketReConnect(BaseModel, frozen=True):
    broker_client: BrokerClient

class UpdateOrderBook(BaseModel, frozen=True):
    broker_client: BrokerClient
    update_on: typing.Literal['orders', 'positions']


class GetPositions(BaseModel, frozen=True):
    broker_clients: list[BrokerClient]


class BrokerOrderUpdateWsData(BaseModel, frozen=True):
    broker_client: BrokerClient
    b_orderid: str
    e_orderid: str
    q_ref_id: int
    qty_filled: int
    qty: int
    instrument: generic_models.Instrument
    buy_sell: execution_enums.OrderTransactionType
    price: float = Field(ge=0)
    price_filled: float = Field(ge=0)
    b_usec_update: dt.datetime
    product_type: execution_enums.OrderProductType
    order_status: execution_enums.OrderStatus
    o_ctr: int
    userid: str
    order_type: execution_enums.OrderType
    q_usec: dt.datetime
    stop_price: typing.Optional[float] = Field(
        ge=0,
        description='Only available for Stop Loss Limit Order type'
    )
