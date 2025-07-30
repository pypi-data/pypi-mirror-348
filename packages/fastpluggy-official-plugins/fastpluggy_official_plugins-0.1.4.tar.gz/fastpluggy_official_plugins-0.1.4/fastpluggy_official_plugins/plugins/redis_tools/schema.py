from typing import Optional

from pydantic import BaseModel


class RedisKeyInfo(BaseModel):
    key: str
    type: str
    ttl: int
    size: Optional[int] = None
    preview: Optional[str] = None
