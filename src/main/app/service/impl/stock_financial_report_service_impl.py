# SPDX-License-Identifier: MIT
"""StockFinancialReport domain service impl"""

from __future__ import annotations

import io
import json
from typing import Type, Any

import pandas as pd
from loguru import logger
from pydantic import ValidationError
from starlette.responses import StreamingResponse

from fastlib.constants import FilterOperators
from fastlib.service.impl.base_service_impl import BaseServiceImpl
from fastlib.utils import excel_util
from fastlib.utils.validate_util import ValidateService
from src.main.app.exception.biz_exception import BusinessErrorCode
from src.main.app.exception.biz_exception import BusinessException
from src.main.app.mapper.stock_financial_report_mapper import StockFinancialReportMapper
from src.main.app.model.stock_financial_report_model import StockFinancialReportModel
from src.main.app.schema.stock_financial_report_schema import (
    ListStockFinancialReportsRequest,
    StockFinancialReport,
    CreateStockFinancialReportRequest,
    UpdateStockFinancialReportRequest,
    BatchDeleteStockFinancialReportsRequest,
    ExportStockFinancialReportsRequest,
    BatchCreateStockFinancialReportsRequest,
    CreateStockFinancialReport,
    BatchUpdateStockFinancialReportsRequest,
    UpdateStockFinancialReport,
    ImportStockFinancialReportsRequest,
    ImportStockFinancialReport,
    ExportStockFinancialReport,
    BatchPatchStockFinancialReportsRequest,
    BatchUpdateStockFinancialReport,
)
from src.main.app.service.stock_financial_report_service import StockFinancialReportService


class StockFinancialReportServiceImpl(BaseServiceImpl[StockFinancialReportMapper, StockFinancialReportModel], StockFinancialReportService):
    """
    Implementation of the StockFinancialReportService interface.
    """

    def __init__(self, mapper: StockFinancialReportMapper):
        """
        Initialize the StockFinancialReportServiceImpl instance.

        Args:
            mapper (StockFinancialReportMapper): The StockFinancialReportMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper, model=StockFinancialReportModel)
        self.mapper = mapper

    async def get_stock_financial_report(
        self,
        *,
        id: int,
    ) -> StockFinancialReportModel:
        stock_financial_report_record: StockFinancialReportModel = await self.mapper.select_by_id(id=id)
        if stock_financial_report_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return stock_financial_report_record

    async def list_stock_financial_reports(
        self, req: ListStockFinancialReportsRequest
    ) -> tuple[list[StockFinancialReportModel], int]:
        filters = {
            FilterOperators.EQ: {},
            FilterOperators.NE: {},
            FilterOperators.GT: {},
            FilterOperators.GE: {},
            FilterOperators.LT: {},
            FilterOperators.LE: {},
            FilterOperators.BETWEEN: {},
            FilterOperators.LIKE: {},
        }
        if req.id is not None and req.id != "":
            filters[FilterOperators.EQ]["id"] = req.id
        if req.stock_symbol_full is not None and req.stock_symbol_full != "":
            filters[FilterOperators.EQ]["stock_symbol_full"] = req.stock_symbol_full
        if req.report_date is not None and req.report_date != "":
            filters[FilterOperators.EQ]["report_date"] = req.report_date
        if req.report_type is not None and req.report_type != "":
            filters[FilterOperators.EQ]["report_type"] = req.report_type
        if req.total_revenue is not None and req.total_revenue != "":
            filters[FilterOperators.EQ]["total_revenue"] = req.total_revenue
        if req.net_profit is not None and req.net_profit != "":
            filters[FilterOperators.EQ]["net_profit"] = req.net_profit
        if req.total_assets is not None and req.total_assets != "":
            filters[FilterOperators.EQ]["total_assets"] = req.total_assets
        if req.total_liabilities is not None and req.total_liabilities != "":
            filters[FilterOperators.EQ]["total_liabilities"] = req.total_liabilities
        if req.net_assets is not None and req.net_assets != "":
            filters[FilterOperators.EQ]["net_assets"] = req.net_assets
        if req.eps is not None and req.eps != "":
            filters[FilterOperators.EQ]["eps"] = req.eps
        if req.roe is not None and req.roe != "":
            filters[FilterOperators.EQ]["roe"] = req.roe
        if req.gross_profit_margin is not None and req.gross_profit_margin != "":
            filters[FilterOperators.EQ]["gross_profit_margin"] = req.gross_profit_margin
        if req.report_source is not None and req.report_source != "":
            filters[FilterOperators.EQ]["report_source"] = req.report_source
        if req.earnings_announcement_date is not None and req.earnings_announcement_date != "":
            filters[FilterOperators.EQ]["earnings_announcement_date"] = req.earnings_announcement_date
        if req.published_date is not None and req.published_date != "":
            filters[FilterOperators.EQ]["published_date"] = req.published_date
        if req.created_at is not None and req.created_at != "":
            filters[FilterOperators.EQ]["created_at"] = req.created_at
        if req.updated_at is not None and req.updated_at != "":
            filters[FilterOperators.EQ]["updated_at"] = req.updated_at
        sort_list = None
        sort_str = req.sort_str
        if sort_str is not None:
            sort_list = json.loads(sort_str)
        return await self.mapper.select_by_ordered_page(
            current=req.current,
            page_size=req.page_size,
            count=req.count,
            **filters,
            sort_list=sort_list,
        )

    

    async def create_stock_financial_report(self, req: CreateStockFinancialReportRequest) -> StockFinancialReportModel:
        stock_financial_report: StockFinancialReportModel = StockFinancialReportModel(**req.stock_financial_report.model_dump())
        return await self.save(data=stock_financial_report)

    async def update_stock_financial_report(self, req: UpdateStockFinancialReportRequest) -> StockFinancialReportModel:
        stock_financial_report_record: StockFinancialReportModel = await self.retrieve_by_id(id=req.stock_financial_report.id)
        if stock_financial_report_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        stock_financial_report_model = StockFinancialReportModel(**req.stock_financial_report.model_dump(exclude_unset=True))
        await self.modify_by_id(data=stock_financial_report_model)
        merged_data = {**stock_financial_report_record.model_dump(), **stock_financial_report_model.model_dump()}
        return StockFinancialReportModel(**merged_data)

    async def delete_stock_financial_report(self, id: int) -> None:
        stock_financial_report_record: StockFinancialReportModel = await self.retrieve_by_id(id=id)
        if stock_financial_report_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_stock_financial_reports(self, ids: list[int]) -> list[StockFinancialReportModel]:
        stock_financial_report_records = list[StockFinancialReportModel] = await self.retrieve_by_ids(ids=ids)
        if stock_financial_report_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(stock_financial_report_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in stock_financial_report_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(stock_financial_report_records)} != {str(not_exits_ids)}",
            )
        return stock_financial_report_records

    async def batch_create_stock_financial_reports(
        self,
        *,
        req: BatchCreateStockFinancialReportsRequest,
    ) -> list[StockFinancialReportModel]:
        stock_financial_report_list: list[CreateStockFinancialReport] = req.stock_financial_reports
        if not stock_financial_report_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [StockFinancialReportModel(**stock_financial_report.model_dump()) for stock_financial_report in stock_financial_report_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_stock_financial_reports(
        self, req: BatchUpdateStockFinancialReportsRequest
    ) -> list[StockFinancialReportModel]:
        stock_financial_report: BatchUpdateStockFinancialReport = req.stock_financial_report
        ids: list[int] = req.ids
        if not stock_financial_report or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=stock_financial_report.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_stock_financial_reports(
        self, req: BatchPatchStockFinancialReportsRequest
    ) -> list[StockFinancialReportModel]:
        stock_financial_reports: list[UpdateStockFinancialReport] = req.stock_financial_reports
        if not stock_financial_reports:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            stock_financial_report.model_dump(exclude_unset=True) for stock_financial_report in stock_financial_reports
        ]
        await self.mapper.batch_update(items=update_data)
        stock_financial_report_ids: list[int] = [stock_financial_report.id for stock_financial_report in stock_financial_reports]
        return await self.mapper.select_by_ids(ids=stock_financial_report_ids)

    async def batch_delete_stock_financial_reports(self, req: BatchDeleteStockFinancialReportsRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_stock_financial_reports_template(self) -> StreamingResponse:
        file_name = "stock_financial_report_import_tpl"
        return await excel_util.export_excel(
            schema=CreateStockFinancialReport, file_name=file_name
        )

    async def export_stock_financial_reports(self, req: ExportStockFinancialReportsRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        stock_financial_report_list: list[StockFinancialReportModel] = await self.mapper.select_by_ids(ids=ids)
        if stock_financial_report_list is None or len(stock_financial_report_list) == 0:
            logger.error(f"No stock_financial_reports found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        stock_financial_report_page_list = [ExportStockFinancialReport(**stock_financial_report.model_dump()) for stock_financial_report in stock_financial_report_list]
        file_name = "stock_financial_report_data_export"
        return await excel_util.export_excel(
            schema=ExportStockFinancialReport, file_name=file_name, data_list=stock_financial_report_page_list
        )

    async def import_stock_financial_reports(self, req: ImportStockFinancialReportsRequest) -> list[ImportStockFinancialReport]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        stock_financial_report_records = import_df.to_dict(orient="records")
        if stock_financial_report_records is None or len(stock_financial_report_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in stock_financial_report_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        stock_financial_report_import_list = []
        for stock_financial_report_record in stock_financial_report_records:
            try:
                stock_financial_report_create = ImportStockFinancialReport(**stock_financial_report_record)
                stock_financial_report_import_list.append(stock_financial_report_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in stock_financial_report_record.items()
                    if k in ImportStockFinancialReport.model_fields
                }
                stock_financial_report_create = ImportStockFinancialReport.model_construct(**valid_data)
                stock_financial_report_create.err_msg = ValidateService.get_validate_err_msg(e)
                stock_financial_report_import_list.append(stock_financial_report_create)
                return stock_financial_report_import_list

        return stock_financial_report_import_list