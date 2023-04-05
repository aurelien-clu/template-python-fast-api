from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.svc.health import HealthService

router = APIRouter()


def _health_check(health: HealthService):
    if health.is_healthy() is True:
        return "ok"
    raise HTTPException(status_code=503, detail="Health check failed")


@router.head("/", name="Health check")
@inject
async def health_head_root(svc: HealthService = Depends(Provide[Container.health])):
    return _health_check(health=svc)


@router.get("/", name="Health check")
@inject
async def health_get_root(svc: HealthService = Depends(Provide[Container.health])):
    return _health_check(health=svc)


@router.head("/health", name="Health check")
@inject
async def health_head(svc: HealthService = Depends(Provide[Container.health])):
    return _health_check(health=svc)


@router.get("/health", name="Health check")
@inject
async def health_get(svc: HealthService = Depends(Provide[Container.health])):
    return _health_check(health=svc)
