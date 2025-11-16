# SPDX-License-Identifier: MIT
"""StockDailyRecommendation data model"""

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


class StockDailyRecommendationBase(SQLModel):
    
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
    recommend_date: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="推荐日期"
        )
    )
    recommend_level: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="推荐等级(1:强烈推荐 2:推荐 3:中性 4:谨慎 5:卖出)"
        )
    )
    price: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="当前价(分)"
        )
    )
    target_price: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="目标价(分)"
        )
    )
    recommend_reason: Optional[str] = Field(
        sa_column=Column(
            String,
            nullable=True,
            comment="推荐理由"
        )
    )
    analyst: Optional[str] = Field(
        sa_column=Column(
            String(100),
            nullable=True,
            comment="分析师"
        )
    )
    institution: Optional[str] = Field(
        sa_column=Column(
            String(100),
            nullable=True,
            comment="机构名称"
        )
    )
    risk_level: Optional[str] = Field(
        sa_column=Column(
            String,
            nullable=True,
            comment="风险等级"
        )
    )
    validity_period: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="有效期(天)"
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


class StockDailyRecommendationModel(StockDailyRecommendationBase, table=True):
    __tablename__ = "stock_daily_recommendation"
    __table_args__ = (
        Index("idx_recommend_date", recommend_date),
        Index("idx_stock_date", stock_symbol_full, recommend_date),
    )