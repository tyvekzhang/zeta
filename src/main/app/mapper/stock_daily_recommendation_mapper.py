# SPDX-License-Identifier: MIT
"""StockDailyRecommendation mapper"""

from __future__ import annotations

from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from fastlib.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.stock_daily_recommendation_model import StockDailyRecommendationModel


class StockDailyRecommendationMapper(SqlModelMapper[StockDailyRecommendationModel]):

    async def select_by_recommend_date(
        self, *, recommend_date: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[StockDailyRecommendationModel]:
        """
        Retrieve a record by recommend_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.recommend_date == recommend_date)
        )
        return result.one_or_none()

    async def select_by_recommend_date_list(
        self, *, recommend_date_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[StockDailyRecommendationModel]:
        """
        Retrieve records by list of recommend_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.recommend_date.in_(recommend_date_list))
        )
        return result.all()



stockDailyRecommendationMapper = StockDailyRecommendationMapper(StockDailyRecommendationModel)