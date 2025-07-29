from typing import Optional

from fastpluggy.core.config import BaseDatabaseSettings


class RedisToolsSettings(BaseDatabaseSettings):
    # Redis connection settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_decode_responses: bool = True
    
    # Browser settings
    keys_limit: int = 100
    
    # Task settings
    enable_clean_expired_keys: bool = False
    clean_expired_keys_interval: int = 3600  # 1 hour