# SPDX-License-Identifier: MIT
"""StockFinancialReport Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from fastlib.service.base_service import BaseService
from src.main.app.model.stock_financial_report_model import StockFinancialReportModel
from src.main.app.schema.stock_financial_report_schema import (
    ListStockFinancialReportsRequest,
    CreateStockFinancialReportRequest,
    StockFinancialReport,
    UpdateStockFinancialReportRequest,
    BatchDeleteStockFinancialReportsRequest,
    ExportStockFinancialReportsRequest,
    BatchCreateStockFinancialReportsRequest,
    BatchUpdateStockFinancialReportsRequest,
    ImportStockFinancialReportsRequest,
    ImportStockFinancialReport,
    BatchPatchStockFinancialReportsRequest,
)


class StockFinancialReportService(BaseService[StockFinancialReportModel], ABC):
    @abstractmethod
    async def get_stock_financial_report(
        self,
        *,
        id: int,
    ) -> StockFinancialReportModel: ...

    @abstractmethod
    async def list_stock_financial_reports(
        self, *, req: ListStockFinancialReportsRequest
    ) -> tuple[list[StockFinancialReportModel], int]: ...

    

    @abstractmethod
    async def create_stock_financial_report(self, *, req: CreateStockFinancialReportRequest) -> StockFinancialReportModel: ...

    @abstractmethod
    async def update_stock_financial_report(self, req: UpdateStockFinancialReportRequest) -> StockFinancialReportModel: ...

    @abstractmethod
    async def delete_stock_financial_report(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_stock_financial_reports(self, ids: list[int]) -> list[StockFinancialReportModel]: ...

    @abstractmethod
    async def batch_create_stock_financial_reports(
        self,
        *,
        req: BatchCreateStockFinancialReportsRequest,
    ) -> list[StockFinancialReportModel]: ...

    @abstractmethod
    async def batch_update_stock_financial_reports(
        self, req: BatchUpdateStockFinancialReportsRequest
    ) -> list[StockFinancialReportModel]: ...

    @abstractmethod
    async def batch_patch_stock_financial_reports(
        self, req: BatchPatchStockFinancialReportsRequest
    ) -> list[StockFinancialReportModel]: ...

    @abstractmethod
    async def batch_delete_stock_financial_reports(self, req: BatchDeleteStockFinancialReportsRequest): ...

    @abstractmethod
    async def export_stock_financial_reports_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_stock_financial_reports(
        self, req: ExportStockFinancialReportsRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_stock_financial_reports(
        self, req: ImportStockFinancialReportsRequest
    ) -> list[ImportStockFinancialReport]: ...