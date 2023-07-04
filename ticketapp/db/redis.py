from redis_om import get_redis_connection
from ..config.settings import settings


redis = get_redis_connection(
    host = f'{settings.redis_host}',
    port = settings.redis_port,
    password = f"{settings.redis_password}",
    decode_responses = True,
)
