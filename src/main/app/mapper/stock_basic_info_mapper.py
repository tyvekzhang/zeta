# SPDX-License-Identifier: MIT
"""StockBasicInfo mapper"""

from __future__ import annotations

from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from fastlib.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.stock_basic_info_model import StockBasicInfoModel


class StockBasicInfoMapper(SqlModelMapper[StockBasicInfoModel]):
    
    async def select_all_symbols(
        self, db_session: Optional[AsyncSession] = None
    ) -> list[dict]:
        """
        获取所有已存在的股票代码
        
        Returns:
            list[dict]: 包含symbol字段的字典列表
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model.symbol)
        )
        symbols = result.all()
        return [{"symbol": symbol} for symbol in symbols]

    async def select_by_exchange(
        self, *, exchange: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockBasicInfoModel]:
        """
        Retrieve a record by exchange.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.exchange == exchange)
        )
        return result.one_or_none()

    async def select_by_exchange_list(
        self, *, exchange_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[StockBasicInfoModel]:
        """
        Retrieve records by list of exchange.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.exchange.in_(exchange_list))
        )
        return result.all()


    async def select_by_industry(
        self, *, industry: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockBasicInfoModel]:
        """
        Retrieve a record by industry.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.industry == industry)
        )
        return result.one_or_none()

    async def select_by_industry_list(
        self, *, industry_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[StockBasicInfoModel]:
        """
        Retrieve records by list of industry.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.industry.in_(industry_list))
        )
        return result.all()


    async def select_by_symbol(
        self, *, symbol: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockBasicInfoModel]:
        """
        Retrieve a record by symbol.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.symbol == symbol)
        )
        return result.one_or_none()

    async def select_by_symbol_list(
        self, *, symbol_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[StockBasicInfoModel]:
        """
        Retrieve records by list of symbol.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.symbol.in_(symbol_list))
        )
        return result.all()


    async def select_by_symbol_full(
        self, *, symbol_full: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockBasicInfoModel]:
        """
        Retrieve a record by symbol_full.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.symbol_full == symbol_full)
        )
        return result.one_or_none()

    async def select_by_symbol_full_list(
        self, *, symbol_full_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[StockBasicInfoModel]:
        """
        Retrieve records by list of symbol_full.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.symbol_full.in_(symbol_full_list))
        )
        return result.all()



stockBasicInfoMapper = StockBasicInfoMapper(StockBasicInfoModel)