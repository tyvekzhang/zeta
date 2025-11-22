# SPDX-License-Identifier: MIT
"""SectorCapitalFlow mapper"""

from __future__ import annotations

from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from fastlib.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.sector_capital_flow_model import SectorCapitalFlowModel


class SectorCapitalFlowMapper(SqlModelMapper[SectorCapitalFlowModel]):

    async def select_by_change_percent(
        self, *, change_percent: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[SectorCapitalFlowModel]:
        """
        Retrieve a record by change_percent.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.change_percent == change_percent)
        )
        return result.one_or_none()

    async def select_by_change_percent_list(
        self, *, change_percent_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[SectorCapitalFlowModel]:
        """
        Retrieve records by list of change_percent.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.change_percent.in_(change_percent_list))
        )
        return result.all()


    async def select_by_sector_type(
        self, *, sector_type: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[SectorCapitalFlowModel]:
        """
        Retrieve a record by sector_type.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.sector_type == sector_type)
        )
        return result.one_or_none()

    async def select_by_sector_type_list(
        self, *, sector_type_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[SectorCapitalFlowModel]:
        """
        Retrieve records by list of sector_type.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.sector_type.in_(sector_type_list))
        )
        return result.all()


    async def select_by_trade_date, sector_code(
        self, *, trade_date, sector_code: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[SectorCapitalFlowModel]:
        """
        Retrieve a record by trade_date, sector_code.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.trade_date, sector_code == trade_date, sector_code)
        )
        return result.one_or_none()

    async def select_by_trade_date, sector_code_list(
        self, *, trade_date, sector_code_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[SectorCapitalFlowModel]:
        """
        Retrieve records by list of trade_date, sector_code.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.trade_date, sector_code.in_(trade_date, sector_code_list))
        )
        return result.all()


    async def select_by_sector_code, trade_date(
        self, *, sector_code, trade_date: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[SectorCapitalFlowModel]:
        """
        Retrieve a record by sector_code, trade_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.sector_code, trade_date == sector_code, trade_date)
        )
        return result.one_or_none()

    async def select_by_sector_code, trade_date_list(
        self, *, sector_code, trade_date_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[SectorCapitalFlowModel]:
        """
        Retrieve records by list of sector_code, trade_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.sector_code, trade_date.in_(sector_code, trade_date_list))
        )
        return result.all()



sectorCapitalFlowMapper = SectorCapitalFlowMapper(SectorCapitalFlowModel)