# SPDX-License-Identifier: MIT
"""Stock mapper"""

from __future__ import annotations

from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from fastlib.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.stock_model import StockModel


class StockMapper(SqlModelMapper[StockModel]):
    
    async def select_all_stocks(
        self, db_session: Optional[AsyncSession] = None
    ) -> list[dict]:
        """
        获取所有已存在的股票代码
        
        Returns:
            list[dict]: 包含stock_code字段的字典列表
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model.stock_code)
        )
        stock_codes = result.all()
        return [{"stock_code": stock_code} for stock_code in stock_codes]

    async def select_by_exchange(
        self, *, exchange: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockModel]:
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
    ) -> list[StockModel]:
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
    ) -> Optional[StockModel]:
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
    ) -> list[StockModel]:
        """
        Retrieve records by list of industry.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.industry.in_(industry_list))
        )
        return result.all()


    async def select_by_listing_date(
        self, *, listing_date: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockModel]:
        """
        Retrieve a record by listing_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.listing_date == listing_date)
        )
        return result.one_or_none()

    async def select_by_listing_date_list(
        self, *, listing_date_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[StockModel]:
        """
        Retrieve records by list of listing_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.listing_date.in_(listing_date_list))
        )
        return result.all()


    async def select_by_province(
        self, *, province: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockModel]:
        """
        Retrieve a record by province.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.province == province)
        )
        return result.one_or_none()

    async def select_by_province_list(
        self, *, province_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[StockModel]:
        """
        Retrieve records by list of province.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.province.in_(province_list))
        )
        return result.all()


    async def select_by_stock_code(
        self, *, stock_code: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockModel]:
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
    ) -> list[StockModel]:
        """
        Retrieve records by list of stock_code.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.stock_code.in_(stock_code_list))
        )
        return result.all()



stockMapper = StockMapper(StockModel)