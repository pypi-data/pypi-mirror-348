"""
SnapEnv Base Settings.

This module contains the base settings and configurations used across different
environments within the SnapEnv framework. It provides constants, environment
detection, and directory setup necessary for the application to function
correctly, especially in containerized environments such as Docker.

The module also defines the `SnapEnvCommonSettings` class, which manages the
configuration parameters, their sources, and provides methods to retrieve
environment-specific information like the local server name and platform.

Attributes
----------
SECRETS_DIR : str
    Directory path where secret files are located, depending on whether the code
    is running inside a Docker container or not.
PLATFORM : dict
    Mapping of platform identifiers to their respective names.
ENVIRONMENT : str
    Current environment identifier, sourced from the ENVIRONMENT environment variable.

Secret Directory Setup
----------------------
The module ensures that the secrets directory exists unless running inside a
Docker container, where Docker handles directory management.

Environment File Selection
--------------------------
The `.env` file used by the application is determined by the value of the
`ENVIRONMENT` environment variable.

- If `ENVIRONMENT` is set to a value (e.g., 'production'), the application will
  look for a file named `<ENVIRONMENT>.env` (e.g., `production.env`).
- This file name is specified in the `model_config` attribute of the
  `SnapEnvCommonSettings` class under `env_file`.
- The `.env` file should be located in the root directory of the project.
- If `ENVIRONMENT` is not set, the application will default to using `.env` as
  the configuration file.
"""

# BUILTIN modules
import os
import platform
import site
import sys

# Third party modules
from pydantic import computed_field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict

# Constants
SECRETS_DIR = "/run/secrets" if os.path.exists("/.dockerenv") else f"{site.USER_BASE}/secrets"
PLATFORM = {"linux": "Linux", "linux2": "Linux", "win32": "Windows", "darwin": "MacOS"}
ENVIRONMENT = os.getenv("ENVIRONMENT", "")


# --------------------------------------------------------------
# This needs to be done before the Base class gets evaluated, and
# to avoid getting five UserWarnings that the path does not exist.
#
# Create the directory if it does not already exist. When running
# inside Docker, skip it (Docker handles that just fine on its own).
#
# if not os.path.exists("/.dockerenv"):
#     os.makedirs(SECRETS_DIR, exist_ok=True)


def initialize_secret_dir() -> None:
    """
    Initialize the secret directory if not running inside a Docker container.

    This function checks for the presence of the "/.dockerenv" file to determine
    if the code is running inside a Docker container. If the file does not exist,
    it creates the directory specified by the `SECRETS_DIR` module variable.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    OSError
        If the directory creation fails due to insufficient permissions or other
        file system-related issues.

    Notes
    -----
    The function uses `os.makedirs` with `exist_ok=True`, so if the directory
    specified by `SECRETS_DIR` already exists, the function will not raise an
    exception.
    """
    if not os.path.exists("/.dockerenv"):
        os.makedirs(SECRETS_DIR, exist_ok=True)


# Call the function at the module level
initialize_secret_dir()


# ------------------------------------------------------------------------
#
class SnapEnvCommonSettings(BaseSettings):
    r"""
    SnapEnv common configuration parameters shared between all instances.

    This class reads configuration parameters defined within the class,
    from environment variables, and from the configuration file's. The source priority
    is as follows (from highest to lowest):

    - env_settings
    - dotenv_settings
    - init_settings
    - file_secret_settings

    Environment Variables
    ---------------------
    The following environment variables should be defined:

    - HOSTNAME (on Linux servers only, set by OS)
    - COMPUTERNAME (on Windows servers only, set by OS)
    - ENVIRONMENT (on all servers)

    File Paths
    ----------
    Paths where the <environment>.env file should be placed:

    - Linux: /home/<user\>/.local
    - macOS: /home/<user\>/.local
    - Windows: C:\\Users\\<user\>\\AppData\\Roaming\\Python
    - Python/Poetry/Docker: Root dir of the project

    Paths where secret files should be placed:

    - Linux: /home/<user\>/.local/secrets
    - macOS: /home/<user\>/.local/secrets
    - Windows: C:\\Users\\<user\>\\AppData\\Roaming\\Python\\secrets
    - Docker: /run/secrets

    Attributes
    ----------
    env : str
        The current environment.
    platform : str
        The platform on which the code is running.
    server : str
        Local server name stripped of possible domain part.
    model_config : SettingsConfigDict
        Configuration dictionary for settings including secrets and .env file handling.

    Methods
    -------
    server():
        Returns the local server name in upper case.
    settings_customise_sources(settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings):
        Customizes the source priority order.
    """

    model_config = SettingsConfigDict(
        extra="ignore",
        secrets_dir=SECRETS_DIR,
        env_file_encoding="utf-8",
        env_file=f"{ENVIRONMENT}.env",
    )

    # constant parameters.

    # Environment depending parameters.
    env: str = ENVIRONMENT
    platform: str = PLATFORM.get(sys.platform, "other")

    @computed_field  # type: ignore[misc]
    @property
    def server(self) -> str:
        """
        Return local server name stripped of possible domain part.

        Returns
        -------
        str
            Server name in upper case.
        """
        return platform.node()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Change source priority order (env trumps environment).

        Parameters
        ----------
        settings_cls : type[BaseSettings]
            The settings class.
        init_settings : PydanticBaseSettingsSource
            Initial settings source.
        env_settings : PydanticBaseSettingsSource
            Environment variable settings source.
        dotenv_settings : PydanticBaseSettingsSource
            Dotenv file settings source.
        file_secret_settings : PydanticBaseSettingsSource
            Secret file settings source.

        Returns
        -------
        tuple[PydanticBaseSettingsSource, ...]
            Tuple of settings sources in the new priority order.
        """
        return (env_settings, dotenv_settings, init_settings, file_secret_settings)
