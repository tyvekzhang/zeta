# SPDX-License-Identifier: MIT
"""Stock Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from fastlib.service.base_service import BaseService
from src.main.app.model.stock_model import StockModel
from src.main.app.schema.stock_schema import (
    ListStocksRequest,
    CreateStockRequest,
    Stock,
    UpdateStockRequest,
    BatchDeleteStocksRequest,
    ExportStocksRequest,
    BatchCreateStocksRequest,
    BatchUpdateStocksRequest,
    ImportStocksRequest,
    ImportStock,
    BatchPatchStocksRequest,
)


class StockService(BaseService[StockModel], ABC):
    
    @abstractmethod
    async def sync_manually(
        self,
    ) -> None:
        pass
    
    @abstractmethod
    async def get_stock(
        self,
        *,
        id: int,
    ) -> StockModel: ...

    @abstractmethod
    async def list_stocks(
        self, *, req: ListStocksRequest
    ) -> tuple[list[StockModel], int]: ...

    

    @abstractmethod
    async def create_stock(self, *, req: CreateStockRequest) -> StockModel: ...

    @abstractmethod
    async def update_stock(self, req: UpdateStockRequest) -> StockModel: ...

    @abstractmethod
    async def delete_stock(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_stocks(self, ids: list[int]) -> list[StockModel]: ...

    @abstractmethod
    async def batch_create_stocks(
        self,
        *,
        req: BatchCreateStocksRequest,
    ) -> list[StockModel]: ...

    @abstractmethod
    async def batch_update_stocks(
        self, req: BatchUpdateStocksRequest
    ) -> list[StockModel]: ...

    @abstractmethod
    async def batch_patch_stocks(
        self, req: BatchPatchStocksRequest
    ) -> list[StockModel]: ...

    @abstractmethod
    async def batch_delete_stocks(self, req: BatchDeleteStocksRequest): ...

    @abstractmethod
    async def export_stocks_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_stocks(
        self, req: ExportStocksRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_stocks(
        self, req: ImportStocksRequest
    ) -> list[ImportStock]: ...