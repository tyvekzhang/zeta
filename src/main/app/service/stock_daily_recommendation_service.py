# SPDX-License-Identifier: MIT
"""StockDailyRecommendation Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from fastlib.service.base_service import BaseService
from src.main.app.model.stock_daily_recommendation_model import StockDailyRecommendationModel
from src.main.app.schema.stock_daily_recommendation_schema import (
    ListStockDailyRecommendationsRequest,
    CreateStockDailyRecommendationRequest,
    StockDailyRecommendation,
    UpdateStockDailyRecommendationRequest,
    BatchDeleteStockDailyRecommendationsRequest,
    ExportStockDailyRecommendationsRequest,
    BatchCreateStockDailyRecommendationsRequest,
    BatchUpdateStockDailyRecommendationsRequest,
    ImportStockDailyRecommendationsRequest,
    ImportStockDailyRecommendation,
    BatchPatchStockDailyRecommendationsRequest,
)


class StockDailyRecommendationService(BaseService[StockDailyRecommendationModel], ABC):
    @abstractmethod
    async def get_stock_daily_recommendation(
        self,
        *,
        id: int,
    ) -> StockDailyRecommendationModel: ...

    @abstractmethod
    async def list_stock_daily_recommendations(
        self, *, req: ListStockDailyRecommendationsRequest
    ) -> tuple[list[StockDailyRecommendationModel], int]: ...

    

    @abstractmethod
    async def create_stock_daily_recommendation(self, *, req: CreateStockDailyRecommendationRequest) -> StockDailyRecommendationModel: ...

    @abstractmethod
    async def update_stock_daily_recommendation(self, req: UpdateStockDailyRecommendationRequest) -> StockDailyRecommendationModel: ...

    @abstractmethod
    async def delete_stock_daily_recommendation(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_stock_daily_recommendations(self, ids: list[int]) -> list[StockDailyRecommendationModel]: ...

    @abstractmethod
    async def batch_create_stock_daily_recommendations(
        self,
        *,
        req: BatchCreateStockDailyRecommendationsRequest,
    ) -> list[StockDailyRecommendationModel]: ...

    @abstractmethod
    async def batch_update_stock_daily_recommendations(
        self, req: BatchUpdateStockDailyRecommendationsRequest
    ) -> list[StockDailyRecommendationModel]: ...

    @abstractmethod
    async def batch_patch_stock_daily_recommendations(
        self, req: BatchPatchStockDailyRecommendationsRequest
    ) -> list[StockDailyRecommendationModel]: ...

    @abstractmethod
    async def batch_delete_stock_daily_recommendations(self, req: BatchDeleteStockDailyRecommendationsRequest): ...

    @abstractmethod
    async def export_stock_daily_recommendations_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_stock_daily_recommendations(
        self, req: ExportStockDailyRecommendationsRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_stock_daily_recommendations(
        self, req: ImportStockDailyRecommendationsRequest
    ) -> list[ImportStockDailyRecommendation]: ...