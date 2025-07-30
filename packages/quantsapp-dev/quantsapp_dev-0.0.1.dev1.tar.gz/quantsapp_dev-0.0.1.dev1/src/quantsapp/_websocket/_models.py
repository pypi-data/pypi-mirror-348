# Third-party Modules
from pydantic import BaseModel


# Local Modules
from quantsapp import _enums as generic_enums


# ----------------------------------------------------------------------------------------------------


class AccountDetails(BaseModel, frozen=True):
    API_KEY: str
    USER_ID: str
    AC_TYPE: generic_enums.AccountTypes
