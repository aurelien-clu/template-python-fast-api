import typing as t


@t.runtime_checkable
class HealthCheck(t.Protocol):
    def is_healthy(self) -> bool:
        ...


class HealthService:
    def __init__(self, others: t.Collection[t.Callable]):
        self.others = others

    def is_healthy(self) -> bool:
        return all([other().is_healthy() for other in self.others])
