# SPDX-License-Identifier: MIT
"""SectorCapitalFlow data model"""

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


class SectorCapitalFlowBase(SQLModel):
    
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
    sector_code: Optional[str] = Field(
        sa_column=Column(
            String(32),
            nullable=True,
            comment="板块代码"
        )
    )
    sector_name: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            comment="板块名称"
        )
    )
    sector_type: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="板块类型(1行业 2概念 3地区)"
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
    stock_count: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="成分股数量"
        )
    )
    rise_count: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="上涨家数"
        )
    )
    fall_count: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="下跌家数"
        )
    )
    flat_count: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="平盘家数"
        )
    )
    sector_index: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="板块指数(x100)"
        )
    )
    change_percent: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="涨跌幅(x100)"
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


class SectorCapitalFlowModel(SectorCapitalFlowBase, table=True):
    __tablename__ = "sector_capital_flow"
    __table_args__ = (
        Index("idx_change_percent", "change_percent"),
        Index("idx_sector_type", "sector_type"),
        Index("idx_trade_date_sector_code", "trade_date", "sector_code"),
    )