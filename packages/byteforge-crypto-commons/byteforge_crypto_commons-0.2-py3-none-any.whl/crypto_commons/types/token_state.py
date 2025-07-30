from dataclasses import dataclass
from typing import Dict, List, Optional
import datetime
from .quote import Quote

@dataclass
class TokenState:
    """Represents the state of a token at a specific moment in time.
    
    This class captures all relevant information about a cryptocurrency token at a specific timestamp,
    including its basic information, market data, supply metrics, and status indicators.

    Required Fields:
        id: Unique identifier for the token
        name: Full name of the token
        symbol: Trading symbol of the token
        timestamp: The specific moment in time this token state represents
        quote_map: Dictionary mapping currency codes to Quote objects containing price and volume data

    Optional Fields:
        last_updated: When this data was last updated in a source system
        infinite_supply: Whether the token has an infinite supply (e.g., ETH)
        slug: URL-friendly version of the token name
        num_market_pairs: Number of active trading pairs for this token
        creation_date: When the token was first created/launched (e.g., Bitcoin's genesis block)
        tags: List of categories or labels associated with the token
        max_supply: Maximum possible supply of the token
        circulating_supply: Number of tokens currently in circulation
        total_supply: Total number of tokens that exist (including locked/unreleased)
        platform: Blockchain platform the token is built on (if applicable)
        cmc_rank: CoinMarketCap ranking of the token
        self_reported_circulating_supply: Circulating supply as reported by the token team
        self_reported_market_cap: Market cap as reported by the token team
        tvl_ratio: Total Value Locked ratio
        is_market_cap_included_in_calc: Whether this token's market cap is included in total market calculations
        is_active: Whether the token is currently active/trading
        is_fiat: Whether this is a fiat currency
    """
    id: int
    name: str
    symbol: str
    timestamp: int  # The specific moment in time this token state represents
    quote_map: Dict[str, Quote]
    last_updated: Optional[datetime.datetime] = None  # When this data was last updated in source system

    infinite_supply: bool = None
    slug: Optional[str] = None
    num_market_pairs: Optional[int] = None
    creation_date: Optional[datetime.datetime] = None  # When the token was first created/launched (e.g. Bitcoin's genesis block)
    tags: Optional[List[str]] = None
    max_supply: Optional[int] = None
    circulating_supply: Optional[int] = None
    total_supply: Optional[float] = None
    platform: Optional[str] = None
    cmc_rank: Optional[int] = None
    self_reported_circulating_supply: Optional[int] = None
    self_reported_market_cap: Optional[float] = None
    tvl_ratio: Optional[float] = None
    is_market_cap_included_in_calc: Optional[bool] = None
    is_active: Optional[bool] = None
    is_fiat: Optional[bool] = None



