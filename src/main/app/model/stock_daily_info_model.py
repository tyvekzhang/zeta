# SPDX-License-Identifier: MIT
"""StockDailyInfo data model"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    DateTime,
    Index,
    UniqueConstraint,
    BigInteger,
    String,
    Integer,
    DateTime,
)

from fastlib.utils.snowflake_util import snowflake_id


class StockDailyInfoBase(SQLModel):
    
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        nullable=False,
        sa_type=BigInteger,sa_column_kwargs={"comment": "主键"}
    )
    stock_symbol_full: Optional[str] = Field(
        sa_column=Column(
            String(20),
            nullable=True,
            comment="股票代码"
        )
    )
    trade_date: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="交易日期"
        )
    )
    open_price: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="开盘价(分)"
        )
    )
    close_price: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="收盘价(分)"
        )
    )
    high_price: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="最高价(分)"
        )
    )
    low_price: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="最低价(分)"
        )
    )
    volume: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="成交量(股)"
        )
    )
    turnover: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="成交额(分)"
        )
    )
    change_amount: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="涨跌额(分)"
        )
    )
    change_rate: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="涨跌幅"
        )
    )
    pe_ratio: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="市盈率"
        )
    )
    pb_ratio: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="市净率"
        )
    )
    market_cap: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="总市值(分)"
        )
    )
    circulating_market_cap: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="流通市值(分)"
        )
    )
    turnover_rate: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="换手率"
        )
    )
    bid_price1: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="买一价(分)"
        )
    )
    bid_price2: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="买二价(分)"
        )
    )
    bid_price3: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="买三价(分)"
        )
    )
    bid_price4: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="买四价(分)"
        )
    )
    bid_price5: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="买五价(分)"
        )
    )
    bid_volume1: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="买一量(股)"
        )
    )
    bid_volume2: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="买二量(股)"
        )
    )
    bid_volume3: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="买三量(股)"
        )
    )
    bid_volume4: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="买四量(股)"
        )
    )
    bid_volume5: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="买五量(股)"
        )
    )
    ask_price1: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="卖一价(分)"
        )
    )
    ask_price2: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="卖二价(分)"
        )
    )
    ask_price3: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="卖三价(分)"
        )
    )
    ask_price4: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="卖四价(分)"
        )
    )
    ask_price5: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="卖五价(分)"
        )
    )
    ask_volume1: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="卖一量(股)"
        )
    )
    ask_volume2: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="卖二量(股)"
        )
    )
    ask_volume3: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="卖三量(股)"
        )
    )
    ask_volume4: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="卖四量(股)"
        )
    )
    ask_volume5: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="卖五量(股)"
        )
    )
    created_at: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=lambda: datetime.now(timezone.utc),sa_column_kwargs={"comment": "创建时间"}
    )
    updated_at: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={
            "onupdate":lambda: datetime.now(timezone.utc),"comment": "更新时间",
        },
    )


class StockDailyInfoModel(StockDailyInfoBase, table=True):
    __tablename__ = "stock_daily_info"
    __table_args__ = (
        Index("idx_stock_symbol", "stock_symbol_full"),
        Index("idx_trade_date", "trade_date"),
    )