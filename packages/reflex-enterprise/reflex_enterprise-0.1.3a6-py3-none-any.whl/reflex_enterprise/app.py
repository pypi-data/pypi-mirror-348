"""Enterprise app class."""

from reflex.app import App
from reflex.config import environment, get_config
from reflex.utils.exec import is_prod_mode

from reflex_enterprise import constants
from reflex_enterprise.config import ConfigEnterprise
from reflex_enterprise.utils import check_config_option_in_tier, is_deploy_context


class AppEnterprise(App):
    """Enterprise app class."""

    def __post_init__(self):
        """Post-initialization."""
        super().__post_init__()
        self._verify_and_setup_badge()
        self._verify_and_setup_proxy()

    def _verify_and_setup_badge(self):
        config = get_config()
        deploy = is_deploy_context()

        check_config_option_in_tier(
            option_name="show_built_with_reflex",
            allowed_tiers=(
                ["pro", "team", "enterprise"] if deploy else ["team", "enterprise"]
            ),
            fallback_value=True,
            help_link=constants.SHOW_BUILT_WITH_REFLEX_INFO,
        )

        if is_prod_mode() and config.show_built_with_reflex:
            self._setup_sticky_badge()

    def _verify_and_setup_proxy(self):
        config = get_config()
        deploy = is_deploy_context()

        if isinstance(config, ConfigEnterprise):
            check_config_option_in_tier(
                "use_single_port",
                [] if deploy else ["team", "enterprise"],
                False,
            )

            if config.use_single_port and not environment.REFLEX_BACKEND_ONLY.get():
                # Enable proxying to frontend server.
                from .proxy import proxy_middleware

                self.register_lifespan_task(proxy_middleware)


App = AppEnterprise
