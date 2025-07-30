from dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class Quote:
    """Represents a cryptocurrency quote with market data and statistics.
    
    This class encapsulates all relevant market data for a cryptocurrency, including
    price, volume, market cap, and various percentage changes over different time periods.
    It's designed to handle both required core metrics and optional extended metrics.
    
    Attributes:
        base_currency (str): The cryptocurrency symbol (e.g., 'BTC', 'ETH').
        price (float): Current price of the cryptocurrency.
        volume_24h (float): 24-hour trading volume in the base currency.
        percent_change_1h (float): Price change percentage over the last hour.
        percent_change_24h (float): Price change percentage over the last 24 hours.
        percent_change_7d (float): Price change percentage over the last 7 days.
        percent_change_30d (float): Price change percentage over the last 30 days.
        market_cap (float): Total market capitalization of the cryptocurrency.
        last_updated (datetime.datetime): Timestamp of when this quote was last updated.
        volume_change_24h (float): Change in 24-hour volume compared to previous period.
        percent_change_60d (float): Price change percentage over the last 60 days.
        percent_change_90d (float): Price change percentage over the last 90 days.
        market_cap_dominance (float): Percentage of total crypto market cap this currency represents.
        fully_diluted_market_cap (float): Market cap if all tokens were in circulation.
        tvl (Optional[float]): Total Value Locked in DeFi protocols, if applicable.
        volume_30d (Optional[float]): 30-day trading volume.
        volume_30d_reported (Optional[float]): Reported 30-day trading volume from exchanges.
        volume_24h_reported (Optional[float]): Reported 24-hour trading volume from exchanges.
        volume_7d_reported (Optional[float]): Reported 7-day trading volume from exchanges.
        market_cap_by_total_supply (Optional[float]): Market cap calculated using total supply.
        volume_7d (Optional[float]): 7-day trading volume.
        total_supply (Optional[float]): Total number of tokens that will ever exist.
        circulating_supply (Optional[float]): Number of tokens currently in circulation.
    """
    base_currency: str
    price: float
    volume_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    percent_change_30d: float
    market_cap: float
    last_updated: datetime.datetime

    # Now all optional/default parameters follow
    volume_change_24h: float = 0.0
    percent_change_60d: float = 0.0
    percent_change_90d: float = 0.0
    market_cap_dominance: float = 0.0
    fully_diluted_market_cap: float = 0.0
    tvl: Optional[float] = None
    volume_30d: Optional[float] = None
    volume_30d_reported: Optional[float] = None
    volume_24h_reported: Optional[float] = None
    volume_7d_reported: Optional[float] = None
    market_cap_by_total_supply: Optional[float] = None
    volume_7d: Optional[float] = None
    total_supply: Optional[float] = None
    circulating_supply: Optional[float] = None
