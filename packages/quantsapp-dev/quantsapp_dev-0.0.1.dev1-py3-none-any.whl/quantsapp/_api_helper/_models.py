# Built-in Modules
import typing
import collections.abc


# Third-party Modules
from pydantic import BaseModel


# ----------------------------------------------------------------------------------------------------


class ApiRequest(BaseModel):
    api_request: typing.Any  # TODO change this to only allowed request
    callback: collections.abc.Callable[[typing.Any], typing.Any]
