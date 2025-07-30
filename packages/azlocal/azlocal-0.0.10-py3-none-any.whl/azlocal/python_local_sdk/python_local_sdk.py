import os

from ..shared import get_proxy_endpoint, get_proxy_env_vars


class PythonLocalSdk:

    def __init__(self):
        self._started = False
        self._existing_env_vars: dict[str, str] = {}
        self._proxy_endpoint = get_proxy_endpoint()

    def start_interception(self):
        if self._started:
            return

        proxy_endpoint = get_proxy_endpoint()
        proxy_env_vars = get_proxy_env_vars(proxy_endpoint)

        # Keep a copy of the existing env vars
        # We're about to overwrite them, but we do want to revert them to the old value when we're done
        self._existing_env_vars = {
            "HTTP_PROXY": os.environ.get("HTTP_PROXY"),
            "HTTPS_PROXY": os.environ.get("HTTPS_PROXY"),
            "MSSQL_ACCEPT_EULA": os.environ.get("MSSQL_ACCEPT_EULA"),
            "REQUESTS_CA_BUNDLE": os.environ.get("REQUESTS_CA_BUNDLE"),
        }

        os.environ.update(proxy_env_vars)

    def stop_interception(self):
        if not self._started:
            return
        os.environ.update({k:v for k,v in self._existing_env_vars.items() if v})
        self._existing_env_vars.clear()

        self._started = False
