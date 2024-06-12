from datetime import timedelta

from api.api_v1.auth.utils import encode_jwt
from api.api_v1.user.schemas import UserSchema

from core.config import settings


SECRET_KEY = settings.auth.secret_key
ALGORITHM = settings.auth.algorithm

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserSchema):
    jwt_payload = {
        "user_id": str(user.uid),
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth.access_token_expire_minutes,
    )


def create_refresh_token(user: UserSchema):
    jwt_payload = {
        "username": user.username,

    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth.refresh_token_expire_days,
        expire_timedelta=timedelta(days=settings.auth.refresh_token_expire_days),
    )