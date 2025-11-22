# SPDX-License-Identifier: MIT
"""StockBasicInfo data model"""

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


class StockBasicInfoBase(SQLModel):
    
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        nullable=False,
        sa_type=BigInteger,sa_column_kwargs={"comment": "主键"}
    )
    symbol: Optional[str] = Field(
        sa_column=Column(
            String(10),
            nullable=True,
            comment="股票编号"
        )
    )
    symbol_full: Optional[str] = Field(
        sa_column=Column(
            String(20),
            nullable=True,
            comment="股票代码"
        )
    )
    name: Optional[str] = Field(
        sa_column=Column(
            String(100),
            nullable=True,
            comment="股票名称"
        )
    )
    exchange: Optional[str] = Field(
        sa_column=Column(
            String(10),
            nullable=True,
            comment="交易所"
        )
    )
    listing_date: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="上市日期"
        )
    )
    industry: Optional[str] = Field(
        sa_column=Column(
            String(50),
            nullable=True,
            comment="行业"
        )
    )
    province: Optional[str] = Field(
        sa_column=Column(
            String(50),
            nullable=True,
            comment="省份"
        )
    )
    city: Optional[str] = Field(
        sa_column=Column(
            String(50),
            nullable=True,
            comment="城市"
        )
    )
    company_name: Optional[str] = Field(
        sa_column=Column(
            String(200),
            nullable=True,
            comment="公司全称"
        )
    )
    english_name: Optional[str] = Field(
        sa_column=Column(
            String(200),
            nullable=True,
            comment="英文名称"
        )
    )
    former_name: Optional[str] = Field(
        sa_column=Column(
            String(200),
            nullable=True,
            comment="曾用简称"
        )
    )
    market_type: Optional[str] = Field(
        sa_column=Column(
            String(20),
            nullable=True,
            comment="所属市场"
        )
    )
    legal_representative: Optional[str] = Field(
        sa_column=Column(
            String(50),
            nullable=True,
            comment="法人代表"
        )
    )
    registered_capital: Optional[str] = Field(
        sa_column=Column(
            String(50),
            nullable=True,
            comment="注册资金(万元)"
        )
    )
    establish_date: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="成立日期"
        )
    )
    website: Optional[str] = Field(
        sa_column=Column(
            String(200),
            nullable=True,
            comment="官网"
        )
    )
    email: Optional[str] = Field(
        sa_column=Column(
            String(100),
            nullable=True,
            comment="电子邮箱"
        )
    )
    telephone: Optional[str] = Field(
        sa_column=Column(
            String(50),
            nullable=True,
            comment="联系电话"
        )
    )
    fax: Optional[str] = Field(
        sa_column=Column(
            String(50),
            nullable=True,
            comment="传真"
        )
    )
    registered_address: Optional[str] = Field(
        sa_column=Column(
            String(500),
            nullable=True,
            comment="注册地址"
        )
    )
    business_address: Optional[str] = Field(
        sa_column=Column(
            String(500),
            nullable=True,
            comment="办公地址"
        )
    )
    postal_code: Optional[str] = Field(
        sa_column=Column(
            String(20),
            nullable=True,
            comment="邮政编码"
        )
    )
    main_business: Optional[str] = Field(
        sa_column=Column(
            String,
            nullable=True,
            comment="主营业务"
        )
    )
    business_scope: Optional[str] = Field(
        sa_column=Column(
            String,
            nullable=True,
            comment="经营范围"
        )
    )
    company_profile: Optional[str] = Field(
        sa_column=Column(
            String,
            nullable=True,
            comment="机构简介"
        )
    )
    data_source: Optional[str] = Field(
        sa_column=Column(
            String(50),
            nullable=True,
            comment="数据来源"
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


class StockBasicInfoModel(StockBasicInfoBase, table=True):
    __tablename__ = "stock_basic_info"
    __table_args__ = (
        Index("idx_exchange", "exchange"),
        Index("idx_industry", "industry"),
        Index("idx_listing_date", "listing_date"),
        Index("idx_province", "province"),
        UniqueConstraint("symbol", name="uniq_symbol"),
        UniqueConstraint("symbol_full", name="uniq_symbol_full"),
    )