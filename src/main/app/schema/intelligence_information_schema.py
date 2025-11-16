# SPDX-License-Identifier: MIT
"""IntelligenceInformation schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from fastlib.request import ListRequest


class ListIntelligenceInformationRequest(ListRequest):
    id: Optional[int] = None
    stock_symbol_full: Optional[str] = None
    news_title: Optional[str] = None
    news_content: Optional[str] = None
    news_source: Optional[str] = None
    publish_time: Optional[datetime] = None
    news_url: Optional[str] = None
    impact_direction: Optional[int] = None
    impact_level: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class IntelligenceInformation(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    news_title: Optional[str] = None
    news_content: Optional[str] = None
    news_source: Optional[str] = None
    publish_time: Optional[datetime] = None
    news_url: Optional[str] = None
    impact_direction: Optional[int] = None
    impact_level: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class IntelligenceInformationDetail(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    news_title: Optional[str] = None
    news_content: Optional[str] = None
    news_source: Optional[str] = None
    publish_time: Optional[datetime] = None
    news_url: Optional[str] = None
    impact_direction: Optional[int] = None
    impact_level: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreateIntelligenceInformation(BaseModel):
    stock_symbol_full: Optional[str] = None
    news_title: Optional[str] = None
    news_content: Optional[str] = None
    news_source: Optional[str] = None
    publish_time: Optional[datetime] = None
    news_url: Optional[str] = None
    impact_direction: Optional[int] = None
    impact_level: Optional[int] = None
    updated_at: Optional[datetime] = None


class CreateIntelligenceInformationRequest(BaseModel):
    intelligence_information: CreateIntelligenceInformation = Field(alias="intelligenceInformation")


class UpdateIntelligenceInformation(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    news_title: Optional[str] = None
    news_content: Optional[str] = None
    news_source: Optional[str] = None
    publish_time: Optional[datetime] = None
    news_url: Optional[str] = None
    impact_direction: Optional[int] = None
    impact_level: Optional[int] = None
    updated_at: Optional[datetime] = None


class UpdateIntelligenceInformationRequest(BaseModel):
    intelligence_information: UpdateIntelligenceInformation = Field(alias="intelligenceInformation")


class BatchGetIntelligenceInformationResponse(BaseModel):
    intelligence_information: list[IntelligenceInformationDetail] = Field(default_factory=list, alias="intelligenceInformation")


class BatchCreateIntelligenceInformationRequest(BaseModel):
    intelligence_information: list[CreateIntelligenceInformation] = Field(default_factory=list, alias="intelligenceInformation")


class BatchCreateIntelligenceInformationResponse(BaseModel):
    intelligence_information: list[IntelligenceInformation] = Field(default_factory=list, alias="intelligenceInformation")


class BatchUpdateIntelligenceInformation(BaseModel):
    stock_symbol_full: Optional[str] = None
    news_title: Optional[str] = None
    news_content: Optional[str] = None
    news_source: Optional[str] = None
    publish_time: Optional[datetime] = None
    news_url: Optional[str] = None
    impact_direction: Optional[int] = None
    impact_level: Optional[int] = None
    updated_at: Optional[datetime] = None


class BatchUpdateIntelligenceInformationRequest(BaseModel):
    ids: list[int]
    intelligence_information: BatchUpdateIntelligenceInformation = Field(alias="intelligenceInformation")


class BatchPatchIntelligenceInformationRequest(BaseModel):
    intelligence_information: list[UpdateIntelligenceInformation] = Field(default_factory=list, alias="intelligenceInformation")


class BatchUpdateIntelligenceInformationResponse(BaseModel):
     intelligence_information: list[IntelligenceInformation] = Field(default_factory=list, alias="intelligenceInformation")


class BatchDeleteIntelligenceInformationRequest(BaseModel):
    ids: list[int]


class ExportIntelligenceInformation(IntelligenceInformation):
    pass


class ExportIntelligenceInformationRequest(BaseModel):
    ids: list[int]


class ImportIntelligenceInformationRequest(BaseModel):
    file: UploadFile


class ImportIntelligenceInformation(CreateIntelligenceInformation):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportIntelligenceInformationResponse(BaseModel):
    intelligence_information: list[ImportIntelligenceInformation] = Field(default_factory=list, alias="intelligenceInformation")