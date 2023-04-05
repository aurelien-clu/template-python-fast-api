import typing as t

from pydantic import BaseSettings, Field


class CorsConfig(BaseSettings):
    origins: t.List[str] = Field(default_factory=list, env="CORS_ORIGINS")
    allow_credentials: bool = True
    allow_methods = ["*"]
    allow_headers = ["*"]


class ServerConfig(BaseSettings):
    cors = CorsConfig()
