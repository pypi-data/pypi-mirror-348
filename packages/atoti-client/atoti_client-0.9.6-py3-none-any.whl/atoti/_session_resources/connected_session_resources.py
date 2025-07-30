from collections.abc import Generator
from contextlib import ExitStack, contextmanager
from pathlib import Path

import httpx

from .._activeviam_client import ActiveViamClient
from .._atoti_client import AtotiClient
from .._java_api import JavaApi
from ..authentication import Authenticate, ClientCertificate
from ._py4j_configuration import Py4jConfiguration, request_py4j_configuration


@contextmanager
def connected_session_resources(
    url: str,
    /,
    *,
    authentication: Authenticate | ClientCertificate | None,
    certificate_authority: Path | None,
    session_id: str,
) -> Generator[tuple[AtotiClient, JavaApi | None], None, None]:
    with ExitStack() as exit_stack:
        activeviam_client = exit_stack.enter_context(
            ActiveViamClient.create(
                url,
                authentication=authentication,
                certificate_authority=certificate_authority,
            ),
        )
        java_api: JavaApi | None = None
        if activeviam_client.has_compatible_atoti_python_sdk_service:
            py4j_configuration_response = request_py4j_configuration(activeviam_client)
            if py4j_configuration_response.status_code == httpx.codes.OK:
                py4j_configuration = (
                    activeviam_client.get_json_response_body_type_adapter(
                        Py4jConfiguration,
                    ).validate_json(py4j_configuration_response.content)
                )
                java_api = exit_stack.enter_context(
                    JavaApi.create(
                        address=activeviam_client.http_client.base_url.host,
                        detached=True,
                        distributed=py4j_configuration.distributed,
                        py4j_java_port=py4j_configuration.port,
                        py4j_auth_token=py4j_configuration.token,
                        session_id=session_id,
                    ),
                )
        atoti_client = AtotiClient(activeviam_client=activeviam_client)
        yield atoti_client, java_api
