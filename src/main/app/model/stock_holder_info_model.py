# SPDX-License-Identifier: MIT
"""StockHolderInfo data model"""

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


class StockHolderInfoBase(SQLModel):
    
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
    holder_name: Optional[str] = Field(
        sa_column=Column(
            String(200),
            nullable=True,
            comment="股东名称"
        )
    )
    holder_info: Optional[str] = Field(
        sa_column=Column(
            String(512),
            nullable=True,
            comment="股东信息"
        )
    )
    holder_type: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="股东类型(1:机构, 2:个人, 3:基金, 4:券商, 5:保险, 6:其他)"
        )
    )
    share_amount: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="持股数量"
        )
    )
    share_ratio: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="持股比例"
        )
    )
    change_amount: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="持股变动数量"
        )
    )
    change_type: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="变动类型(1:增持, 2:减持, 3:不变, 4:新进)"
        )
    )
    report_date: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="报告日期"
        )
    )
    is_top_ten: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="是否十大股东"
        )
    )
    ranking: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="股东排名"
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


class StockHolderInfoModel(StockHolderInfoBase, table=True):
    __tablename__ = "stock_holder_info"
    __table_args__ = (
        Index("idx_holder", "holder_name"),
        Index("idx_stock_date", "stock_symbol_full", "report_date"),
    )