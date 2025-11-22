# SPDX-License-Identifier: MIT
"""StockBasicInfo Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from fastlib.service.base_service import BaseService
from src.main.app.model.stock_basic_info_model import StockBasicInfoModel
from src.main.app.schema.stock_basic_info_schema import (
    ListStockBasicInfosRequest,
    CreateStockBasicInfoRequest,
    StockBasicInfo,
    UpdateStockBasicInfoRequest,
    BatchDeleteStockBasicInfosRequest,
    ExportStockBasicInfosRequest,
    BatchCreateStockBasicInfosRequest,
    BatchUpdateStockBasicInfosRequest,
    ImportStockBasicInfosRequest,
    ImportStockBasicInfo,
    BatchPatchStockBasicInfosRequest,
)


class StockBasicInfoService(BaseService[StockBasicInfoModel], ABC):

    @abstractmethod
    async def sync_manually(
        self,
    ) -> None:
        pass

    @abstractmethod
    async def get_stock_basic_info(
        self,
        *,
        id: int,
    ) -> StockBasicInfoModel: ...

    @abstractmethod
    async def list_stock_basic_infos(
        self, *, req: ListStockBasicInfosRequest
    ) -> tuple[list[StockBasicInfoModel], int]: ...

    @abstractmethod
    async def create_stock_basic_info(
        self, *, req: CreateStockBasicInfoRequest
    ) -> StockBasicInfoModel: ...

    @abstractmethod
    async def update_stock_basic_info(
        self, req: UpdateStockBasicInfoRequest
    ) -> StockBasicInfoModel: ...

    @abstractmethod
    async def delete_stock_basic_info(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_stock_basic_infos(
        self, ids: list[int]
    ) -> list[StockBasicInfoModel]: ...

    @abstractmethod
    async def batch_create_stock_basic_infos(
        self,
        *,
        req: BatchCreateStockBasicInfosRequest,
    ) -> list[StockBasicInfoModel]: ...

    @abstractmethod
    async def batch_update_stock_basic_infos(
        self, req: BatchUpdateStockBasicInfosRequest
    ) -> list[StockBasicInfoModel]: ...

    @abstractmethod
    async def batch_patch_stock_basic_infos(
        self, req: BatchPatchStockBasicInfosRequest
    ) -> list[StockBasicInfoModel]: ...

    @abstractmethod
    async def batch_delete_stock_basic_infos(
        self, req: BatchDeleteStockBasicInfosRequest
    ): ...

    @abstractmethod
    async def export_stock_basic_infos_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_stock_basic_infos(
        self, req: ExportStockBasicInfosRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_stock_basic_infos(
        self, req: ImportStockBasicInfosRequest
    ) -> list[ImportStockBasicInfo]: ...
