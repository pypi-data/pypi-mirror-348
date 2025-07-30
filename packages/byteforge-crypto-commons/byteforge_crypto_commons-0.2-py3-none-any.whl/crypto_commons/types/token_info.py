from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class TokenInfo:
    id: int
    rank: Optional[int]
    name: str
    symbol: str
    slug: str
    status: int
    is_active: Optional[int] = None
    first_historical_data: Optional[datetime] = None
    last_historical_data: Optional[datetime] = None
    platform: Optional[str] = None
