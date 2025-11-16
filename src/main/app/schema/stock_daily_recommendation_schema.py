# SPDX-License-Identifier: MIT
"""StockDailyRecommendation schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from fastlib.request import ListRequest


class ListStockDailyRecommendationsRequest(ListRequest):
    id: Optional[int] = None
    stock_symbol_full: Optional[str] = None
    recommend_date: Optional[datetime] = None
    recommend_level: Optional[int] = None
    price: Optional[int] = None
    target_price: Optional[int] = None
    recommend_reason: Optional[str] = None
    analyst: Optional[str] = None
    institution: Optional[str] = None
    risk_level: Optional[str] = None
    validity_period: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StockDailyRecommendation(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    recommend_date: Optional[datetime] = None
    recommend_level: Optional[int] = None
    price: Optional[int] = None
    target_price: Optional[int] = None
    recommend_reason: Optional[str] = None
    analyst: Optional[str] = None
    institution: Optional[str] = None
    risk_level: Optional[str] = None
    validity_period: Optional[int] = None
    created_at: Optional[datetime] = CURRENT_TIMESTAMP
    updated_at: Optional[datetime] = CURRENT_TIMESTAMP


class StockDailyRecommendationDetail(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    recommend_date: Optional[datetime] = None
    recommend_level: Optional[int] = None
    price: Optional[int] = None
    target_price: Optional[int] = None
    recommend_reason: Optional[str] = None
    analyst: Optional[str] = None
    institution: Optional[str] = None
    risk_level: Optional[str] = None
    validity_period: Optional[int] = None
    created_at: Optional[datetime] = CURRENT_TIMESTAMP
    updated_at: Optional[datetime] = CURRENT_TIMESTAMP


class CreateStockDailyRecommendation(BaseModel):
    stock_symbol_full: Optional[str] = None
    recommend_date: Optional[datetime] = None
    recommend_level: Optional[int] = None
    price: Optional[int] = None
    target_price: Optional[int] = None
    recommend_reason: Optional[str] = None
    analyst: Optional[str] = None
    institution: Optional[str] = None
    risk_level: Optional[str] = None
    validity_period: Optional[int] = None
    updated_at: Optional[datetime] = CURRENT_TIMESTAMP


class CreateStockDailyRecommendationRequest(BaseModel):
    stock_daily_recommendation: CreateStockDailyRecommendation = Field(alias="stockDailyRecommendation")


class UpdateStockDailyRecommendation(BaseModel):
    id: int
    stock_symbol_full: Optional[str] = None
    recommend_date: Optional[datetime] = None
    recommend_level: Optional[int] = None
    price: Optional[int] = None
    target_price: Optional[int] = None
    recommend_reason: Optional[str] = None
    analyst: Optional[str] = None
    institution: Optional[str] = None
    risk_level: Optional[str] = None
    validity_period: Optional[int] = None
    updated_at: Optional[datetime] = CURRENT_TIMESTAMP


class UpdateStockDailyRecommendationRequest(BaseModel):
    stock_daily_recommendation: UpdateStockDailyRecommendation = Field(alias="stockDailyRecommendation")


class BatchGetStockDailyRecommendationsResponse(BaseModel):
    stock_daily_recommendations: list[StockDailyRecommendationDetail] = Field(default_factory=list, alias="stockDailyRecommendations")


class BatchCreateStockDailyRecommendationsRequest(BaseModel):
    stock_daily_recommendations: list[CreateStockDailyRecommendation] = Field(default_factory=list, alias="stockDailyRecommendations")


class BatchCreateStockDailyRecommendationsResponse(BaseModel):
    stock_daily_recommendations: list[StockDailyRecommendation] = Field(default_factory=list, alias="stockDailyRecommendations")


class BatchUpdateStockDailyRecommendation(BaseModel):
    stock_symbol_full: Optional[str] = None
    recommend_date: Optional[datetime] = None
    recommend_level: Optional[int] = None
    price: Optional[int] = None
    target_price: Optional[int] = None
    recommend_reason: Optional[str] = None
    analyst: Optional[str] = None
    institution: Optional[str] = None
    risk_level: Optional[str] = None
    validity_period: Optional[int] = None
    updated_at: Optional[datetime] = CURRENT_TIMESTAMP


class BatchUpdateStockDailyRecommendationsRequest(BaseModel):
    ids: list[int]
    stock_daily_recommendation: BatchUpdateStockDailyRecommendation = Field(alias="stockDailyRecommendation")


class BatchPatchStockDailyRecommendationsRequest(BaseModel):
    stock_daily_recommendations: list[UpdateStockDailyRecommendation] = Field(default_factory=list, alias="stockDailyRecommendations")


class BatchUpdateStockDailyRecommendationsResponse(BaseModel):
     stock_daily_recommendations: list[StockDailyRecommendation] = Field(default_factory=list, alias="stockDailyRecommendations")


class BatchDeleteStockDailyRecommendationsRequest(BaseModel):
    ids: list[int]


class ExportStockDailyRecommendation(StockDailyRecommendation):
    pass


class ExportStockDailyRecommendationsRequest(BaseModel):
    ids: list[int]


class ImportStockDailyRecommendationsRequest(BaseModel):
    file: UploadFile


class ImportStockDailyRecommendation(CreateStockDailyRecommendation):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportStockDailyRecommendationsResponse(BaseModel):
    stock_daily_recommendations: list[ImportStockDailyRecommendation] = Field(default_factory=list, alias="stockDailyRecommendations")