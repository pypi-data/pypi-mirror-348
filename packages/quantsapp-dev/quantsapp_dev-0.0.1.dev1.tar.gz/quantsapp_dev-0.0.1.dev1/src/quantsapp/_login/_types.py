# Built-in Modules
import typing


class LoginAPIResponse(typing.TypedDict):
    status: typing.Literal['0', '1']
    msg: typing.Optional[str]
    jwt_token: str