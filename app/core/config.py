from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsRedis(BaseModel):
    host: str = "localhost"
    port: int = 6379


class AuthConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8080


class ApiV1Prefix(BaseModel):
    users: str = "/users"
    auth: str = "/auth"
    products: str = "/products"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    auth: AuthConfig
    redis: SettingsRedis


settings = Settings()
