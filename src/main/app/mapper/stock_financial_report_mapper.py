# SPDX-License-Identifier: MIT
"""StockFinancialReport mapper"""

from __future__ import annotations

from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from fastlib.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.stock_financial_report_model import StockFinancialReportModel


class StockFinancialReportMapper(SqlModelMapper[StockFinancialReportModel]):

    async def select_by_stock_symbol_full, report_date(
        self, *, stock_symbol_full, report_date: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockFinancialReportModel]:
        """
        Retrieve a record by stock_symbol_full, report_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.stock_symbol_full, report_date == stock_symbol_full, report_date)
        )
        return result.one_or_none()

    async def select_by_stock_symbol_full, report_date_list(
        self, *, stock_symbol_full, report_date_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[StockFinancialReportModel]:
        """
        Retrieve records by list of stock_symbol_full, report_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.stock_symbol_full, report_date.in_(stock_symbol_full, report_date_list))
        )
        return result.all()



stockFinancialReportMapper = StockFinancialReportMapper(StockFinancialReportModel)