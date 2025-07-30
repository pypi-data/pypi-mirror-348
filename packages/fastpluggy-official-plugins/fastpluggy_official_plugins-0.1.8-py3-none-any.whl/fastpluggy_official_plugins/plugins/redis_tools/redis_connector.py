from typing import List, Dict, Any

from fastapi import HTTPException
import redis

from redis_tools.schema import RedisKeyInfo


class RedisConnection:
    def __init__(self, db: int = None):
        # Get settings from config
        from .config import RedisToolsSettings
        self.settings = RedisToolsSettings()

        # Use provided db or default from settings
        db_to_use = db if db is not None else self.settings.redis_db

        # Create Redis client with settings
        self.client = self._create_client(db_to_use)

    def _create_client(self, db: int = 0) -> redis.Redis:
        if self.settings.REDIS_DSN:
            return redis.from_url(self.settings.REDIS_DSN, db=db, decode_responses=self.settings.redis_decode_responses)
        return redis.Redis(
            host=self.settings.redis_host,
            port=self.settings.redis_port,
            ssl=self.settings.use_ssl,
            db=db,
            password=self.settings.redis_password,
            decode_responses=self.settings.redis_decode_responses
        )

    def test_connection(self) -> bool:
        try:
            return self.client.ping()
        except redis.exceptions.ConnectionError:
            return False

    def get_key_info(self, key: str) -> RedisKeyInfo:
        key_type = self.client.type(key)
        ttl = self.client.ttl(key)

        preview = None
        size = None

        if key_type == "string":
            value = self.client.get(key)
            size = len(value) if value else 0
            preview = value[:100] if value else ""
        elif key_type == "list":
            size = self.client.llen(key)
            preview = str(self.client.lrange(key, 0, 5))
        elif key_type == "hash":
            size = self.client.hlen(key)
            preview = str(dict(list(self.client.hgetall(key).items())[:5]))
        elif key_type == "set":
            size = self.client.scard(key)
            preview = str(self.client.smembers(key)[:5] if size <= 5 else list(self.client.smembers(key))[:5])
        elif key_type == "zset":
            size = self.client.zcard(key)
            preview = str(self.client.zrange(key, 0, 5, withscores=True))

        return RedisKeyInfo(
            key=key,
            type=key_type,
            ttl=ttl,
            size=size,
            preview=preview
        )

    def get_keys(self, pattern: str = "*", limit: int = None) -> List[RedisKeyInfo]:
        from .config import RedisToolsSettings
        settings = RedisToolsSettings()

        # Use provided limit or default from settings
        if limit is None:
            limit = settings.keys_limit

        keys = self.client.keys(pattern)[:limit]
        return [self.get_key_info(key) for key in keys]

    def get_key_data(self, key: str) -> Dict[str, Any]:
        key_type = self.client.type(key)
        data = {
            "key": key,
            "type": key_type,
            "ttl": self.client.ttl(key),
        }

        if key_type == "string":
            data["value"] = self.client.get(key)
        elif key_type == "list":
            data["value"] = self.client.lrange(key, 0, -1)
        elif key_type == "hash":
            data["value"] = self.client.hgetall(key)
        elif key_type == "set":
            data["value"] = list(self.client.smembers(key))
        elif key_type == "zset":
            data["value"] = self.client.zrange(key, 0, -1, withscores=True)

        return data

    def delete_key(self, key: str) -> bool:
        return bool(self.client.delete(key))

    def flush_db(self) -> bool:
        self.client.flushdb()
        return True

    def get_current_db(self) -> int:
        """Get the current database index."""
        return self.client.connection_pool.connection_kwargs.get('db', 0)

    def get_databases(self) -> List[Dict[str, Any]]:
        """Get a list of available Redis databases with key counts."""
        # Create a connection to database 0 to run the INFO command
        info_client = self._create_client(0)

        # Get database info from Redis INFO command
        info = info_client.info('keyspace')

        # Default Redis has 16 databases (0-15)
        # We can determine the actual number from the keyspace info
        max_db = 15  # Default max database index

        # Find the highest database index in the keyspace info
        for key in info.keys():
            if key.startswith('db'):
                try:
                    db_index = int(key[2:])  # Extract number from 'db0', 'db1', etc.
                    max_db = max(max_db, db_index)
                except ValueError:
                    pass

        # Create a list of all databases (even empty ones)
        databases = []
        current_db = self.get_current_db()

        for i in range(max_db + 1):
            db_key = f'db{i}'
            db_info = info.get(db_key, {})

            # If the database isn't in the info, it's empty
            keys = db_info.get('keys', 0)
            expires = db_info.get('expires', 0)

            databases.append({
                'index': i,
                'keys': keys,
                'expires': expires,
                'current': i == current_db
            })

        return databases

    def select_db(self, db_index: int) -> bool:
        try:
            self.client = self._create_client(db_index)
            self.db = db_index
            return self.test_connection()
        except Exception:
            return False


def get_redis_connection(db: int = None):
    conn = RedisConnection(db=db)
    if not conn.test_connection():
        raise HTTPException(status_code=500, detail="Cannot connect to Redis server")
    return conn
