# SPDX-License-Identifier: MIT
"""ReportIncomeStatement Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from fastlib.service.base_service import BaseService
from src.main.app.model.report_income_statement_model import ReportIncomeStatementModel
from src.main.app.schema.report_income_statement_schema import (
    ListReportIncomeStatementsRequest,
    CreateReportIncomeStatementRequest,
    ReportIncomeStatement,
    UpdateReportIncomeStatementRequest,
    BatchDeleteReportIncomeStatementsRequest,
    ExportReportIncomeStatementsRequest,
    BatchCreateReportIncomeStatementsRequest,
    BatchUpdateReportIncomeStatementsRequest,
    ImportReportIncomeStatementsRequest,
    ImportReportIncomeStatement,
    BatchPatchReportIncomeStatementsRequest,
)


class ReportIncomeStatementService(BaseService[ReportIncomeStatementModel], ABC):
    
    @abstractmethod
    async def sync_manually(
        self, year: int, quarter: int
    ) -> None:
        pass
    
    @abstractmethod
    async def get_report_income_statement(
        self,
        *,
        id: int,
    ) -> ReportIncomeStatementModel: ...

    @abstractmethod
    async def list_report_income_statements(
        self, *, req: ListReportIncomeStatementsRequest
    ) -> tuple[list[ReportIncomeStatementModel], int]: ...

    

    @abstractmethod
    async def create_report_income_statement(self, *, req: CreateReportIncomeStatementRequest) -> ReportIncomeStatementModel: ...

    @abstractmethod
    async def update_report_income_statement(self, req: UpdateReportIncomeStatementRequest) -> ReportIncomeStatementModel: ...

    @abstractmethod
    async def delete_report_income_statement(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_report_income_statements(self, ids: list[int]) -> list[ReportIncomeStatementModel]: ...

    @abstractmethod
    async def batch_create_report_income_statements(
        self,
        *,
        req: BatchCreateReportIncomeStatementsRequest,
    ) -> list[ReportIncomeStatementModel]: ...

    @abstractmethod
    async def batch_update_report_income_statements(
        self, req: BatchUpdateReportIncomeStatementsRequest
    ) -> list[ReportIncomeStatementModel]: ...

    @abstractmethod
    async def batch_patch_report_income_statements(
        self, req: BatchPatchReportIncomeStatementsRequest
    ) -> list[ReportIncomeStatementModel]: ...

    @abstractmethod
    async def batch_delete_report_income_statements(self, req: BatchDeleteReportIncomeStatementsRequest): ...

    @abstractmethod
    async def export_report_income_statements_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_report_income_statements(
        self, req: ExportReportIncomeStatementsRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_report_income_statements(
        self, req: ImportReportIncomeStatementsRequest
    ) -> list[ImportReportIncomeStatement]: ...