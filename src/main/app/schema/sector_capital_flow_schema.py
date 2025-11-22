# SPDX-License-Identifier: MIT
"""SectorCapitalFlow schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from fastlib.request import ListRequest


class ListSectorCapitalFlowsRequest(ListRequest):
    id: Optional[int] = None
    trade_date: Optional[datetime] = None
    sector_code: Optional[str] = None
    sector_name: Optional[str] = None
    sector_type: Optional[int] = None
    main_inflow: Optional[int] = None
    main_outflow: Optional[int] = None
    main_net: Optional[int] = None
    total_inflow: Optional[int] = None
    total_outflow: Optional[int] = None
    total_net: Optional[int] = None
    stock_count: Optional[int] = None
    rise_count: Optional[int] = None
    fall_count: Optional[int] = None
    flat_count: Optional[int] = None
    sector_index: Optional[int] = None
    change_percent: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SectorCapitalFlow(BaseModel):
    id: int
    trade_date: Optional[datetime] = None
    sector_code: Optional[str] = None
    sector_name: Optional[str] = None
    sector_type: Optional[int] = None
    main_inflow: Optional[int] = '0'
    main_outflow: Optional[int] = '0'
    main_net: Optional[int] = '0'
    total_inflow: Optional[int] = '0'
    total_outflow: Optional[int] = '0'
    total_net: Optional[int] = '0'
    stock_count: Optional[int] = '0'
    rise_count: Optional[int] = '0'
    fall_count: Optional[int] = '0'
    flat_count: Optional[int] = '0'
    sector_index: Optional[int] = '0'
    change_percent: Optional[int] = '0'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SectorCapitalFlowDetail(BaseModel):
    id: int
    trade_date: Optional[datetime] = None
    sector_code: Optional[str] = None
    sector_name: Optional[str] = None
    sector_type: Optional[int] = None
    main_inflow: Optional[int] = '0'
    main_outflow: Optional[int] = '0'
    main_net: Optional[int] = '0'
    total_inflow: Optional[int] = '0'
    total_outflow: Optional[int] = '0'
    total_net: Optional[int] = '0'
    stock_count: Optional[int] = '0'
    rise_count: Optional[int] = '0'
    fall_count: Optional[int] = '0'
    flat_count: Optional[int] = '0'
    sector_index: Optional[int] = '0'
    change_percent: Optional[int] = '0'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreateSectorCapitalFlow(BaseModel):
    trade_date: Optional[datetime] = None
    sector_code: Optional[str] = None
    sector_name: Optional[str] = None
    sector_type: Optional[int] = None
    main_inflow: Optional[int] = '0'
    main_outflow: Optional[int] = '0'
    main_net: Optional[int] = '0'
    total_inflow: Optional[int] = '0'
    total_outflow: Optional[int] = '0'
    total_net: Optional[int] = '0'
    stock_count: Optional[int] = '0'
    rise_count: Optional[int] = '0'
    fall_count: Optional[int] = '0'
    flat_count: Optional[int] = '0'
    sector_index: Optional[int] = '0'
    change_percent: Optional[int] = '0'
    updated_at: Optional[datetime] = None


class CreateSectorCapitalFlowRequest(BaseModel):
    sector_capital_flow: CreateSectorCapitalFlow = Field(alias="sectorCapitalFlow")


class UpdateSectorCapitalFlow(BaseModel):
    id: int
    trade_date: Optional[datetime] = None
    sector_code: Optional[str] = None
    sector_name: Optional[str] = None
    sector_type: Optional[int] = None
    main_inflow: Optional[int] = '0'
    main_outflow: Optional[int] = '0'
    main_net: Optional[int] = '0'
    total_inflow: Optional[int] = '0'
    total_outflow: Optional[int] = '0'
    total_net: Optional[int] = '0'
    stock_count: Optional[int] = '0'
    rise_count: Optional[int] = '0'
    fall_count: Optional[int] = '0'
    flat_count: Optional[int] = '0'
    sector_index: Optional[int] = '0'
    change_percent: Optional[int] = '0'
    updated_at: Optional[datetime] = None


class UpdateSectorCapitalFlowRequest(BaseModel):
    sector_capital_flow: UpdateSectorCapitalFlow = Field(alias="sectorCapitalFlow")


class BatchGetSectorCapitalFlowsResponse(BaseModel):
    sector_capital_flows: list[SectorCapitalFlowDetail] = Field(default_factory=list, alias="sectorCapitalFlows")


class BatchCreateSectorCapitalFlowsRequest(BaseModel):
    sector_capital_flows: list[CreateSectorCapitalFlow] = Field(default_factory=list, alias="sectorCapitalFlows")


class BatchCreateSectorCapitalFlowsResponse(BaseModel):
    sector_capital_flows: list[SectorCapitalFlow] = Field(default_factory=list, alias="sectorCapitalFlows")


class BatchUpdateSectorCapitalFlow(BaseModel):
    trade_date: Optional[datetime] = None
    sector_code: Optional[str] = None
    sector_name: Optional[str] = None
    sector_type: Optional[int] = None
    main_inflow: Optional[int] = '0'
    main_outflow: Optional[int] = '0'
    main_net: Optional[int] = '0'
    total_inflow: Optional[int] = '0'
    total_outflow: Optional[int] = '0'
    total_net: Optional[int] = '0'
    stock_count: Optional[int] = '0'
    rise_count: Optional[int] = '0'
    fall_count: Optional[int] = '0'
    flat_count: Optional[int] = '0'
    sector_index: Optional[int] = '0'
    change_percent: Optional[int] = '0'
    updated_at: Optional[datetime] = None


class BatchUpdateSectorCapitalFlowsRequest(BaseModel):
    ids: list[int]
    sector_capital_flow: BatchUpdateSectorCapitalFlow = Field(alias="sectorCapitalFlow")


class BatchPatchSectorCapitalFlowsRequest(BaseModel):
    sector_capital_flows: list[UpdateSectorCapitalFlow] = Field(default_factory=list, alias="sectorCapitalFlows")


class BatchUpdateSectorCapitalFlowsResponse(BaseModel):
     sector_capital_flows: list[SectorCapitalFlow] = Field(default_factory=list, alias="sectorCapitalFlows")


class BatchDeleteSectorCapitalFlowsRequest(BaseModel):
    ids: list[int]


class ExportSectorCapitalFlow(SectorCapitalFlow):
    pass


class ExportSectorCapitalFlowsRequest(BaseModel):
    ids: list[int]


class ImportSectorCapitalFlowsRequest(BaseModel):
    file: UploadFile


class ImportSectorCapitalFlow(CreateSectorCapitalFlow):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportSectorCapitalFlowsResponse(BaseModel):
    sector_capital_flows: list[ImportSectorCapitalFlow] = Field(default_factory=list, alias="sectorCapitalFlows")