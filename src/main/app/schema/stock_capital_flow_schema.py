# SPDX-License-Identifier: MIT
"""StockCapitalFlow schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from fastlib.request import ListRequest


class ListStockCapitalFlowsRequest(ListRequest):
    id: Optional[int] = None
    trade_date: Optional[datetime] = None
    stock_symbol_full: Optional[str] = None
    exchange: Optional[str] = None
    main_inflow: Optional[int] = None
    main_outflow: Optional[int] = None
    main_net: Optional[int] = None
    retail_inflow: Optional[int] = None
    retail_outflow: Optional[int] = None
    retail_net: Optional[int] = None
    total_inflow: Optional[int] = None
    total_outflow: Optional[int] = None
    total_net: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StockCapitalFlow(BaseModel):
    id: int
    trade_date: Optional[datetime] = None
    stock_symbol_full: Optional[str] = None
    exchange: Optional[str] = None
    main_inflow: Optional[int] = '0'
    main_outflow: Optional[int] = '0'
    main_net: Optional[int] = '0'
    retail_inflow: Optional[int] = '0'
    retail_outflow: Optional[int] = '0'
    retail_net: Optional[int] = '0'
    total_inflow: Optional[int] = '0'
    total_outflow: Optional[int] = '0'
    total_net: Optional[int] = '0'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StockCapitalFlowDetail(BaseModel):
    id: int
    trade_date: Optional[datetime] = None
    stock_symbol_full: Optional[str] = None
    exchange: Optional[str] = None
    main_inflow: Optional[int] = '0'
    main_outflow: Optional[int] = '0'
    main_net: Optional[int] = '0'
    retail_inflow: Optional[int] = '0'
    retail_outflow: Optional[int] = '0'
    retail_net: Optional[int] = '0'
    total_inflow: Optional[int] = '0'
    total_outflow: Optional[int] = '0'
    total_net: Optional[int] = '0'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreateStockCapitalFlow(BaseModel):
    trade_date: Optional[datetime] = None
    stock_symbol_full: Optional[str] = None
    exchange: Optional[str] = None
    main_inflow: Optional[int] = '0'
    main_outflow: Optional[int] = '0'
    main_net: Optional[int] = '0'
    retail_inflow: Optional[int] = '0'
    retail_outflow: Optional[int] = '0'
    retail_net: Optional[int] = '0'
    total_inflow: Optional[int] = '0'
    total_outflow: Optional[int] = '0'
    total_net: Optional[int] = '0'
    updated_at: Optional[datetime] = None


class CreateStockCapitalFlowRequest(BaseModel):
    stock_capital_flow: CreateStockCapitalFlow = Field(alias="stockCapitalFlow")


class UpdateStockCapitalFlow(BaseModel):
    id: int
    trade_date: Optional[datetime] = None
    stock_symbol_full: Optional[str] = None
    exchange: Optional[str] = None
    main_inflow: Optional[int] = '0'
    main_outflow: Optional[int] = '0'
    main_net: Optional[int] = '0'
    retail_inflow: Optional[int] = '0'
    retail_outflow: Optional[int] = '0'
    retail_net: Optional[int] = '0'
    total_inflow: Optional[int] = '0'
    total_outflow: Optional[int] = '0'
    total_net: Optional[int] = '0'
    updated_at: Optional[datetime] = None


class UpdateStockCapitalFlowRequest(BaseModel):
    stock_capital_flow: UpdateStockCapitalFlow = Field(alias="stockCapitalFlow")


class BatchGetStockCapitalFlowsResponse(BaseModel):
    stock_capital_flows: list[StockCapitalFlowDetail] = Field(default_factory=list, alias="stockCapitalFlows")


class BatchCreateStockCapitalFlowsRequest(BaseModel):
    stock_capital_flows: list[CreateStockCapitalFlow] = Field(default_factory=list, alias="stockCapitalFlows")


class BatchCreateStockCapitalFlowsResponse(BaseModel):
    stock_capital_flows: list[StockCapitalFlow] = Field(default_factory=list, alias="stockCapitalFlows")


class BatchUpdateStockCapitalFlow(BaseModel):
    trade_date: Optional[datetime] = None
    stock_symbol_full: Optional[str] = None
    exchange: Optional[str] = None
    main_inflow: Optional[int] = '0'
    main_outflow: Optional[int] = '0'
    main_net: Optional[int] = '0'
    retail_inflow: Optional[int] = '0'
    retail_outflow: Optional[int] = '0'
    retail_net: Optional[int] = '0'
    total_inflow: Optional[int] = '0'
    total_outflow: Optional[int] = '0'
    total_net: Optional[int] = '0'
    updated_at: Optional[datetime] = None


class BatchUpdateStockCapitalFlowsRequest(BaseModel):
    ids: list[int]
    stock_capital_flow: BatchUpdateStockCapitalFlow = Field(alias="stockCapitalFlow")


class BatchPatchStockCapitalFlowsRequest(BaseModel):
    stock_capital_flows: list[UpdateStockCapitalFlow] = Field(default_factory=list, alias="stockCapitalFlows")


class BatchUpdateStockCapitalFlowsResponse(BaseModel):
     stock_capital_flows: list[StockCapitalFlow] = Field(default_factory=list, alias="stockCapitalFlows")


class BatchDeleteStockCapitalFlowsRequest(BaseModel):
    ids: list[int]


class ExportStockCapitalFlow(StockCapitalFlow):
    pass


class ExportStockCapitalFlowsRequest(BaseModel):
    ids: list[int]


class ImportStockCapitalFlowsRequest(BaseModel):
    file: UploadFile


class ImportStockCapitalFlow(CreateStockCapitalFlow):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportStockCapitalFlowsResponse(BaseModel):
    stock_capital_flows: list[ImportStockCapitalFlow] = Field(default_factory=list, alias="stockCapitalFlows")