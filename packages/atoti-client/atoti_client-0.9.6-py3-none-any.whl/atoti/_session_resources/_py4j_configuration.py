from typing import final

from httpx import Response
from pydantic.dataclasses import dataclass

from .._activeviam_client import ActiveViamClient
from .._pydantic import PYDANTIC_CONFIG


@final
@dataclass(config=PYDANTIC_CONFIG, frozen=True, kw_only=True)
class Py4jConfiguration:
    distributed: bool
    port: int
    token: str | None = None


def request_py4j_configuration(activeviam_client: ActiveViamClient) -> Response:
    return activeviam_client.http_client.get(
        activeviam_client.get_endpoint_path(
            namespace="atoti",
            route="py4j/configuration",
        ),
    )


def retrieve_py4j_configuration(
    activeviam_client: ActiveViamClient,
) -> Py4jConfiguration:
    response = request_py4j_configuration(activeviam_client)
    response.raise_for_status()
    return activeviam_client.get_json_response_body_type_adapter(
        Py4jConfiguration,
    ).validate_json(response.content)
