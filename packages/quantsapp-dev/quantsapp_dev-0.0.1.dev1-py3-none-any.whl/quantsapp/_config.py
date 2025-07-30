# Built-in Modules
import re
import shutil
import pathlib


# Local Modules
from quantsapp._logger import qapp_logger
from quantsapp._utils import get_temp_storage_path
from quantsapp._version import __version__ as qapp_version


# -- Instrument Data ---------------------------------------------------------------------------------

# sample instr - 'NIFTY:15-May-25:x', 'NIFTY:15-May-25:c:25200'
API_INSTRUMENT_INSTR_REGEX_PATTERN: str = r'^(?P<symbol>.+?)(:(?P<expiry>\d{2}\-\w{3}-\d{2})(:(?P<instr_typ>[xcp])(:(?P<strike>.+))?)?)?$'
re_api_instr: re.Pattern[str] = re.compile(API_INSTRUMENT_INSTR_REGEX_PATTERN)

EXPIRY_FORMAT: str = '%d-%b-%y'


# -- Temp directory ----------------------------------------------------------------------------------

__tmp_storage_path = pathlib.Path(get_temp_storage_path())
__tmp_folder_name = f".quantsapp_tmp_{qapp_version}"

# Remove old SDK cache folders if found
for i in __tmp_storage_path.glob('*/'):
    if i.name.startswith('.quantsapp_tmp_') \
            and i.name != __tmp_folder_name:
        shutil.rmtree(i)
        qapp_logger.debug(f"Old sdk version cache folder removed ({i.name})")

# Create a new cache folder if not found
tmp_cache_folder_path = __tmp_storage_path.joinpath(__tmp_folder_name)
tmp_cache_folder_path.mkdir(parents=True, exist_ok=True)