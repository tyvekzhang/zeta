# SPDX-License-Identifier: MIT
"""IntelligenceInformation data model"""

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


class IntelligenceInformationBase(SQLModel):
    
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
    news_title: Optional[str] = Field(
        sa_column=Column(
            String(500),
            nullable=True,
            comment="标题"
        )
    )
    news_content: Optional[str] = Field(
        sa_column=Column(
            String,
            nullable=True,
            comment="内容"
        )
    )
    news_source: Optional[str] = Field(
        sa_column=Column(
            String(100),
            nullable=True,
            comment="来源"
        )
    )
    publish_time: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="发布时间"
        )
    )
    news_url: Optional[str] = Field(
        sa_column=Column(
            String(500),
            nullable=True,
            comment="新闻链接"
        )
    )
    impact_direction: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="影响面(-1:负面, 0:中性, 1: 正面)"
        )
    )
    impact_level: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="影响程度(1:低, 2:中, 3:高)"
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


class IntelligenceInformationModel(IntelligenceInformationBase, table=True):
    __tablename__ = "intelligence_information"
    __table_args__ = (
        Index("idx_publish_time", publish_time),
        Index("idx_stock_time", stock_symbol_full, publish_time),
        Index("idx_title_content", news_title, news_content),
    )