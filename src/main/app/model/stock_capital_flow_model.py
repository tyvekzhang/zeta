# SPDX-License-Identifier: MIT
"""StockCapitalFlow data model"""

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


class StockCapitalFlowBase(SQLModel):
    
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        nullable=False,
        sa_type=BigInteger,sa_column_kwargs={"comment": "主键"}
    )
    trade_date: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="交易日期"
        )
    )
    stock_symbol_full: Optional[str] = Field(
        sa_column=Column(
            String(16),
            nullable=True,
            comment="股票代码(如 600519.SZ)"
        )
    )
    exchange: Optional[str] = Field(
        sa_column=Column(
            String(8),
            nullable=True,
            comment="交易所(SH-上交所 SZ-深交所 BJ-北交所)"
        )
    )
    main_inflow: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="主力流入(元)"
        )
    )
    main_outflow: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="主力流出(元)"
        )
    )
    main_net: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="主力净流入(元)"
        )
    )
    retail_inflow: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="散户流入(元)"
        )
    )
    retail_outflow: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="散户流出(元)"
        )
    )
    retail_net: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="散户净流入(元)"
        )
    )
    total_inflow: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="总流入(元)"
        )
    )
    total_outflow: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="总流出(元)"
        )
    )
    total_net: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="总净流入(元)"
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


class StockCapitalFlowModel(StockCapitalFlowBase, table=True):
    __tablename__ = "stock_capital_flow"
    __table_args__ = (
        Index("idx_symbol", "stock_symbol_full"),
        Index("idx_trade_date", "trade_date"),
    )