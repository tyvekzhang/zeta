# SPDX-License-Identifier: MIT
"""StockHolderInfo mapper"""

from __future__ import annotations

from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from fastlib.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.stock_holder_info_model import StockHolderInfoModel


class StockHolderInfoMapper(SqlModelMapper[StockHolderInfoModel]):

    async def select_by_holder_name(
        self, *, holder_name: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockHolderInfoModel]:
        """
        Retrieve a record by holder_name.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.holder_name == holder_name)
        )
        return result.one_or_none()

    async def select_by_holder_name_list(
        self, *, holder_name_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[StockHolderInfoModel]:
        """
        Retrieve records by list of holder_name.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.holder_name.in_(holder_name_list))
        )
        return result.all()


stockHolderInfoMapper = StockHolderInfoMapper(StockHolderInfoModel)