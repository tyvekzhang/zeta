# SPDX-License-Identifier: MIT
"""ReportIncomeStatement schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from fastlib.request import ListRequest


class ListReportIncomeStatementsRequest(ListRequest):
    id: Optional[int] = None
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    net_profit: Optional[str] = None
    net_profit_yoy: Optional[str] = None
    total_operating_income: Optional[str] = None
    total_operating_income_yoy: Optional[str] = None
    operating_expenses: Optional[str] = None
    sales_expenses: Optional[str] = None
    management_expenses: Optional[str] = None
    financial_expenses: Optional[str] = None
    total_operating_expenses: Optional[str] = None
    operating_profit: Optional[str] = None
    total_profit: Optional[str] = None
    announcement_date: Optional[datetime] = None
    year: Optional[int] = None
    quarter: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ReportIncomeStatement(BaseModel):
    id: int
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    net_profit: Optional[str] = None
    net_profit_yoy: Optional[str] = None
    total_operating_income: Optional[str] = None
    total_operating_income_yoy: Optional[str] = None
    operating_expenses: Optional[str] = None
    sales_expenses: Optional[str] = None
    management_expenses: Optional[str] = None
    financial_expenses: Optional[str] = None
    total_operating_expenses: Optional[str] = None
    operating_profit: Optional[str] = None
    total_profit: Optional[str] = None
    announcement_date: Optional[datetime] = None
    year: Optional[int] = None
    quarter: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ReportIncomeStatementDetail(BaseModel):
    id: int
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    net_profit: Optional[str] = None
    net_profit_yoy: Optional[str] = None
    total_operating_income: Optional[str] = None
    total_operating_income_yoy: Optional[str] = None
    operating_expenses: Optional[str] = None
    sales_expenses: Optional[str] = None
    management_expenses: Optional[str] = None
    financial_expenses: Optional[str] = None
    total_operating_expenses: Optional[str] = None
    operating_profit: Optional[str] = None
    total_profit: Optional[str] = None
    announcement_date: Optional[datetime] = None
    year: Optional[int] = None
    quarter: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreateReportIncomeStatement(BaseModel):
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    net_profit: Optional[str] = None
    net_profit_yoy: Optional[str] = None
    total_operating_income: Optional[str] = None
    total_operating_income_yoy: Optional[str] = None
    operating_expenses: Optional[str] = None
    sales_expenses: Optional[str] = None
    management_expenses: Optional[str] = None
    financial_expenses: Optional[str] = None
    total_operating_expenses: Optional[str] = None
    operating_profit: Optional[str] = None
    total_profit: Optional[str] = None
    announcement_date: Optional[datetime] = None
    year: Optional[int] = None
    quarter: Optional[int] = None
    updated_at: Optional[datetime] = None


class CreateReportIncomeStatementRequest(BaseModel):
    report_income_statement: CreateReportIncomeStatement = Field(alias="reportIncomeStatement")


class UpdateReportIncomeStatement(BaseModel):
    id: int
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    net_profit: Optional[str] = None
    net_profit_yoy: Optional[str] = None
    total_operating_income: Optional[str] = None
    total_operating_income_yoy: Optional[str] = None
    operating_expenses: Optional[str] = None
    sales_expenses: Optional[str] = None
    management_expenses: Optional[str] = None
    financial_expenses: Optional[str] = None
    total_operating_expenses: Optional[str] = None
    operating_profit: Optional[str] = None
    total_profit: Optional[str] = None
    announcement_date: Optional[datetime] = None
    year: Optional[int] = None
    quarter: Optional[int] = None
    updated_at: Optional[datetime] = None


class UpdateReportIncomeStatementRequest(BaseModel):
    report_income_statement: UpdateReportIncomeStatement = Field(alias="reportIncomeStatement")


class BatchGetReportIncomeStatementsResponse(BaseModel):
    report_income_statements: list[ReportIncomeStatementDetail] = Field(default_factory=list, alias="reportIncomeStatements")


class BatchCreateReportIncomeStatementsRequest(BaseModel):
    report_income_statements: list[CreateReportIncomeStatement] = Field(default_factory=list, alias="reportIncomeStatements")


class BatchCreateReportIncomeStatementsResponse(BaseModel):
    report_income_statements: list[ReportIncomeStatement] = Field(default_factory=list, alias="reportIncomeStatements")


class BatchUpdateReportIncomeStatement(BaseModel):
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    net_profit: Optional[str] = None
    net_profit_yoy: Optional[str] = None
    total_operating_income: Optional[str] = None
    total_operating_income_yoy: Optional[str] = None
    operating_expenses: Optional[str] = None
    sales_expenses: Optional[str] = None
    management_expenses: Optional[str] = None
    financial_expenses: Optional[str] = None
    total_operating_expenses: Optional[str] = None
    operating_profit: Optional[str] = None
    total_profit: Optional[str] = None
    announcement_date: Optional[datetime] = None
    year: Optional[int] = None
    quarter: Optional[int] = None
    updated_at: Optional[datetime] = None


class BatchUpdateReportIncomeStatementsRequest(BaseModel):
    ids: list[int]
    report_income_statement: BatchUpdateReportIncomeStatement = Field(alias="reportIncomeStatement")


class BatchPatchReportIncomeStatementsRequest(BaseModel):
    report_income_statements: list[UpdateReportIncomeStatement] = Field(default_factory=list, alias="reportIncomeStatements")


class BatchUpdateReportIncomeStatementsResponse(BaseModel):
     report_income_statements: list[ReportIncomeStatement] = Field(default_factory=list, alias="reportIncomeStatements")


class BatchDeleteReportIncomeStatementsRequest(BaseModel):
    ids: list[int]


class ExportReportIncomeStatement(ReportIncomeStatement):
    pass


class ExportReportIncomeStatementsRequest(BaseModel):
    ids: list[int]


class ImportReportIncomeStatementsRequest(BaseModel):
    file: UploadFile


class ImportReportIncomeStatement(CreateReportIncomeStatement):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportReportIncomeStatementsResponse(BaseModel):
    report_income_statements: list[ImportReportIncomeStatement] = Field(default_factory=list, alias="reportIncomeStatements")