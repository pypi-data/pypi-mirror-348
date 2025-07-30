from __future__ import annotations

from collections.abc import Mapping
from typing import final

from typing_extensions import override

from .._is_jwt_expired import is_jwt_expired
from .._java_api import JavaApi
from ..authentication import Authenticate


@final
class ApiTokenAndJwtAuthentication(Authenticate):
    _token: str
    _java_api: JavaApi | None = None
    _jwt: str | None = None

    def __init__(self, token: str) -> None:
        self._token = token

    def set_java_api(self, java_api: JavaApi) -> None:
        self._java_api = java_api
        self._token = ""  # Not needed anymore, we will only use JWT from this point on

    @override
    def __call__(self, _url: str) -> Mapping[str, str]:
        return {"Authorization": self._get_authorization_header()}

    def _get_authorization_header(self) -> str:
        if self._java_api:
            if not self._jwt or is_jwt_expired(self._jwt):
                self._jwt = self._java_api.generate_jwt()
            return f"Jwt {self._jwt}"
        return f"API-TOKEN {self._token}"
