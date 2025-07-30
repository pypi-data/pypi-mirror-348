from __future__ import annotations

import os
import tempfile
from collections.abc import Generator
from contextlib import ExitStack, contextmanager
from dataclasses import replace
from pathlib import Path
from secrets import token_urlsafe
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING

from _atoti_core import LicenseKeyLocation
from py4j.java_gateway import DEFAULT_ADDRESS

from .._activeviam_client import ActiveViamClient
from .._atoti_client import AtotiClient
from .._generate_session_id import generate_session_id
from .._java_api import JavaApi
from ..config import (
    SessionConfig,
)
from ._api_token_and_jwt_authentication import ApiTokenAndJwtAuthentication
from ._py4j_configuration import retrieve_py4j_configuration
from ._transform_session_config import (
    add_branding_app_extension_to_config,
    apply_plugin_config_hooks,
    convert_session_config_to_json,
)

if TYPE_CHECKING:
    from _atoti_server import (  # pylint: disable=nested-import,undeclared-dependency
        ServerSubprocess,
    )


# Keep environment variable names and default values in sync with constants in Java's ApplicationStarter.
_idle_application_starter_path = Path(
    os.getenv(
        "_ATOTI_IDLE_APPLICATION_STARTER_PATH",
        f"{tempfile.gettempdir()}/atoti-idle-application-starter",
    )
)
_default_debug_session_config_path = Path(
    os.getenv(
        "_ATOTI_DEFAULT_DEBUG_SESSION_CONFIG_PATH",
        f"{tempfile.gettempdir()}/atoti-session-config",
    )
)
_default_debug_port_path = Path(
    os.getenv(
        "_ATOTI_DEFAULT_DEBUG_PORT_PATH",
        f"{tempfile.gettempdir()}/atoti-port",
    )
)


def _update_args_with_dev_env_vars(
    *,
    debug: bool,
    session_config_path: Path | None,
    port_path: Path | None,
) -> tuple[bool, Path | None, Path | None]:
    """Updates the given ``started_session_resources`` arguments based on environment variables meant for development."""
    if not debug:
        try:
            _idle_application_starter_path.unlink()
            debug = True
        except:  # noqa: E722, S110
            pass  # Either the file didn't exist so no application starter is idle, or some other error occurred and we'll ignore it because this is a development feature

    if debug:
        session_config_path = session_config_path or _default_debug_session_config_path
        port_path = port_path or _default_debug_port_path

    return debug, session_config_path, port_path


def _get_url(*, address: str, https_domain: str | None, port: int) -> str:
    if address == DEFAULT_ADDRESS:
        address = "localhost"

    protocol = "http"

    if https_domain is not None:
        address = https_domain
        protocol = "https"

    return f"{protocol}://{address}:{port}"


def _create_temporary_file(suffix: str | None = None) -> Path:
    with NamedTemporaryFile(delete=False, suffix=suffix) as file:
        return Path(file.name)


@contextmanager
def started_session_resources(
    *,
    address: str | None,
    config: SessionConfig,
    distributed: bool,
    enable_py4j_auth: bool,
    py4j_server_port: int | None,
    debug: bool,
    session_config_path: Path | None,
    port_path: Path | None,
    api_token: str | None,
) -> Generator[tuple[AtotiClient, JavaApi, ServerSubprocess | None, str], None, None]:
    from _atoti_server import (  # pylint: disable=nested-import,undeclared-dependency,shortest-import
        ServerSubprocess,
        resolve_license_key,
        retrieve_spring_application_port,
    )

    if address is None:
        address = DEFAULT_ADDRESS

    debug, session_config_path, port_path = _update_args_with_dev_env_vars(
        debug=debug,
        session_config_path=session_config_path,
        port_path=port_path,
    )

    config = apply_plugin_config_hooks(config)
    config = add_branding_app_extension_to_config(config)
    if config.license_key == LicenseKeyLocation.EMBEDDED:
        # Allows debugging the Java side of an Atoti Python SDK test with the same license key as the one set up on the Python side.
        license_key = resolve_license_key(config.license_key)
        assert license_key is not None
        config = replace(config, license_key=license_key)
    api_token = api_token or token_urlsafe()
    config_json = convert_session_config_to_json(
        config, api_token=api_token, distributed=distributed
    )

    session_id = generate_session_id()
    server_subprocess: ServerSubprocess | None = None

    if session_config_path is None:
        session_config_path = _create_temporary_file(".json")

    with ExitStack() as exit_stack:
        try:
            session_config_path.write_text(config_json)

            if port_path is not None:
                # Most likely a leftover since the server isn't ready yet
                port_path.unlink(missing_ok=True)

            if debug:
                if port_path is None:
                    # We need to be given the same path as the server and can't guess it or choose it ourselves
                    raise ValueError(
                        "A file in which to write the port must be specified when in debug mode"
                    )

                session_port, _ = retrieve_spring_application_port(
                    port_path, process=None
                )
            else:
                if port_path is None:
                    port_path = _create_temporary_file()

                server_subprocess = exit_stack.enter_context(
                    ServerSubprocess.create(
                        address=address,
                        enable_py4j_auth=enable_py4j_auth,
                        extra_jars=config.extra_jars,
                        java_options=config.java_options,
                        license_key=config.license_key,
                        logs_destination=config.logging.destination
                        if config.logging
                        else None,
                        session_config_path=session_config_path,
                        port_path=port_path,
                        port=config.port,
                        py4j_server_port=py4j_server_port,
                        session_id=session_id,
                    ),
                )
                session_port = server_subprocess.port
        finally:
            session_config_path.unlink(missing_ok=True)
            if port_path is not None:
                port_path.unlink(missing_ok=True)

        url = _get_url(
            address=address,
            https_domain=config.security.https.domain
            if config.security and config.security.https
            else None,
            port=session_port,
        )

        authentication = ApiTokenAndJwtAuthentication(api_token)
        with ActiveViamClient.create(
            url,
            authentication=authentication,
            certificate_authority=config.security.https.certificate_authority
            if config.security and config.security.https
            else None,
            ping=not distributed,
        ) as activeviam_client:
            atoti_client = AtotiClient(activeviam_client=activeviam_client)

            py4j_configuration = retrieve_py4j_configuration(activeviam_client)

            java_api = exit_stack.enter_context(
                JavaApi.create(
                    address=address,
                    detached=False,
                    distributed=distributed,
                    py4j_auth_token=py4j_configuration.token,
                    py4j_java_port=py4j_configuration.port,
                    session_id=session_id,
                ),
            )
            authentication.set_java_api(java_api)

            yield atoti_client, java_api, server_subprocess, session_id
