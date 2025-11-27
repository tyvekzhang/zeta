# SPDX-License-Identifier: MIT
"""ReportIncomeStatement mapper"""

from __future__ import annotations

from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from fastlib.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.report_income_statement_model import ReportIncomeStatementModel


class ReportIncomeStatementMapper(SqlModelMapper[ReportIncomeStatementModel]):

    async def select_by_announcement_date(
        self, *, announcement_date: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[ReportIncomeStatementModel]:
        """
        Retrieve a record by announcement_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.announcement_date == announcement_date)
        )
        return result.one_or_none()

    async def select_by_announcement_date_list(
        self, *, announcement_date_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[ReportIncomeStatementModel]:
        """
        Retrieve records by list of announcement_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.announcement_date.in_(announcement_date_list))
        )
        return result.all()


    async def select_by_net_profit_yoy(
        self, *, net_profit_yoy: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[ReportIncomeStatementModel]:
        """
        Retrieve a record by net_profit_yoy.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.net_profit_yoy == net_profit_yoy)
        )
        return result.one_or_none()

    async def select_by_net_profit_yoy_list(
        self, *, net_profit_yoy_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[ReportIncomeStatementModel]:
        """
        Retrieve records by list of net_profit_yoy.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.net_profit_yoy.in_(net_profit_yoy_list))
        )
        return result.all()


    async def select_by_stock_code(
        self, *, stock_code: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[ReportIncomeStatementModel]:
        """
        Retrieve a record by stock_code.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.stock_code == stock_code)
        )
        return result.one_or_none()

    async def select_by_stock_code_list(
        self, *, stock_code_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[ReportIncomeStatementModel]:
        """
        Retrieve records by list of stock_code.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.stock_code.in_(stock_code_list))
        )
        return result.all()



reportIncomeStatementMapper = ReportIncomeStatementMapper(ReportIncomeStatementModel)