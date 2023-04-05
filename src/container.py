from dependency_injector import containers, providers

from src.config.server import ServerConfig
from src.svc.health import HealthService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.health",
        ]
    )

    # config
    server_config: ServerConfig = providers.Singleton(ServerConfig)

    # infra
    # here would setup auth, repositories, etc.

    # services
    health: HealthService = providers.Singleton(
        HealthService,
        others=[],
    )
