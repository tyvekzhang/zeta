# SPDX-License-Identifier: MIT
"""StockDailyInfo schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from fastlib.request import ListRequest


class ListStockDailyInfosRequest(ListRequest):
    id: Optional[int] = None
    stock_symbol_full: Optional[str] = None
    trade_date: Optional[datetime] = None
    open_price: Optional[int] = None
    close_price: Optional[int] = None
    high_price: Optional[int] = None
    low_price: Optional[int] = None
    volume: Optional[int] = None
    turnover: Optional[int] = None
    change_amount: Optional[int] = None
    change_rate: Optional[int] = None
    pe_ratio: Optional[int] = None
    pb_ratio: Optional[int] = None
    market_cap: Optional[int] = None
    circulating_market_cap: Optional[int] = None
    turnover_rate: Optional[int] = None
    bid_price1: Optional[int] = None
    bid_price2: Optional[int] = None
    bid_price3: Optional[int] = None
    bid_price4: Optional[int] = None
    bid_price5: Optional[int] = None
    bid_volume1: Optional[int] = None
    bid_volume2: Optional[int] = None
    bid_volume3: Optional[int] = None
    bid_volume4: Optional[int] = None
    bid_volume5: Optional[int] = None
    ask_price1: Optional[int] = None
    ask_price2: Optional[int] = None
    ask_price3: Optional[int] = None
    ask_price4: Optional[int] = None
    ask_price5: Optional[int] = None
    ask_volume1: Optional[int] = None
    ask_volume2: Optional[int] = None
    ask_volume3: Optional[int] = None
    ask_volume4: Optional[int] = None
    ask_volume5: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StockDailyInfo(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    trade_date: Optional[datetime] = None
    open_price: Optional[int] = None
    close_price: Optional[int] = None
    high_price: Optional[int] = None
    low_price: Optional[int] = None
    volume: Optional[int] = None
    turnover: Optional[int] = None
    change_amount: Optional[int] = None
    change_rate: Optional[int] = None
    pe_ratio: Optional[int] = None
    pb_ratio: Optional[int] = None
    market_cap: Optional[int] = None
    circulating_market_cap: Optional[int] = None
    turnover_rate: Optional[int] = None
    bid_price1: Optional[int] = None
    bid_price2: Optional[int] = None
    bid_price3: Optional[int] = None
    bid_price4: Optional[int] = None
    bid_price5: Optional[int] = None
    bid_volume1: Optional[int] = None
    bid_volume2: Optional[int] = None
    bid_volume3: Optional[int] = None
    bid_volume4: Optional[int] = None
    bid_volume5: Optional[int] = None
    ask_price1: Optional[int] = None
    ask_price2: Optional[int] = None
    ask_price3: Optional[int] = None
    ask_price4: Optional[int] = None
    ask_price5: Optional[int] = None
    ask_volume1: Optional[int] = None
    ask_volume2: Optional[int] = None
    ask_volume3: Optional[int] = None
    ask_volume4: Optional[int] = None
    ask_volume5: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StockDailyInfoDetail(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    trade_date: Optional[datetime] = None
    open_price: Optional[int] = None
    close_price: Optional[int] = None
    high_price: Optional[int] = None
    low_price: Optional[int] = None
    volume: Optional[int] = None
    turnover: Optional[int] = None
    change_amount: Optional[int] = None
    change_rate: Optional[int] = None
    pe_ratio: Optional[int] = None
    pb_ratio: Optional[int] = None
    market_cap: Optional[int] = None
    circulating_market_cap: Optional[int] = None
    turnover_rate: Optional[int] = None
    bid_price1: Optional[int] = None
    bid_price2: Optional[int] = None
    bid_price3: Optional[int] = None
    bid_price4: Optional[int] = None
    bid_price5: Optional[int] = None
    bid_volume1: Optional[int] = None
    bid_volume2: Optional[int] = None
    bid_volume3: Optional[int] = None
    bid_volume4: Optional[int] = None
    bid_volume5: Optional[int] = None
    ask_price1: Optional[int] = None
    ask_price2: Optional[int] = None
    ask_price3: Optional[int] = None
    ask_price4: Optional[int] = None
    ask_price5: Optional[int] = None
    ask_volume1: Optional[int] = None
    ask_volume2: Optional[int] = None
    ask_volume3: Optional[int] = None
    ask_volume4: Optional[int] = None
    ask_volume5: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreateStockDailyInfo(BaseModel):
    stock_symbol_full: Optional[str] = None
    trade_date: Optional[datetime] = None
    open_price: Optional[int] = None
    close_price: Optional[int] = None
    high_price: Optional[int] = None
    low_price: Optional[int] = None
    volume: Optional[int] = None
    turnover: Optional[int] = None
    change_amount: Optional[int] = None
    change_rate: Optional[int] = None
    pe_ratio: Optional[int] = None
    pb_ratio: Optional[int] = None
    market_cap: Optional[int] = None
    circulating_market_cap: Optional[int] = None
    turnover_rate: Optional[int] = None
    bid_price1: Optional[int] = None
    bid_price2: Optional[int] = None
    bid_price3: Optional[int] = None
    bid_price4: Optional[int] = None
    bid_price5: Optional[int] = None
    bid_volume1: Optional[int] = None
    bid_volume2: Optional[int] = None
    bid_volume3: Optional[int] = None
    bid_volume4: Optional[int] = None
    bid_volume5: Optional[int] = None
    ask_price1: Optional[int] = None
    ask_price2: Optional[int] = None
    ask_price3: Optional[int] = None
    ask_price4: Optional[int] = None
    ask_price5: Optional[int] = None
    ask_volume1: Optional[int] = None
    ask_volume2: Optional[int] = None
    ask_volume3: Optional[int] = None
    ask_volume4: Optional[int] = None
    ask_volume5: Optional[int] = None
    updated_at: Optional[datetime] = None


class CreateStockDailyInfoRequest(BaseModel):
    stock_daily_info: CreateStockDailyInfo = Field(alias="stockDailyInfo")


class UpdateStockDailyInfo(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    trade_date: Optional[datetime] = None
    open_price: Optional[int] = None
    close_price: Optional[int] = None
    high_price: Optional[int] = None
    low_price: Optional[int] = None
    volume: Optional[int] = None
    turnover: Optional[int] = None
    change_amount: Optional[int] = None
    change_rate: Optional[int] = None
    pe_ratio: Optional[int] = None
    pb_ratio: Optional[int] = None
    market_cap: Optional[int] = None
    circulating_market_cap: Optional[int] = None
    turnover_rate: Optional[int] = None
    bid_price1: Optional[int] = None
    bid_price2: Optional[int] = None
    bid_price3: Optional[int] = None
    bid_price4: Optional[int] = None
    bid_price5: Optional[int] = None
    bid_volume1: Optional[int] = None
    bid_volume2: Optional[int] = None
    bid_volume3: Optional[int] = None
    bid_volume4: Optional[int] = None
    bid_volume5: Optional[int] = None
    ask_price1: Optional[int] = None
    ask_price2: Optional[int] = None
    ask_price3: Optional[int] = None
    ask_price4: Optional[int] = None
    ask_price5: Optional[int] = None
    ask_volume1: Optional[int] = None
    ask_volume2: Optional[int] = None
    ask_volume3: Optional[int] = None
    ask_volume4: Optional[int] = None
    ask_volume5: Optional[int] = None
    updated_at: Optional[datetime] = None


class UpdateStockDailyInfoRequest(BaseModel):
    stock_daily_info: UpdateStockDailyInfo = Field(alias="stockDailyInfo")


class BatchGetStockDailyInfosResponse(BaseModel):
    stock_daily_infos: list[StockDailyInfoDetail] = Field(default_factory=list, alias="stockDailyInfos")


class BatchCreateStockDailyInfosRequest(BaseModel):
    stock_daily_infos: list[CreateStockDailyInfo] = Field(default_factory=list, alias="stockDailyInfos")


class BatchCreateStockDailyInfosResponse(BaseModel):
    stock_daily_infos: list[StockDailyInfo] = Field(default_factory=list, alias="stockDailyInfos")


class BatchUpdateStockDailyInfo(BaseModel):
    stock_symbol_full: Optional[str] = None
    trade_date: Optional[datetime] = None
    open_price: Optional[int] = None
    close_price: Optional[int] = None
    high_price: Optional[int] = None
    low_price: Optional[int] = None
    volume: Optional[int] = None
    turnover: Optional[int] = None
    change_amount: Optional[int] = None
    change_rate: Optional[int] = None
    pe_ratio: Optional[int] = None
    pb_ratio: Optional[int] = None
    market_cap: Optional[int] = None
    circulating_market_cap: Optional[int] = None
    turnover_rate: Optional[int] = None
    bid_price1: Optional[int] = None
    bid_price2: Optional[int] = None
    bid_price3: Optional[int] = None
    bid_price4: Optional[int] = None
    bid_price5: Optional[int] = None
    bid_volume1: Optional[int] = None
    bid_volume2: Optional[int] = None
    bid_volume3: Optional[int] = None
    bid_volume4: Optional[int] = None
    bid_volume5: Optional[int] = None
    ask_price1: Optional[int] = None
    ask_price2: Optional[int] = None
    ask_price3: Optional[int] = None
    ask_price4: Optional[int] = None
    ask_price5: Optional[int] = None
    ask_volume1: Optional[int] = None
    ask_volume2: Optional[int] = None
    ask_volume3: Optional[int] = None
    ask_volume4: Optional[int] = None
    ask_volume5: Optional[int] = None
    updated_at: Optional[datetime] = None


class BatchUpdateStockDailyInfosRequest(BaseModel):
    ids: list[int]
    stock_daily_info: BatchUpdateStockDailyInfo = Field(alias="stockDailyInfo")


class BatchPatchStockDailyInfosRequest(BaseModel):
    stock_daily_infos: list[UpdateStockDailyInfo] = Field(default_factory=list, alias="stockDailyInfos")


class BatchUpdateStockDailyInfosResponse(BaseModel):
     stock_daily_infos: list[StockDailyInfo] = Field(default_factory=list, alias="stockDailyInfos")


class BatchDeleteStockDailyInfosRequest(BaseModel):
    ids: list[int]


class ExportStockDailyInfo(StockDailyInfo):
    pass


class ExportStockDailyInfosRequest(BaseModel):
    ids: list[int]


class ImportStockDailyInfosRequest(BaseModel):
    file: UploadFile


class ImportStockDailyInfo(CreateStockDailyInfo):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportStockDailyInfosResponse(BaseModel):
    stock_daily_infos: list[ImportStockDailyInfo] = Field(default_factory=list, alias="stockDailyInfos")