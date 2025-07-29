"""Enterprise utilities for Reflex CLI."""

from reflex.config import Config, EnvironmentVariables, EnvVar


class ConfigEnterprise(Config):
    """Enterprise configuration class."""

    show_built_with_reflex: bool | None = None

    use_single_port: bool | None = None


class EnvironmentEnterpriseVariables(EnvironmentVariables):
    """Enterprise environment variables."""

    REFLEX_ENTERPRISE_SHOW_BUILT_WITH_REFLEX = EnvVar(
        "REFLEX_ENTERPRISE_SHOW_BUILT_WITH_REFLEX",
        bool,
        "Whether to show the 'Built with Reflex' message.",
    )

    REFLEX_ENTERPRISE_USE_SINGLE_PORT = EnvVar(
        "REFLEX_ENTERPRISE_USE_SINGLE_PORT",
        bool,
        "Whether to use a single port for all Reflex apps.",
    )


Config = ConfigEnterprise

environment = EnvironmentEnterpriseVariables()
