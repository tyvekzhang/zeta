# SPDX-License-Identifier: MIT
"""ReportIncomeStatement data model"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import (
    BigInteger,
    Float,
    SQLModel,
    Field,
    Column,
    DateTime,
    Index,
    DateTime,
    Float,
    String,
)

from fastlib.utils.snowflake_util import snowflake_id


class ReportIncomeStatementBase(SQLModel):

    id: float = Field(
        default_factory=snowflake_id,
        primary_key=True,
        nullable=False,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    stock_code: Optional[str] = Field(
        sa_column=Column(String(20), nullable=True, comment="股票代码")
    )
    stock_name: Optional[str] = Field(
        sa_column=Column(String(100), nullable=True, comment="股票简称")
    )
    exchange: Optional[str] = Field(
        sa_column=Column(
            String(10),
            nullable=True,
            comment="交易所(SH=上交所, SZ=深交所, HK=港股, US=美股)",
        )
    )
    net_profit: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="净利润(元)")
    )
    net_profit_yoy: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="净利润同比(%)")
    )
    total_operating_income: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="营业总收入(元)")
    )
    total_operating_income_yoy: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="营业总收入同比(%)")
    )
    operating_expenses: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="营业总支出-营业支出(元)")
    )
    sales_expenses: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="营业总支出-销售费用(元)")
    )
    management_expenses: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="营业总支出-管理费用(元)")
    )
    financial_expenses: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="营业总支出-财务费用(元)")
    )
    total_operating_expenses: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="营业总支出-营业总支出(元)")
    )
    operating_profit: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="营业利润(元)")
    )
    total_profit: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="利润总额(元)")
    )
    announcement_date: Optional[datetime] = Field(
        sa_column=Column(DateTime, nullable=True, comment="公告日期")
    )
    year: Optional[float] = Field(sa_column=Column(Float, nullable=True, comment="年份"))
    quarter: Optional[float] = Field(
        sa_column=Column(Float, nullable=True, comment="季度")
    )
    created_at: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"comment": "创建时间"},
    )
    updated_at: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
            "comment": "更新时间",
        },
    )


class ReportIncomeStatementModel(ReportIncomeStatementBase, table=True):
    __tablename__ = "report_income_statement"
    __table_args__ = (
        Index("idx_announcement_date", "announcement_date"),
        Index("idx_net_profit_yoy", "net_profit_yoy"),
        Index("idx_stock_code", "stock_code"),
        {"comment": "利润表"},
    )
