# SPDX-License-Identifier: MIT
"""Stock schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from fastlib.request import ListRequest


class ListStocksRequest(ListRequest):
    id: Optional[int] = None
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    company_name: Optional[str] = None
    english_name: Optional[str] = None
    former_name: Optional[str] = None
    market_type: Optional[str] = None
    legal_representative: Optional[str] = None
    registered_capital: Optional[str] = None
    establish_date: Optional[datetime] = None
    website: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    fax: Optional[str] = None
    registered_address: Optional[str] = None
    business_address: Optional[str] = None
    postal_code: Optional[str] = None
    main_business: Optional[str] = None
    business_scope: Optional[str] = None
    company_profile: Optional[str] = None
    data_source: Optional[str] = None


class Stock(BaseModel):
    id: int
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    company_name: Optional[str] = None
    english_name: Optional[str] = None
    former_name: Optional[str] = None
    market_type: Optional[str] = None
    legal_representative: Optional[str] = None
    registered_capital: Optional[str] = None
    establish_date: Optional[datetime] = None
    website: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    fax: Optional[str] = None
    registered_address: Optional[str] = None
    business_address: Optional[str] = None
    postal_code: Optional[str] = None
    main_business: Optional[str] = None
    business_scope: Optional[str] = None
    company_profile: Optional[str] = None
    data_source: Optional[str] = None


class StockDetail(BaseModel):
    id: int
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    company_name: Optional[str] = None
    english_name: Optional[str] = None
    former_name: Optional[str] = None
    market_type: Optional[str] = None
    legal_representative: Optional[str] = None
    registered_capital: Optional[str] = None
    establish_date: Optional[datetime] = None
    website: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    fax: Optional[str] = None
    registered_address: Optional[str] = None
    business_address: Optional[str] = None
    postal_code: Optional[str] = None
    main_business: Optional[str] = None
    business_scope: Optional[str] = None
    company_profile: Optional[str] = None
    data_source: Optional[str] = None


class CreateStock(BaseModel):
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    company_name: Optional[str] = None
    english_name: Optional[str] = None
    former_name: Optional[str] = None
    market_type: Optional[str] = None
    legal_representative: Optional[str] = None
    registered_capital: Optional[str] = None
    establish_date: Optional[datetime] = None
    website: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    fax: Optional[str] = None
    registered_address: Optional[str] = None
    business_address: Optional[str] = None
    postal_code: Optional[str] = None
    main_business: Optional[str] = None
    business_scope: Optional[str] = None
    company_profile: Optional[str] = None
    data_source: Optional[str] = None


class CreateStockRequest(BaseModel):
    stock: CreateStock = Field(alias="stock")


class UpdateStock(BaseModel):
    id: int
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    company_name: Optional[str] = None
    english_name: Optional[str] = None
    former_name: Optional[str] = None
    market_type: Optional[str] = None
    legal_representative: Optional[str] = None
    registered_capital: Optional[str] = None
    establish_date: Optional[datetime] = None
    website: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    fax: Optional[str] = None
    registered_address: Optional[str] = None
    business_address: Optional[str] = None
    postal_code: Optional[str] = None
    main_business: Optional[str] = None
    business_scope: Optional[str] = None
    company_profile: Optional[str] = None
    data_source: Optional[str] = None


class UpdateStockRequest(BaseModel):
    stock: UpdateStock = Field(alias="stock")


class BatchGetStocksResponse(BaseModel):
    stocks: list[StockDetail] = Field(default_factory=list, alias="stocks")


class BatchCreateStocksRequest(BaseModel):
    stocks: list[CreateStock] = Field(default_factory=list, alias="stocks")


class BatchCreateStocksResponse(BaseModel):
    stocks: list[Stock] = Field(default_factory=list, alias="stocks")


class BatchUpdateStock(BaseModel):
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    exchange: Optional[str] = None
    listing_date: Optional[datetime] = None
    industry: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    company_name: Optional[str] = None
    english_name: Optional[str] = None
    former_name: Optional[str] = None
    market_type: Optional[str] = None
    legal_representative: Optional[str] = None
    registered_capital: Optional[str] = None
    establish_date: Optional[datetime] = None
    website: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    fax: Optional[str] = None
    registered_address: Optional[str] = None
    business_address: Optional[str] = None
    postal_code: Optional[str] = None
    main_business: Optional[str] = None
    business_scope: Optional[str] = None
    company_profile: Optional[str] = None
    data_source: Optional[str] = None


class BatchUpdateStocksRequest(BaseModel):
    ids: list[int]
    stock: BatchUpdateStock = Field(alias="stock")


class BatchPatchStocksRequest(BaseModel):
    stocks: list[UpdateStock] = Field(default_factory=list, alias="stocks")


class BatchUpdateStocksResponse(BaseModel):
     stocks: list[Stock] = Field(default_factory=list, alias="stocks")


class BatchDeleteStocksRequest(BaseModel):
    ids: list[int]


class ExportStock(Stock):
    pass


class ExportStocksRequest(BaseModel):
    ids: list[int]


class ImportStocksRequest(BaseModel):
    file: UploadFile


class ImportStock(CreateStock):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportStocksResponse(BaseModel):
    stocks: list[ImportStock] = Field(default_factory=list, alias="stocks")