# SPDX-License-Identifier: MIT
"""StockHolderInfo schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from fastlib.request import ListRequest


class ListStockHolderInfosRequest(ListRequest):
    id: Optional[int] = None
    stock_symbol_full: Optional[str] = None
    holder_name: Optional[str] = None
    holder_info: Optional[str] = None
    holder_type: Optional[int] = None
    share_amount: Optional[int] = None
    share_ratio: Optional[int] = None
    change_amount: Optional[int] = None
    change_type: Optional[int] = None
    report_date: Optional[datetime] = None
    is_top_ten: Optional[int] = None
    ranking: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StockHolderInfo(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    holder_name: Optional[str] = None
    holder_info: Optional[str] = None
    holder_type: Optional[int] = None
    share_amount: Optional[int] = None
    share_ratio: Optional[int] = None
    change_amount: Optional[int] = None
    change_type: Optional[int] = None
    report_date: Optional[datetime] = None
    is_top_ten: Optional[int] = '0'
    ranking: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StockHolderInfoDetail(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    holder_name: Optional[str] = None
    holder_info: Optional[str] = None
    holder_type: Optional[int] = None
    share_amount: Optional[int] = None
    share_ratio: Optional[int] = None
    change_amount: Optional[int] = None
    change_type: Optional[int] = None
    report_date: Optional[datetime] = None
    is_top_ten: Optional[int] = '0'
    ranking: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreateStockHolderInfo(BaseModel):
    stock_symbol_full: Optional[str] = None
    holder_name: Optional[str] = None
    holder_info: Optional[str] = None
    holder_type: Optional[int] = None
    share_amount: Optional[int] = None
    share_ratio: Optional[int] = None
    change_amount: Optional[int] = None
    change_type: Optional[int] = None
    report_date: Optional[datetime] = None
    is_top_ten: Optional[int] = '0'
    ranking: Optional[int] = None
    updated_at: Optional[datetime] = None


class CreateStockHolderInfoRequest(BaseModel):
    stock_holder_info: CreateStockHolderInfo = Field(alias="stockHolderInfo")


class UpdateStockHolderInfo(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    holder_name: Optional[str] = None
    holder_info: Optional[str] = None
    holder_type: Optional[int] = None
    share_amount: Optional[int] = None
    share_ratio: Optional[int] = None
    change_amount: Optional[int] = None
    change_type: Optional[int] = None
    report_date: Optional[datetime] = None
    is_top_ten: Optional[int] = '0'
    ranking: Optional[int] = None
    updated_at: Optional[datetime] = None


class UpdateStockHolderInfoRequest(BaseModel):
    stock_holder_info: UpdateStockHolderInfo = Field(alias="stockHolderInfo")


class BatchGetStockHolderInfosResponse(BaseModel):
    stock_holder_infos: list[StockHolderInfoDetail] = Field(default_factory=list, alias="stockHolderInfos")


class BatchCreateStockHolderInfosRequest(BaseModel):
    stock_holder_infos: list[CreateStockHolderInfo] = Field(default_factory=list, alias="stockHolderInfos")


class BatchCreateStockHolderInfosResponse(BaseModel):
    stock_holder_infos: list[StockHolderInfo] = Field(default_factory=list, alias="stockHolderInfos")


class BatchUpdateStockHolderInfo(BaseModel):
    stock_symbol_full: Optional[str] = None
    holder_name: Optional[str] = None
    holder_info: Optional[str] = None
    holder_type: Optional[int] = None
    share_amount: Optional[int] = None
    share_ratio: Optional[int] = None
    change_amount: Optional[int] = None
    change_type: Optional[int] = None
    report_date: Optional[datetime] = None
    is_top_ten: Optional[int] = '0'
    ranking: Optional[int] = None
    updated_at: Optional[datetime] = None


class BatchUpdateStockHolderInfosRequest(BaseModel):
    ids: list[int]
    stock_holder_info: BatchUpdateStockHolderInfo = Field(alias="stockHolderInfo")


class BatchPatchStockHolderInfosRequest(BaseModel):
    stock_holder_infos: list[UpdateStockHolderInfo] = Field(default_factory=list, alias="stockHolderInfos")


class BatchUpdateStockHolderInfosResponse(BaseModel):
     stock_holder_infos: list[StockHolderInfo] = Field(default_factory=list, alias="stockHolderInfos")


class BatchDeleteStockHolderInfosRequest(BaseModel):
    ids: list[int]


class ExportStockHolderInfo(StockHolderInfo):
    pass


class ExportStockHolderInfosRequest(BaseModel):
    ids: list[int]


class ImportStockHolderInfosRequest(BaseModel):
    file: UploadFile


class ImportStockHolderInfo(CreateStockHolderInfo):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportStockHolderInfosResponse(BaseModel):
    stock_holder_infos: list[ImportStockHolderInfo] = Field(default_factory=list, alias="stockHolderInfos")