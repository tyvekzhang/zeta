# SPDX-License-Identifier: MIT
"""StockCapitalFlow mapper"""

from __future__ import annotations

from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from fastlib.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.stock_capital_flow_model import StockCapitalFlowModel


class StockCapitalFlowMapper(SqlModelMapper[StockCapitalFlowModel]):

    async def select_by_stock_symbol_full(
        self, *, stock_symbol_full: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockCapitalFlowModel]:
        """
        Retrieve a record by stock_symbol_full.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.stock_symbol_full == stock_symbol_full)
        )
        return result.one_or_none()

    async def select_by_stock_symbol_full_list(
        self, *, stock_symbol_full_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[StockCapitalFlowModel]:
        """
        Retrieve records by list of stock_symbol_full.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.stock_symbol_full.in_(stock_symbol_full_list))
        )
        return result.all()


    async def select_by_trade_date(
        self, *, trade_date: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockCapitalFlowModel]:
        """
        Retrieve a record by trade_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.trade_date == trade_date)
        )
        return result.one_or_none()

    async def select_by_trade_date_list(
        self, *, trade_date_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[StockCapitalFlowModel]:
        """
        Retrieve records by list of trade_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.trade_date.in_(trade_date_list))
        )
        return result.all()



stockCapitalFlowMapper = StockCapitalFlowMapper(StockCapitalFlowModel)