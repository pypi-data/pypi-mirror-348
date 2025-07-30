# Built-in Modules
import typing
import datetime as dt


# Third-party Modules
from pydantic import (
    BaseModel,

    PositiveInt,
    PositiveFloat,
    ConfigDict,

    Field,
    computed_field,
    model_validator,

    StrictStr,
)


# Local Modules
from quantsapp import (
    _config as generic_config,
    _enums as generic_enums,
    _utils as generic_utils,
    constants as generic_constants,
)
import quantsapp._master_data
from quantsapp._execution import (
    _config as execution_config,
)
from quantsapp.exceptions import InvalidInputError


# ----------------------------------------------------------------------------------------------------


class Instrument(BaseModel):

    # Variables
    symbol: StrictStr
    expiry: dt.datetime
    instrument_type: generic_enums.InstrumentType
    strike: typing.Optional[PositiveInt | PositiveFloat] = Field(
        default=None,
        gt=0,
        validate_default=True,
    )

    # ---------------------------------------------------------------------------

    @model_validator(mode='after')
    def validate_instr(self: typing.Self) -> typing.Self:

        # Validation - Symbol
        if not quantsapp._master_data.MasterData.is_valid_symbol(self.symbol):
            raise InvalidInputError(f"Invalid symbol = {self.symbol}")
    
        # Validation - Expiry
        self.expiry = self.expiry.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=generic_constants.DT_ZONE_IST,
        )
        if not quantsapp._master_data.MasterData.is_valid_expiry(symbol=self.symbol, expiry=self.expiry):
            raise InvalidInputError(f"Invalid Expiry for symbol ({self.symbol}) = {self.expiry:%d-%b-%Y}. Available expiries are {[f'{_exp:%d-%b-%Y}' for _exp in quantsapp._master_data.MasterData.get_all_expiries(self.symbol)]}")

        # Validation - Strike
        if self.instrument_type != generic_enums.InstrumentType.FUTURE:
            if not quantsapp._master_data.MasterData.is_valid_strike(symbol=self.symbol, expiry=self.expiry, strike=self.strike):
                raise InvalidInputError(f"Invalid Strike for symbol ({self.symbol}), Expiry ({self.expiry:%d-%b-%Y}) = {self.strike}. Available strikes are {quantsapp._master_data.MasterData.get_all_strikes(self.symbol, self.expiry)}")

        # To avoid modifying the values once set
        self.__class__.model_config = ConfigDict(
            frozen=True,
        )

        return self

    # ---------------------------------------------------------------------------

    @classmethod
    def from_api_str(cls, instr: str) -> typing.Self:
        """Convert API String representation of instr to Instance Model
            'NIFTY:15-May-25:x'
            'NIFTY:15-May-25:c:25200'
        """

        _tmp = generic_config.re_api_instr.search(instr).groupdict()

        return cls(
            symbol=_tmp['symbol'],
            expiry=dt.datetime.strptime(_tmp['expiry'], generic_config.EXPIRY_FORMAT),
            instrument_type=generic_enums.InstrumentType(_tmp['instr_typ']),
            strike=generic_utils.get_int_or_float(_tmp['strike']) if _tmp['strike'] else None,
        )

    # ---------------------------------------------------------------------------

    @computed_field
    @property
    def _api_instr_str(self) -> str:
        """String representation to be used on API level conversions
            'NIFTY:15-May-25:x'
            'NIFTY:15-May-25:c:25200'
        """

        _instr = self.symbol

        _instr += f":{self.expiry:%d-%b-%y}"

        if self.instrument_type == generic_enums.InstrumentType.FUTURE:
            _instr += ':x'
        else:
            _instr += f":{self.instrument_type.value}:{self.strike}"

        return _instr
    

    # ---------------------------------------------------------------------------

    @computed_field
    @property
    def _api_expiry_str(self) -> str:
        """String representation of expiry to be used on API level conversions
            '%d-%b-%y' - '15-May-25'
        """

        return self.expiry.strftime(execution_config.BROKER_ORDER_PLACEMENT_DATE_FORMAT)    


# ----------------------------------------------------------------------------------------------------
