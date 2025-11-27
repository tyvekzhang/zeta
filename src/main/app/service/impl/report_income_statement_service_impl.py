# SPDX-License-Identifier: MIT
"""ReportIncomeStatement domain service impl"""

from __future__ import annotations

import io
import json
from typing import Any
import akshare as ak

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
from src.main.app.mapper.report_income_statement_mapper import (
    ReportIncomeStatementMapper,
)
from src.main.app.model.report_income_statement_model import ReportIncomeStatementModel
from src.main.app.schema.report_income_statement_schema import (
    ListReportIncomeStatementsRequest,
    CreateReportIncomeStatementRequest,
    UpdateReportIncomeStatementRequest,
    BatchDeleteReportIncomeStatementsRequest,
    ExportReportIncomeStatementsRequest,
    BatchCreateReportIncomeStatementsRequest,
    CreateReportIncomeStatement,
    BatchUpdateReportIncomeStatementsRequest,
    UpdateReportIncomeStatement,
    ImportReportIncomeStatementsRequest,
    ImportReportIncomeStatement,
    ExportReportIncomeStatement,
    BatchPatchReportIncomeStatementsRequest,
    BatchUpdateReportIncomeStatement,
)
from src.main.app.service.report_income_statement_service import (
    ReportIncomeStatementService,
)


class ReportIncomeStatementServiceImpl(
    BaseServiceImpl[ReportIncomeStatementMapper, ReportIncomeStatementModel],
    ReportIncomeStatementService,
):
    """
    Implementation of the ReportIncomeStatementService interface.
    """

    def __init__(self, mapper: ReportIncomeStatementMapper):
        """
        Initialize the ReportIncomeStatementServiceImpl instance.

        Args:
            mapper (ReportIncomeStatementMapper): The ReportIncomeStatementMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper, model=ReportIncomeStatementModel)
        self.mapper = mapper
        
    async def calculate_key_financial_ratios(
            self, report_list: list[ReportIncomeStatementModel]
        ) -> list[ReportIncomeStatementModel]:
            """
            Calculates key financial ratios (Gross Margin, Expense Ratio, Operating Profit Margin)
            for a list of income statement records and updates the models.
            
            Note: This assumes ReportIncomeStatementModel has been updated to include
            'gross_margin', 'expense_ratio', and 'operating_profit_margin' fields.

            Args:
                report_list (list[ReportIncomeStatementModel]): List of income statement models.

            Returns:
                list[ReportIncomeStatementModel]: List of models updated with calculated ratios.
            """
            calculated_list: list[ReportIncomeStatementModel] = []
            for report in report_list:
                # 转换为字典以便添加新的计算字段
                report_dict = report.model_dump()
                
                # 提取所需数据，并确保它们是浮点数，默认为 0
                # 使用 getattr 安全地访问字段
                total_operating_income = float(getattr(report, 'total_operating_income', 0) or 0)
                # 假设 'operating_expenses' 为营业成本
                operating_expenses = float(getattr(report, 'operating_expenses', 0) or 0)
                sales_expenses = float(getattr(report, 'sales_expenses', 0) or 0)
                management_expenses = float(getattr(report, 'management_expenses', 0) or 0)
                financial_expenses = float(getattr(report, 'financial_expenses', 0) or 0)
                operating_profit = float(getattr(report, 'operating_profit', 0) or 0)

                # 默认设置为 None 或 0.0
                gross_margin = None
                expense_ratio = None
                operating_profit_margin = None

                if total_operating_income != 0:
                    # 1. 毛利率 (Gross Margin)
                    # Gross Margin = (Operating Revenue - Operating Cost) / Operating Revenue
                    gross_profit = total_operating_income - operating_expenses
                    gross_margin = round((gross_profit / total_operating_income) * 100, 2)
                    
                    # 2. 费用率 (Expense Ratio) - 期间费用率
                    # Expense Ratio = (Sales Expenses + Management Expenses + Financial Expenses) / Operating Revenue
                    total_period_expenses = sales_expenses + management_expenses + financial_expenses
                    expense_ratio = round((total_period_expenses / total_operating_income) * 100, 2)
                    
                    # 3. 营业利润率 (Operating Profit Margin)
                    # Operating Profit Margin = Operating Profit / Operating Revenue
                    operating_profit_margin = round((operating_profit / total_operating_income) * 100, 2)

                # 更新模型的临时字典，以便重新构造模型或返回
                report_dict["gross_margin"] = gross_margin
                report_dict["expense_ratio"] = expense_ratio
                report_dict["operating_profit_margin"] = operating_profit_margin
                
                # 尝试使用更新后的字典构造新的模型实例
                try:
                    # 假设 ReportIncomeStatementModel 现在包含这些字段
                    calculated_list.append(ReportIncomeStatementModel(**report_dict))
                except Exception as e:
                    # 如果模型未更新，可能需要返回字典或处理错误
                    logger.warning(f"Failed to instantiate model with ratios: {e}")
                    # 作为一个回退方案，如果模型无法构造，我们直接返回原始模型
                    calculated_list.append(report)

            return calculated_list

    async def sync_manually(self, year: int, quarter: int) -> None:
        filters = {
            FilterOperators.EQ: {},
        }
        filters[FilterOperators.EQ]["year"] = year
        filters[FilterOperators.EQ]["quarter"] = quarter
        exist_data, _ = await self.mapper.select_by_page(count=False, **filters)
        if exist_data:
            exist_ids = [item.id for item in exist_data]
            await self.mapper.batch_delete_by_ids(ids=exist_ids)
        quarter_str = "1231"
        match(quarter):
            case 1:
               quarter_str = "0331" 
            case 1:
               quarter_str = "0630" 
            case 1:
               quarter_str = "0930"
        date_str = str(year) + quarter_str
        quarter_data = ak.stock_lrb_em(date=date_str)
        if quarter_data.empty:
            return

        quarter_data["year"] = year
        quarter_data["quarter"] = quarter
        column_mapping = {
            "股票代码": "stock_code",
            "股票简称": "stock_name",
            "净利润": "net_profit",
            "净利润同比": "net_profit_yoy",
            "营业总收入": "total_operating_income",
            "营业总收入同比": "total_operating_income_yoy",
            "营业总支出-营业支出": "operating_expenses",
            "营业总支出-销售费用": "sales_expenses",
            "营业总支出-管理费用": "management_expenses",
            "营业总支出-财务费用": "financial_expenses",
            "营业总支出-营业总支出": "total_operating_expenses",
            "营业利润": "operating_profit",
            "利润总额": "total_profit",
            "公告日期": "announcement_date",
        }
        quarter_data.rename(columns=column_mapping, inplace=True)
        quarter_data = quarter_data.fillna(0)
        data_list = quarter_data.to_dict(orient='records')
        need_save_data = [ReportIncomeStatementModel(**item) for item in data_list]
        await self.mapper.batch_insert(data_list=need_save_data)

    async def get_report_income_statement(
        self,
        *,
        id: int,
    ) -> ReportIncomeStatementModel:
        report_income_statement_record: ReportIncomeStatementModel = (
            await self.mapper.select_by_id(id=id)
        )
        if report_income_statement_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return report_income_statement_record

    async def list_report_income_statements(
        self, req: ListReportIncomeStatementsRequest
    ) -> tuple[list[ReportIncomeStatementModel], int]:
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
        if req.stock_code is not None and req.stock_code != "":
            filters[FilterOperators.EQ]["stock_code"] = req.stock_code
        if req.stock_name is not None and req.stock_name != "":
            filters[FilterOperators.LIKE]["stock_name"] = req.stock_name
        if req.exchange is not None and req.exchange != "":
            filters[FilterOperators.EQ]["exchange"] = req.exchange
        if req.net_profit is not None and req.net_profit != "":
            filters[FilterOperators.EQ]["net_profit"] = req.net_profit
        if req.net_profit_yoy is not None and req.net_profit_yoy != "":
            filters[FilterOperators.EQ]["net_profit_yoy"] = req.net_profit_yoy
        if req.total_operating_income is not None and req.total_operating_income != "":
            filters[FilterOperators.EQ][
                "total_operating_income"
            ] = req.total_operating_income
        if (
            req.total_operating_income_yoy is not None
            and req.total_operating_income_yoy != ""
        ):
            filters[FilterOperators.EQ][
                "total_operating_income_yoy"
            ] = req.total_operating_income_yoy
        if req.operating_expenses is not None and req.operating_expenses != "":
            filters[FilterOperators.EQ]["operating_expenses"] = req.operating_expenses
        if req.sales_expenses is not None and req.sales_expenses != "":
            filters[FilterOperators.EQ]["sales_expenses"] = req.sales_expenses
        if req.management_expenses is not None and req.management_expenses != "":
            filters[FilterOperators.EQ]["management_expenses"] = req.management_expenses
        if req.financial_expenses is not None and req.financial_expenses != "":
            filters[FilterOperators.EQ]["financial_expenses"] = req.financial_expenses
        if (
            req.total_operating_expenses is not None
            and req.total_operating_expenses != ""
        ):
            filters[FilterOperators.EQ][
                "total_operating_expenses"
            ] = req.total_operating_expenses
        if req.operating_profit is not None and req.operating_profit != "":
            filters[FilterOperators.EQ]["operating_profit"] = req.operating_profit
        if req.total_profit is not None and req.total_profit != "":
            filters[FilterOperators.EQ]["total_profit"] = req.total_profit
        if req.announcement_date is not None and req.announcement_date != "":
            filters[FilterOperators.EQ]["announcement_date"] = req.announcement_date
        if req.year is not None and req.year != "":
            filters[FilterOperators.EQ]["year"] = req.year
        if req.quarter is not None and req.quarter != "":
            filters[FilterOperators.EQ]["quarter"] = req.quarter
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

    async def create_report_income_statement(
        self, req: CreateReportIncomeStatementRequest
    ) -> ReportIncomeStatementModel:
        report_income_statement: ReportIncomeStatementModel = (
            ReportIncomeStatementModel(**req.report_income_statement.model_dump())
        )
        return await self.save(data=report_income_statement)

    async def update_report_income_statement(
        self, req: UpdateReportIncomeStatementRequest
    ) -> ReportIncomeStatementModel:
        report_income_statement_record: ReportIncomeStatementModel = (
            await self.retrieve_by_id(id=req.report_income_statement.id)
        )
        if report_income_statement_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        report_income_statement_model = ReportIncomeStatementModel(
            **req.report_income_statement.model_dump(exclude_unset=True)
        )
        await self.modify_by_id(data=report_income_statement_model)
        merged_data = {
            **report_income_statement_record.model_dump(),
            **report_income_statement_model.model_dump(),
        }
        return ReportIncomeStatementModel(**merged_data)

    async def delete_report_income_statement(self, id: int) -> None:
        report_income_statement_record: ReportIncomeStatementModel = (
            await self.retrieve_by_id(id=id)
        )
        if report_income_statement_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_report_income_statements(
        self, ids: list[int]
    ) -> list[ReportIncomeStatementModel]:
        report_income_statement_records = list[ReportIncomeStatementModel] = (
            await self.retrieve_by_ids(ids=ids)
        )
        if report_income_statement_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(report_income_statement_records) != len(ids):
            not_exits_ids = [
                id for id in ids if id not in report_income_statement_records
            ]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(report_income_statement_records)} != {str(not_exits_ids)}",
            )
        return report_income_statement_records

    async def batch_create_report_income_statements(
        self,
        *,
        req: BatchCreateReportIncomeStatementsRequest,
    ) -> list[ReportIncomeStatementModel]:
        report_income_statement_list: list[CreateReportIncomeStatement] = (
            req.report_income_statements
        )
        if not report_income_statement_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [
            ReportIncomeStatementModel(**report_income_statement.model_dump())
            for report_income_statement in report_income_statement_list
        ]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_report_income_statements(
        self, req: BatchUpdateReportIncomeStatementsRequest
    ) -> list[ReportIncomeStatementModel]:
        report_income_statement: BatchUpdateReportIncomeStatement = (
            req.report_income_statement
        )
        ids: list[int] = req.ids
        if not report_income_statement or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=report_income_statement.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_report_income_statements(
        self, req: BatchPatchReportIncomeStatementsRequest
    ) -> list[ReportIncomeStatementModel]:
        report_income_statements: list[UpdateReportIncomeStatement] = (
            req.report_income_statements
        )
        if not report_income_statements:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            report_income_statement.model_dump(exclude_unset=True)
            for report_income_statement in report_income_statements
        ]
        await self.mapper.batch_update(items=update_data)
        report_income_statement_ids: list[int] = [
            report_income_statement.id
            for report_income_statement in report_income_statements
        ]
        return await self.mapper.select_by_ids(ids=report_income_statement_ids)

    async def batch_delete_report_income_statements(
        self, req: BatchDeleteReportIncomeStatementsRequest
    ):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_report_income_statements_template(self) -> StreamingResponse:
        file_name = "report_income_statement_import_tpl"
        return await excel_util.export_excel(
            schema=CreateReportIncomeStatement, file_name=file_name
        )

    async def export_report_income_statements(
        self, req: ExportReportIncomeStatementsRequest
    ) -> StreamingResponse:
        ids: list[int] = req.ids
        report_income_statement_list: list[ReportIncomeStatementModel] = (
            await self.mapper.select_by_ids(ids=ids)
        )
        if (
            report_income_statement_list is None
            or len(report_income_statement_list) == 0
        ):
            logger.error(f"No report_income_statements found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        report_income_statement_page_list = [
            ExportReportIncomeStatement(**report_income_statement.model_dump())
            for report_income_statement in report_income_statement_list
        ]
        file_name = "report_income_statement_data_export"
        return await excel_util.export_excel(
            schema=ExportReportIncomeStatement,
            file_name=file_name,
            data_list=report_income_statement_page_list,
        )

    async def import_report_income_statements(
        self, req: ImportReportIncomeStatementsRequest
    ) -> list[ImportReportIncomeStatement]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        report_income_statement_records = import_df.to_dict(orient="records")
        if (
            report_income_statement_records is None
            or len(report_income_statement_records) == 0
        ):
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in report_income_statement_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        report_income_statement_import_list = []
        for report_income_statement_record in report_income_statement_records:
            try:
                report_income_statement_create = ImportReportIncomeStatement(
                    **report_income_statement_record
                )
                report_income_statement_import_list.append(
                    report_income_statement_create
                )
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in report_income_statement_record.items()
                    if k in ImportReportIncomeStatement.model_fields
                }
                report_income_statement_create = (
                    ImportReportIncomeStatement.model_construct(**valid_data)
                )
                report_income_statement_create.err_msg = (
                    ValidateService.get_validate_err_msg(e)
                )
                report_income_statement_import_list.append(
                    report_income_statement_create
                )
                return report_income_statement_import_list

        return report_income_statement_import_list
