# SPDX-License-Identifier: MIT
"""StockCapitalFlow Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from fastlib.service.base_service import BaseService
from src.main.app.model.stock_capital_flow_model import StockCapitalFlowModel
from src.main.app.schema.stock_capital_flow_schema import (
    ListStockCapitalFlowsRequest,
    CreateStockCapitalFlowRequest,
    StockCapitalFlow,
    UpdateStockCapitalFlowRequest,
    BatchDeleteStockCapitalFlowsRequest,
    ExportStockCapitalFlowsRequest,
    BatchCreateStockCapitalFlowsRequest,
    BatchUpdateStockCapitalFlowsRequest,
    ImportStockCapitalFlowsRequest,
    ImportStockCapitalFlow,
    BatchPatchStockCapitalFlowsRequest,
)


class StockCapitalFlowService(BaseService[StockCapitalFlowModel], ABC):
    @abstractmethod
    async def get_stock_capital_flow(
        self,
        *,
        id: int,
    ) -> StockCapitalFlowModel: ...

    @abstractmethod
    async def list_stock_capital_flows(
        self, *, req: ListStockCapitalFlowsRequest
    ) -> tuple[list[StockCapitalFlowModel], int]: ...

    

    @abstractmethod
    async def create_stock_capital_flow(self, *, req: CreateStockCapitalFlowRequest) -> StockCapitalFlowModel: ...

    @abstractmethod
    async def update_stock_capital_flow(self, req: UpdateStockCapitalFlowRequest) -> StockCapitalFlowModel: ...

    @abstractmethod
    async def delete_stock_capital_flow(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_stock_capital_flows(self, ids: list[int]) -> list[StockCapitalFlowModel]: ...

    @abstractmethod
    async def batch_create_stock_capital_flows(
        self,
        *,
        req: BatchCreateStockCapitalFlowsRequest,
    ) -> list[StockCapitalFlowModel]: ...

    @abstractmethod
    async def batch_update_stock_capital_flows(
        self, req: BatchUpdateStockCapitalFlowsRequest
    ) -> list[StockCapitalFlowModel]: ...

    @abstractmethod
    async def batch_patch_stock_capital_flows(
        self, req: BatchPatchStockCapitalFlowsRequest
    ) -> list[StockCapitalFlowModel]: ...

    @abstractmethod
    async def batch_delete_stock_capital_flows(self, req: BatchDeleteStockCapitalFlowsRequest): ...

    @abstractmethod
    async def export_stock_capital_flows_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_stock_capital_flows(
        self, req: ExportStockCapitalFlowsRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_stock_capital_flows(
        self, req: ImportStockCapitalFlowsRequest
    ) -> list[ImportStockCapitalFlow]: ...