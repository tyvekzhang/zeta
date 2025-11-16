# SPDX-License-Identifier: MIT
"""StockFinancialReport schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from fastlib.request import ListRequest


class ListStockFinancialReportsRequest(ListRequest):
    id: Optional[int] = None
    stock_symbol_full: Optional[str] = None
    report_date: Optional[datetime] = None
    report_type: Optional[int] = None
    total_revenue: Optional[int] = None
    net_profit: Optional[int] = None
    total_assets: Optional[int] = None
    total_liabilities: Optional[int] = None
    net_assets: Optional[int] = None
    eps: Optional[int] = None
    roe: Optional[int] = None
    gross_profit_margin: Optional[int] = None
    report_source: Optional[str] = None
    earnings_announcement_date: Optional[datetime] = None
    published_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StockFinancialReport(BaseModel):
    id: int
    file_id: Optional[int] = None
    stock_symbol_full: Optional[str] = None
    report_date: Optional[datetime] = None
    report_type: Optional[int] = None
    total_revenue: Optional[int] = None
    net_profit: Optional[int] = None
    total_assets: Optional[int] = None
    total_liabilities: Optional[int] = None
    net_assets: Optional[int] = None
    eps: Optional[int] = None
    roe: Optional[int] = None
    gross_profit_margin: Optional[int] = None
    report_source: Optional[str] = None
    earnings_announcement_date: Optional[datetime] = None
    published_date: Optional[datetime] = None
    comment: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StockFinancialReportDetail(BaseModel):
    id: int
    file_id: Optional[int] = None
    stock_symbol_full: Optional[str] = None
    report_date: Optional[datetime] = None
    report_type: Optional[int] = None
    total_revenue: Optional[int] = None
    net_profit: Optional[int] = None
    total_assets: Optional[int] = None
    total_liabilities: Optional[int] = None
    net_assets: Optional[int] = None
    eps: Optional[int] = None
    roe: Optional[int] = None
    gross_profit_margin: Optional[int] = None
    report_source: Optional[str] = None
    earnings_announcement_date: Optional[datetime] = None
    published_date: Optional[datetime] = None
    comment: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreateStockFinancialReport(BaseModel):
    file_id: Optional[int] = None
    stock_symbol_full: Optional[str] = None
    report_date: Optional[datetime] = None
    report_type: Optional[int] = None
    total_revenue: Optional[int] = None
    net_profit: Optional[int] = None
    total_assets: Optional[int] = None
    total_liabilities: Optional[int] = None
    net_assets: Optional[int] = None
    eps: Optional[int] = None
    roe: Optional[int] = None
    gross_profit_margin: Optional[int] = None
    report_source: Optional[str] = None
    earnings_announcement_date: Optional[datetime] = None
    published_date: Optional[datetime] = None
    comment: Optional[str] = None
    updated_at: Optional[datetime] = None


class CreateStockFinancialReportRequest(BaseModel):
    stock_financial_report: CreateStockFinancialReport = Field(alias="stockFinancialReport")


class UpdateStockFinancialReport(BaseModel):
    id: int
    file_id: Optional[int] = None
    stock_symbol_full: Optional[str] = None
    report_date: Optional[datetime] = None
    report_type: Optional[int] = None
    total_revenue: Optional[int] = None
    net_profit: Optional[int] = None
    total_assets: Optional[int] = None
    total_liabilities: Optional[int] = None
    net_assets: Optional[int] = None
    eps: Optional[int] = None
    roe: Optional[int] = None
    gross_profit_margin: Optional[int] = None
    report_source: Optional[str] = None
    earnings_announcement_date: Optional[datetime] = None
    published_date: Optional[datetime] = None
    comment: Optional[str] = None
    updated_at: Optional[datetime] = None


class UpdateStockFinancialReportRequest(BaseModel):
    stock_financial_report: UpdateStockFinancialReport = Field(alias="stockFinancialReport")


class BatchGetStockFinancialReportsResponse(BaseModel):
    stock_financial_reports: list[StockFinancialReportDetail] = Field(default_factory=list, alias="stockFinancialReports")


class BatchCreateStockFinancialReportsRequest(BaseModel):
    stock_financial_reports: list[CreateStockFinancialReport] = Field(default_factory=list, alias="stockFinancialReports")


class BatchCreateStockFinancialReportsResponse(BaseModel):
    stock_financial_reports: list[StockFinancialReport] = Field(default_factory=list, alias="stockFinancialReports")


class BatchUpdateStockFinancialReport(BaseModel):
    file_id: Optional[int] = None
    stock_symbol_full: Optional[str] = None
    report_date: Optional[datetime] = None
    report_type: Optional[int] = None
    total_revenue: Optional[int] = None
    net_profit: Optional[int] = None
    total_assets: Optional[int] = None
    total_liabilities: Optional[int] = None
    net_assets: Optional[int] = None
    eps: Optional[int] = None
    roe: Optional[int] = None
    gross_profit_margin: Optional[int] = None
    report_source: Optional[str] = None
    earnings_announcement_date: Optional[datetime] = None
    published_date: Optional[datetime] = None
    comment: Optional[str] = None
    updated_at: Optional[datetime] = None


class BatchUpdateStockFinancialReportsRequest(BaseModel):
    ids: list[int]
    stock_financial_report: BatchUpdateStockFinancialReport = Field(alias="stockFinancialReport")


class BatchPatchStockFinancialReportsRequest(BaseModel):
    stock_financial_reports: list[UpdateStockFinancialReport] = Field(default_factory=list, alias="stockFinancialReports")


class BatchUpdateStockFinancialReportsResponse(BaseModel):
     stock_financial_reports: list[StockFinancialReport] = Field(default_factory=list, alias="stockFinancialReports")


class BatchDeleteStockFinancialReportsRequest(BaseModel):
    ids: list[int]


class ExportStockFinancialReport(StockFinancialReport):
    pass


class ExportStockFinancialReportsRequest(BaseModel):
    ids: list[int]


class ImportStockFinancialReportsRequest(BaseModel):
    file: UploadFile


class ImportStockFinancialReport(CreateStockFinancialReport):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportStockFinancialReportsResponse(BaseModel):
    stock_financial_reports: list[ImportStockFinancialReport] = Field(default_factory=list, alias="stockFinancialReports")