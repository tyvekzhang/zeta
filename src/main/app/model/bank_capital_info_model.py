# SPDX-License-Identifier: MIT
"""BankCapitalInfo data model"""

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


class BankCapitalInfoBase(SQLModel):
    
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        nullable=False,
        sa_type=BigInteger,sa_column_kwargs={"comment": "主键ID"}
    )
    trade_date: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="交易日期"
        )
    )
    bank_code: Optional[str] = Field(
        sa_column=Column(
            String(16),
            nullable=True,
            comment="银行代码"
        )
    )
    bank_name: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            comment="银行名称"
        )
    )
    bank_type: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="银行类型(1-国有行 2-股份制 3-城商行 4-农商行 5-政策性)"
        )
    )
    total_deposits: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="存款总额(元)"
        )
    )
    total_loans: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="贷款总额(元)"
        )
    )
    non_performing_loan_ratio: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="不良贷款率(×10000)"
        )
    )
    loan_loss_provision_ratio: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="拨备覆盖率(×10000)"
        )
    )
    net_interest_margin: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="净息差(×10000)"
        )
    )
    capital_adequacy_ratio: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="资本充足率(×10000)"
        )
    )
    tier1_capital_ratio: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="一级资本充足率(×10000)"
        )
    )
    core_tier1_ratio: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='0',comment="核心一级资本充足率(×10000)"
        )
    )
    data_source: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='1',comment="数据来源(1-银保监会 2-央行 3-银行财报)"
        )
    )
    data_frequency: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default='1',comment="频率(1-日 2-周 3-月 4-季)"
        )
    )
    created_at: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={
            "onupdate":lambda: datetime.now(timezone.utc),
        },
    )


class BankCapitalInfoModel(BankCapitalInfoBase, table=True):
    __tablename__ = "bank_capital_info"
    __table_args__ = (
        Index("idx_bank_code", "bank_code"),
        Index("idx_bank_type", "bank_type"),
        Index("idx_trade_date", "trade_date"),
    )