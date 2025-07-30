# Contains all generic types which can be used by all modules

import typing
import datetime as dt


NumericString = typing.NewType('NumericString', str)
"""sample:-
```
'1'
'1.1'
"""

DateTime = typing.NewType('DateTime', str)
"""sample:-
```
'02-May-25 23:59:59'
"""

DateTimeIso = typing.NewType('DateTimeIso', str)
"""sample:-
```
'2025-05-10T00:18:45.951177+05:30'
"""

AccountType = typing.Literal[
    'free',
    'pro',
    'pro_plus',
]

Country = typing.Literal[
    'in',
]

Exchange = typing.Literal[
    'nse-fo',
]


# -- Master Data -------------------------------------------------------------------------------------


class MasterDataApiResponse(typing.TypedDict):
    """sample
    ```
    {
        'master_data': 'Base64 Gzipped Pickle data',
        'last_updated_on':'2025-05-13T06:50:06.106209+05:30',
        'pickle_protocol': PICKLE_PROTOCOL,
        'master_version': '14-May-25'
    }
    """
    master_data: str
    last_update_on: str
    pickle_protocol: int
    master_version: str


class MasterExpiryData(typing.TypedDict):
    """sample
    ```
    {
        "weekly": [
            "09112023"  # Instead of expiry in string it will be in datatime
        ],
        "all": [
            "09112023"
        ],
        "monthly": [
            "30112023"
        ]
    }
    """
    weekly: list[dt.datetime]
    all: list[dt.datetime]
    monthly: list[dt.datetime]

class MasterSymbolData(typing.TypedDict):
    """sample
    ```
    {
        "lot_size": {
            datetime.datetime(2025, 5, 29, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800), 'IST')): 50,
        },
        "expiry": MasterExpiryData,
        "strikes": {
            "07122023": [
                "16150"
            ]
        }
    }
    """
    lot_size: dict[dt.datetime, int]
    expiry: MasterExpiryData
    strikes: dict[dt.datetime, list[int | float]]


class MasterScripData(typing.TypedDict):
    """sample
    ```
    {
        "instruments_to_scrip": {
            "NIFTY:25012024|x": "55319"
        },
        "scrip_to_instruments": {
            "55319": "NIFTY:25012024|x"
        }
    }
    """
    instruments_to_scrip: dict[str, NumericString]
    scrip_to_instruments: dict[NumericString, str]


class MasterData(typing.TypedDict):
    """sample
    ```
    {
        "symbol_data": {
            'NIFTY': MasterSymbolData,
        },
        "scrip_data": MasterScripData
    }
    """
    symbol_data: dict[str, MasterSymbolData]
    scrip_data: MasterScripData