from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class IPO(Base):
    __tablename__ = "ipos"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_name: Mapped[str] = mapped_column(String(255), index=True)
    company_logo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price_band_min: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    price_band_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    open_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    close_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    listing_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    issue_size: Mapped[str | None] = mapped_column(String(100), nullable=True)
    issue_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="upcoming", index=True)
    ipo_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    listing_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    cmp: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    rhp_pdf: Mapped[str | None] = mapped_column(String(500), nullable=True)
    drhp_pdf: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    @property
    def listing_gain(self):
        if self.ipo_price is not None and self.listing_price is not None:
            return self.listing_price - self.ipo_price
        return None

    @property
    def listing_gain_percent(self):
        if self.ipo_price and self.listing_price:
            return (self.listing_price - self.ipo_price) / self.ipo_price * 100
        return None

    @property
    def current_return(self):
        if self.ipo_price and self.cmp:
            return (self.cmp - self.ipo_price) / self.ipo_price * 100
        return None
