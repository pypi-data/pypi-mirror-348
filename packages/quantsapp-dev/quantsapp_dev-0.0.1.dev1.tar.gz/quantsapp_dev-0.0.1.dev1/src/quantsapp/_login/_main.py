# Built-in Modules
import sys
import hmac
import typing
import datetime as dt

from dataclasses import dataclass


# Third-party Modules
import requests


# Local Modules
import quantsapp.exceptions as exceptions

from quantsapp._logger import qapp_logger
from quantsapp import constants as generic_constants
from quantsapp._login import (
    _config as login_config,
    _types as login_types,
)
from quantsapp._version import __version__ as qapp_package_version


# ----------------------------------------------------------------------------------------------------


@dataclass
class Login:
    """Login and get the session_id for further communication"""

    api_key: str
    secret_key: str

    # ---------------------------------------------------------------------------

    def login(self) -> str:

        try:
            _sign = self._get_signature()

            try:
                resp = self._call_api(_sign)
            except Exception as err:
                raise exceptions.APIConnectionError(f"API Connection Issue -> {err}")

            if resp['status'] != '1':
                # raise exceptions.InvalidLoginCredentials('Invalid Login Credentials')
                raise exceptions.InvalidLoginCredentials(resp.get('msg') or  'Invalid Login Credentials')

            return resp['jwt_token']
    
        except Exception:
            raise exceptions.APIConnectionError('Error on Login API')

    # ---------------------------------------------------------------------------

    def _call_api_tmp(self, signature: str) -> login_types.LoginAPIResponse:
        """Invoke the API to Login"""

        # TODO remove this before live

        return {
            'status': '1',
            'msg': 'success',
            'jwt_token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDcwMzU3NzUsIm5iZiI6MTc0Njc3NjU3NSwiaWF0IjoxNzQ2Nzc2NTc1LCJpc3MiOiJxYXBwX2NsaWVudF9saWJfbG9naW4iLCJhdWQiOiJxYXBwX2Jyb2tlcl9weXRob25fY2xpZW50X2xpYnJhcnlfbG9naW4iLCJqdGkiOiJmZTBjYWFiNCIsInFhcHAiOnsiZXRva2VuIjoic3BXNDhaWEwwdUZhNDk3JTJCaVdGdm5YM3ZMVzhOb1NFWWM2bkhWd1BsbFhNaER0Qk1TMGtpVndidWRUZklUNWpNQlozTTh2SHkzVDFPeWRnRkVQQkFtWkZTMVBvOFVKNlpHTmVaa2xUSFNGWjdnYiUyQnU1WiUyQmJnTExRUlNmMTQ1WDd2MHpraWpPMnJuZnQlMkZKUyUyRmJyRnJRelAwbGUlMkZqRWxnNXBiSHh4R1plWVhHMVNOcUY3WEdmJTJCUCUyQktNU3hzdlNyUHZmTGJPbjg3WjEydnQlMkZmbzlJcmlUYm9FZkhGNDI0ZUFVOXBwNk1IdWZsWmh0bTI2R001JTJGdk41enVUTmZyY3VSWiJ9fQ.sl3QV7IIeY0gldss4aLRWT_RVZYQtHl-s5zJE8CAmX1y9uiOErfkUnKbPyJNSGdZU06mk2xVEkgF-MT-3tU9_CRhM3mOCq6jieDFPewTzXyIPKmWTVY6kwWVlPFqKIuWoZLgn4J0ZFkn57qXUC4rSiTr-fMNrpN_Zq07ix2p1R7ngPzaxWA_iY1ZtbicfjhQBxOrjaywf6hXWoHE22t7NECa1uQYpz2D2P8Opw4ERB7bfF7tfyCZFf3rHC-I8WEVrsrJC3Wz58F4Ehko86jW3X1XNK4yDN_PiAFq1zExtduBtBUOP_so8laBLYKa2W2Fqc93XIwHg2l-2y34n364A0pWkMRV8g-_Jb02cirapASoE0ednmjCrOPs3e47ly-M4315SlnCR2nFkaNvbjd7PHijme0EfPs1Yun5ACC9N4OA7kQuTsVEqpn-iw0_tCWVq4TrucWLtEOxsR-v6iU3SGiSlVt7KY4PEUY104LJotWRzB-QvPGkyjx6nA_D2LuajxMTHoTjf3cHvJGCjYsyfGZkGanz6w1njUlojbXxbmVCAOtK0sX-AIw3W9OIhK9YrTk2VdES4Nc4mMETr6NUl1oBKTXK_ckQ9nn9Xf85qn50TWw3OVl_O63yK7UeOrLMauFf_8vRhLN7nL3QY9O7pye8gbqLgxeZ2JpO58Al1yY',
        }


    # ---------------------------------------------------------------------------

    def _call_api(self, signature: str) -> login_types.LoginAPIResponse:
        """Invoke the API to Login"""

        headers = {
            'X-QAPP-Authorization': signature,
            'X-QAPP-Portal': 'api',
            'X-QAPP-SubPortal': 'python_sdk',
            'X-QAPP-Version': qapp_package_version,
            'X-QAPP-PythonVersion': sys.version,
        }

        payload: dict[str, typing.Any] = {
            'mode': 'api_login',
            'api_version': '1',
            'login_data': {
                'api_key': self.api_key,
                'signature': signature,
            },
        }

        qapp_logger.debug(f"Invoking Login API -> {headers=}, {payload=}")

        return requests.post(
            url=login_config.LoginAPI.URL,
            json=payload,
            headers=headers,
            timeout=login_config.LoginAPI.TIMEOUT,
        ).json()

    # ---------------------------------------------------------------------------

    def _get_signature(self) -> str:
        """Create a signature based on the user credentials and other details to enforce the security even more"""

        signature = ''

        # Multi-stage msg sign
        msgs_to_sign = [
            self.api_key.encode('utf-8'),  # Api Key
            dt.datetime.now(generic_constants.DT_ZONE_IST).strftime(format=login_config.DATETIME_FMT_MSG_TO_SIGN).encode('utf-8'),
        ]

        # Intital key with secret key
        _key_to_sign = self.secret_key.encode('utf-8')

        # Sign all messages
        for idx, msg_to_sign in enumerate(msgs_to_sign, 1):

            _resp = self._sign(
                msg=msg_to_sign,
                key=_key_to_sign,
            )

            # On final msg, get the hex str value
            if idx == len(msgs_to_sign):
                signature = _resp.hexdigest()

            # Consider the new resultant bytes as a key for next msg signature creation
            else:
                _key_to_sign = _resp.digest()

        return signature

    # ---------------------------------------------------------------------------

    def _sign(self, msg: bytes, key: bytes) -> hmac.HMAC:
        """Sign the msg with HMAC"""

        return hmac.new(
            key=key,
            msg=msg,
            digestmod=login_config.HMAC_DIGEST_MOD,
        )