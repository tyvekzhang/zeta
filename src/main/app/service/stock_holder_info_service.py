# SPDX-License-Identifier: MIT
"""StockHolderInfo Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from fastlib.service.base_service import BaseService
from src.main.app.model.stock_holder_info_model import StockHolderInfoModel
from src.main.app.schema.stock_holder_info_schema import (
    ListStockHolderInfosRequest,
    CreateStockHolderInfoRequest,
    StockHolderInfo,
    UpdateStockHolderInfoRequest,
    BatchDeleteStockHolderInfosRequest,
    ExportStockHolderInfosRequest,
    BatchCreateStockHolderInfosRequest,
    BatchUpdateStockHolderInfosRequest,
    ImportStockHolderInfosRequest,
    ImportStockHolderInfo,
    BatchPatchStockHolderInfosRequest,
)


class StockHolderInfoService(BaseService[StockHolderInfoModel], ABC):
    @abstractmethod
    async def get_stock_holder_info(
        self,
        *,
        id: int,
    ) -> StockHolderInfoModel: ...

    @abstractmethod
    async def list_stock_holder_infos(
        self, *, req: ListStockHolderInfosRequest
    ) -> tuple[list[StockHolderInfoModel], int]: ...

    

    @abstractmethod
    async def create_stock_holder_info(self, *, req: CreateStockHolderInfoRequest) -> StockHolderInfoModel: ...

    @abstractmethod
    async def update_stock_holder_info(self, req: UpdateStockHolderInfoRequest) -> StockHolderInfoModel: ...

    @abstractmethod
    async def delete_stock_holder_info(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_stock_holder_infos(self, ids: list[int]) -> list[StockHolderInfoModel]: ...

    @abstractmethod
    async def batch_create_stock_holder_infos(
        self,
        *,
        req: BatchCreateStockHolderInfosRequest,
    ) -> list[StockHolderInfoModel]: ...

    @abstractmethod
    async def batch_update_stock_holder_infos(
        self, req: BatchUpdateStockHolderInfosRequest
    ) -> list[StockHolderInfoModel]: ...

    @abstractmethod
    async def batch_patch_stock_holder_infos(
        self, req: BatchPatchStockHolderInfosRequest
    ) -> list[StockHolderInfoModel]: ...

    @abstractmethod
    async def batch_delete_stock_holder_infos(self, req: BatchDeleteStockHolderInfosRequest): ...

    @abstractmethod
    async def export_stock_holder_infos_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_stock_holder_infos(
        self, req: ExportStockHolderInfosRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_stock_holder_infos(
        self, req: ImportStockHolderInfosRequest
    ) -> list[ImportStockHolderInfo]: ...