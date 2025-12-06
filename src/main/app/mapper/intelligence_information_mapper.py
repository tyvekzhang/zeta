# SPDX-License-Identifier: MIT
"""IntelligenceInformation mapper"""

from __future__ import annotations

from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from fastlib.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.intelligence_information_model import IntelligenceInformationModel


class IntelligenceInformationMapper(SqlModelMapper[IntelligenceInformationModel]):

    async def select_by_publish_time(
        self, *, publish_time: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[IntelligenceInformationModel]:
        """
        Retrieve a record by publish_time.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.publish_time == publish_time)
        )
        return result.one_or_none()

    async def select_by_publish_time_list(
        self, *, publish_time_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[IntelligenceInformationModel]:
        """
        Retrieve records by list of publish_time.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.publish_time.in_(publish_time_list))
        )
        return result.all()




intelligenceInformationMapper = IntelligenceInformationMapper(IntelligenceInformationModel)