from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class IPOBase(BaseModel):
    company_name: str = Field(min_length=2, max_length=255)
    company_logo: str | None = None
    price_band_min: Decimal | None = Field(default=None, ge=0)
    price_band_max: Decimal | None = Field(default=None, ge=0)
    open_date: date | None = None
    close_date: date | None = None
    listing_date: date | None = None
    issue_size: str | None = None
    issue_type: str | None = None
    status: str = "upcoming"
    ipo_price: Decimal | None = Field(default=None, ge=0)
    listing_price: Decimal | None = Field(default=None, ge=0)
    cmp: Decimal | None = Field(default=None, ge=0)
    rhp_pdf: str | None = None
    drhp_pdf: str | None = None
    description: str | None = None

class IPOCreate(IPOBase): pass
class IPOUpdate(IPOBase): pass

class IPOSummary(IPOBase):
    id: int
    listing_gain: Decimal | None = None
    listing_gain_percent: Decimal | None = None
    current_return: Decimal | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
