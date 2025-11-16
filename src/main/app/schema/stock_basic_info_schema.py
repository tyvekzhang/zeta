# SPDX-License-Identifier: MIT
"""StockBasicInfo schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from fastlib.request import ListRequest


class ListStockBasicInfosRequest(ListRequest):
    id: Optional[int] = None
    symbol: Optional[str] = None
    symbol_full: Optional[str] = None
    name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    industry_gy: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    price_tick: Optional[int] = None
    data_source: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StockBasicInfo(BaseModel):
    id: int
    symbol: Optional[str] = None
    symbol_full: Optional[str] = None
    name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    industry_gy: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    price_tick: Optional[int] = '1'
    data_source: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StockBasicInfoDetail(BaseModel):
    id: int
    symbol: Optional[str] = None
    symbol_full: Optional[str] = None
    name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    industry_gy: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    price_tick: Optional[int] = '1'
    data_source: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreateStockBasicInfo(BaseModel):
    symbol: Optional[str] = None
    symbol_full: Optional[str] = None
    name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    industry_gy: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    price_tick: Optional[int] = '1'
    data_source: Optional[str] = None
    updated_at: Optional[datetime] = None


class CreateStockBasicInfoRequest(BaseModel):
    stock_basic_info: CreateStockBasicInfo = Field(alias="stockBasicInfo")


class UpdateStockBasicInfo(BaseModel):
    id: int
    symbol: Optional[str] = None
    symbol_full: Optional[str] = None
    name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    industry_gy: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    price_tick: Optional[int] = '1'
    data_source: Optional[str] = None
    updated_at: Optional[datetime] = None


class UpdateStockBasicInfoRequest(BaseModel):
    stock_basic_info: UpdateStockBasicInfo = Field(alias="stockBasicInfo")


class BatchGetStockBasicInfosResponse(BaseModel):
    stock_basic_infos: list[StockBasicInfoDetail] = Field(default_factory=list, alias="stockBasicInfos")


class BatchCreateStockBasicInfosRequest(BaseModel):
    stock_basic_infos: list[CreateStockBasicInfo] = Field(default_factory=list, alias="stockBasicInfos")


class BatchCreateStockBasicInfosResponse(BaseModel):
    stock_basic_infos: list[StockBasicInfo] = Field(default_factory=list, alias="stockBasicInfos")


class BatchUpdateStockBasicInfo(BaseModel):
    symbol: Optional[str] = None
    symbol_full: Optional[str] = None
    name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    industry_gy: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    price_tick: Optional[int] = '1'
    data_source: Optional[str] = None
    updated_at: Optional[datetime] = None


class BatchUpdateStockBasicInfosRequest(BaseModel):
    ids: list[int]
    stock_basic_info: BatchUpdateStockBasicInfo = Field(alias="stockBasicInfo")


class BatchPatchStockBasicInfosRequest(BaseModel):
    stock_basic_infos: list[UpdateStockBasicInfo] = Field(default_factory=list, alias="stockBasicInfos")


class BatchUpdateStockBasicInfosResponse(BaseModel):
     stock_basic_infos: list[StockBasicInfo] = Field(default_factory=list, alias="stockBasicInfos")


class BatchDeleteStockBasicInfosRequest(BaseModel):
    ids: list[int]


class ExportStockBasicInfo(StockBasicInfo):
    pass


class ExportStockBasicInfosRequest(BaseModel):
    ids: list[int]


class ImportStockBasicInfosRequest(BaseModel):
    file: UploadFile


class ImportStockBasicInfo(CreateStockBasicInfo):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportStockBasicInfosResponse(BaseModel):
    stock_basic_infos: list[ImportStockBasicInfo] = Field(default_factory=list, alias="stockBasicInfos")