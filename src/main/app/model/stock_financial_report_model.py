# SPDX-License-Identifier: MIT
"""StockFinancialReport data model"""

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


class StockFinancialReportBase(SQLModel):
    
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        nullable=False,
        sa_type=BigInteger,sa_column_kwargs={"comment": "主键"}
    )
    file_id: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="文件主键"
        )
    )
    stock_symbol_full: Optional[str] = Field(
        sa_column=Column(
            String(20),
            nullable=True,
            comment="股票代码"
        )
    )
    report_date: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="报告期"
        )
    )
    report_type: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="报告类型(1:一季度, 2:年中, 3:三季度, 4:年终)"
        )
    )
    total_revenue: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="营业收入（分）"
        )
    )
    net_profit: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="净利润（分）"
        )
    )
    total_assets: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="总资产（分）"
        )
    )
    total_liabilities: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="总负债（分）"
        )
    )
    net_assets: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="净资产（分）"
        )
    )
    eps: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="每股收益（分）"
        )
    )
    roe: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="净资产收益率"
        )
    )
    gross_profit_margin: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="毛利率"
        )
    )
    report_source: Optional[str] = Field(
        sa_column=Column(
            String(100),
            nullable=True,
            comment="报告来源"
        )
    )
    earnings_announcement_date: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="预约披露日期"
        )
    )
    published_date: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="发布日期"
        )
    )
    comment: Optional[str] = Field(
        sa_column=Column(
            String,
            nullable=True,
            comment="备注"
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


class StockFinancialReportModel(StockFinancialReportBase, table=True):
    __tablename__ = "stock_financial_report"
    __table_args__ = (
        Index("idx_stock_date", stock_symbol_full, report_date),
    )