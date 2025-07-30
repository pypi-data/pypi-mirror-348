# Built-in Modules
import os
import sys
import json
import uuid
import gzip
import typing
import base64
import pickle
import tempfile
import functools
import datetime as dt


# Local Modules
from quantsapp._logger import qapp_logger
from quantsapp import (
    _config as generic_config,
    exceptions as generic_exceptions,
)
from quantsapp._websocket import _models as websocket_models

# ----------------------------------------------------------------------------------------------------

# Auto reload, when required
_account_details: dict[typing.Literal['ac_data'], websocket_models.AccountDetails] = {}

# ----------------------------------------------------------------------------------------------------

class MarketTimings:

    dt_open: dt.datetime = None # type: ignore
    dt_close: dt.datetime = None # type: ignore
    is_open_today: bool = False

    # TODO add auto reload market timings data every 'n' minutes

    # ---------------------------------------------------------------------------

    @staticmethod
    def is_market_open() -> bool:
        """Return current status whether market open at time of func invoke"""

        if not MarketTimings.is_open_today:
            return False

        if not MarketTimings.dt_open \
                or not MarketTimings.dt_close:
            raise generic_exceptions.LoginNotInitiatedError('Initiate Login to check Market timings')  # TODO change the exception and its error

        return MarketTimings.dt_open <= dt.datetime.now(dt.UTC) <= MarketTimings.dt_close

    # ---------------------------------------------------------------------------

    @staticmethod
    def is_after_market() -> bool:
        """Return current status whether market open at time of func invoke"""

        if not MarketTimings.is_open_today:
            return True

        if not MarketTimings.dt_open \
                or not MarketTimings.dt_close:
            raise generic_exceptions.LoginNotInitiatedError('Initiate Login to check Market timings')  # TODO change the exception and its error

        return dt.datetime.now(dt.UTC) > MarketTimings.dt_close


# ----------------------------------------------------------------------------------------------------

def convert_str_to_datetime(date: str, format: str, timezone: dt.timezone = dt.UTC) -> dt.datetime:
    """Convert the date string based on specific format to the required timezone"""

    return dt.datetime.strptime(
        date,
        format,
    ).replace(
        tzinfo=timezone,
    )

# ----------------------------------------------------------------------------------------------------

@functools.lru_cache()
def get_mac_address() -> str:
    """Retreive the mac address of the connected network interface"""

    # Get the hardware address as a 48-bit positive integer
    mac_num = uuid.getnode()

    # 1. Convert the number to hex
    # 2. Pad it to 12 chars
    # 3. Convert it to a series of two char strings
    # 4. Join them with colons
    # 5. convert to uppercase
    return ':'.join(f"{b:02x}" for b in mac_num.to_bytes(6)).upper()

# ----------------------------------------------------------------------------------------------------

def get_int_or_float(value: str) -> int | float:
    """Parse string to int or float"""

    _float_value = float(value)
    return int(_float_value) if _float_value % 1 == 0 else _float_value

# ----------------------------------------------------------------------------------------------------

def gzip_decompress_response_data(data: str):
    """Base64 decode and Gzip deccompress the data"""

    return json.loads(
        gzip.decompress(
            base64.b64decode(data)
        )
    )

# ----------------------------------------------------------------------------------------------------

def get_local_file_cache_data(file_name: str) -> typing.Any:
    """Get the data from local cache file, if available"""

    file_path = generic_config.tmp_cache_folder_path / file_name

    match file_path.suffix:
        case '.pkl':
            with open(file_path, 'rb') as fp:
                return pickle.load(fp)
        case '.json':
            with open(file_path, 'r') as fp:
                return json.load(fp)
        case _:
            raise ValueError('Invalid File Type')
    

# ----------------------------------------------------------------------------------------------------

def put_local_file_cache_data(file_name: str, data: typing.Any, success_log_msg: typing.Optional[str] = None) -> None:
    """Push the data to local cache file"""

    file_path = generic_config.tmp_cache_folder_path / file_name

    match file_path.suffix:
        case '.pkl':
            with open(file_path, 'wb') as fp:
                return pickle.dump(obj=data, file=fp)
        case '.json':
            with open(file_path, 'w') as fp:
                return json.dump(obj=data, fp=fp)
        case _:
            raise ValueError('Invalid File Type')
    
    _msg = f"Data dumped to cache file = {file_path}"
    if success_log_msg:
        _msg += f" -> {success_log_msg}"
    qapp_logger.debug(_msg)

# ----------------------------------------------------------------------------------------------------

def get_quantsapp_ac_details() -> websocket_models.AccountDetails:
    """Return the details related to logged in Quantsapp Account"""

    if 'ac_data' not in _account_details:
        raise generic_exceptions.LoginNotInitiatedError('Initiate Login to get the Quantsapp account details')  # TODO change the exception and its error

    return _account_details['ac_data']

# ----------------------------------------------------------------------------------------------------

def get_temp_storage_path() -> str:
    """Return the persistant temp storage even on system reboot"""

    try:
        match sys.platform:

            # Linux OS
            case 'linux':

                # For AWS lambda (sample - "AWS_EXECUTION_ENV": "AWS_Lambda_python3.13")
                # on AWS lambda, there is no persistent temp storage, since it is a serverless
                # once the lambda session timeout (usally 15 min), then temp storage will be flushed out
                # Ref - https://docs.aws.amazon.com/lambda/latest/api/API_EphemeralStorage.html
                if os.environ.get('AWS_EXECUTION_ENV', '').startswith('AWS_Lambda'):
                    return '/tmp'
            
                # On linux os, the persistent tmp storage is not '/tmp'
                else:
                    return '/var/tmp'
            
            # Windows OS
            case 'win32' | 'cygwin':
                return tempfile.gettempdir()
            
            # Mac OS
            case 'darwin':
                return '/var/folders'

            # Default provide the temp non-persistent folder path
            case _:
                return tempfile.gettempdir()
    
    except Exception:
        return tempfile.gettempdir()

