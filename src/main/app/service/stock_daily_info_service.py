# SPDX-License-Identifier: MIT
"""StockDailyInfo Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from fastlib.service.base_service import BaseService
from src.main.app.model.stock_daily_info_model import StockDailyInfoModel
from src.main.app.schema.stock_daily_info_schema import (
    ListStockDailyInfosRequest,
    CreateStockDailyInfoRequest,
    StockDailyInfo,
    UpdateStockDailyInfoRequest,
    BatchDeleteStockDailyInfosRequest,
    ExportStockDailyInfosRequest,
    BatchCreateStockDailyInfosRequest,
    BatchUpdateStockDailyInfosRequest,
    ImportStockDailyInfosRequest,
    ImportStockDailyInfo,
    BatchPatchStockDailyInfosRequest,
)


class StockDailyInfoService(BaseService[StockDailyInfoModel], ABC):
    @abstractmethod
    async def get_stock_daily_info(
        self,
        *,
        id: int,
    ) -> StockDailyInfoModel: ...

    @abstractmethod
    async def list_stock_daily_infos(
        self, *, req: ListStockDailyInfosRequest
    ) -> tuple[list[StockDailyInfoModel], int]: ...

    

    @abstractmethod
    async def create_stock_daily_info(self, *, req: CreateStockDailyInfoRequest) -> StockDailyInfoModel: ...

    @abstractmethod
    async def update_stock_daily_info(self, req: UpdateStockDailyInfoRequest) -> StockDailyInfoModel: ...

    @abstractmethod
    async def delete_stock_daily_info(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_stock_daily_infos(self, ids: list[int]) -> list[StockDailyInfoModel]: ...

    @abstractmethod
    async def batch_create_stock_daily_infos(
        self,
        *,
        req: BatchCreateStockDailyInfosRequest,
    ) -> list[StockDailyInfoModel]: ...

    @abstractmethod
    async def batch_update_stock_daily_infos(
        self, req: BatchUpdateStockDailyInfosRequest
    ) -> list[StockDailyInfoModel]: ...

    @abstractmethod
    async def batch_patch_stock_daily_infos(
        self, req: BatchPatchStockDailyInfosRequest
    ) -> list[StockDailyInfoModel]: ...

    @abstractmethod
    async def batch_delete_stock_daily_infos(self, req: BatchDeleteStockDailyInfosRequest): ...

    @abstractmethod
    async def export_stock_daily_infos_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_stock_daily_infos(
        self, req: ExportStockDailyInfosRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_stock_daily_infos(
        self, req: ImportStockDailyInfosRequest
    ) -> list[ImportStockDailyInfo]: ...