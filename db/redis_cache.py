import os
import redis
import json
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))


def create_redis_client():
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True,
            socket_timeout=2,
            socket_connect_timeout=2
        )
        client.ping()
        return client
    except Exception:
        return None


redis_client = create_redis_client()


def get_cache(key: str):
    """Retrieve JSON value from Redis."""
    if redis_client is None:
        return None
    try:
        raw = redis_client.get(key)
        return json.loads(raw) if raw else None
    except Exception:
        return None


def set_cache(key: str, value, ttl_seconds: int = 3600):
    """Set JSON-serializable value into Redis."""
    if redis_client is None:
        return
    try:
        redis_client.set(key, json.dumps(value), ex=ttl_seconds)
    except Exception:
        pass
