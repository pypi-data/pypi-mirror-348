from quantsapp._execution import (
    _models as execution_models,
    _types as execution_types,
)

mapped_brokers: execution_types.ListBrokersResponse = None  # type: ignore
 
orders: dict[execution_models.BrokerClient, dict[str, execution_types.OrderListingData]] = {}