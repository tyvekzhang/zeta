# SPDX-License-Identifier: MIT
"""BankCapitalInfo schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from fastlib.request import ListRequest


class ListBankCapitalInfosRequest(ListRequest):
    id: Optional[int] = None
    trade_date: Optional[datetime] = None
    bank_code: Optional[str] = None
    bank_name: Optional[str] = None
    bank_type: Optional[int] = None
    total_deposits: Optional[int] = None
    total_loans: Optional[int] = None
    non_performing_loan_ratio: Optional[int] = None
    loan_loss_provision_ratio: Optional[int] = None
    net_interest_margin: Optional[int] = None
    capital_adequacy_ratio: Optional[int] = None
    tier1_capital_ratio: Optional[int] = None
    core_tier1_ratio: Optional[int] = None
    data_source: Optional[int] = None
    data_frequency: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BankCapitalInfo(BaseModel):
    id: int
    trade_date: Optional[datetime] = None
    bank_code: Optional[str] = None
    bank_name: Optional[str] = None
    bank_type: Optional[int] = None
    total_deposits: Optional[int] = '0'
    total_loans: Optional[int] = '0'
    non_performing_loan_ratio: Optional[int] = '0'
    loan_loss_provision_ratio: Optional[int] = '0'
    net_interest_margin: Optional[int] = '0'
    capital_adequacy_ratio: Optional[int] = '0'
    tier1_capital_ratio: Optional[int] = '0'
    core_tier1_ratio: Optional[int] = '0'
    data_source: Optional[int] = '1'
    data_frequency: Optional[int] = '1'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BankCapitalInfoDetail(BaseModel):
    id: int
    trade_date: Optional[datetime] = None
    bank_code: Optional[str] = None
    bank_name: Optional[str] = None
    bank_type: Optional[int] = None
    total_deposits: Optional[int] = '0'
    total_loans: Optional[int] = '0'
    non_performing_loan_ratio: Optional[int] = '0'
    loan_loss_provision_ratio: Optional[int] = '0'
    net_interest_margin: Optional[int] = '0'
    capital_adequacy_ratio: Optional[int] = '0'
    tier1_capital_ratio: Optional[int] = '0'
    core_tier1_ratio: Optional[int] = '0'
    data_source: Optional[int] = '1'
    data_frequency: Optional[int] = '1'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreateBankCapitalInfo(BaseModel):
    trade_date: Optional[datetime] = None
    bank_code: Optional[str] = None
    bank_name: Optional[str] = None
    bank_type: Optional[int] = None
    total_deposits: Optional[int] = '0'
    total_loans: Optional[int] = '0'
    non_performing_loan_ratio: Optional[int] = '0'
    loan_loss_provision_ratio: Optional[int] = '0'
    net_interest_margin: Optional[int] = '0'
    capital_adequacy_ratio: Optional[int] = '0'
    tier1_capital_ratio: Optional[int] = '0'
    core_tier1_ratio: Optional[int] = '0'
    data_source: Optional[int] = '1'
    data_frequency: Optional[int] = '1'
    updated_at: Optional[datetime] = None


class CreateBankCapitalInfoRequest(BaseModel):
    bank_capital_info: CreateBankCapitalInfo = Field(alias="bankCapitalInfo")


class UpdateBankCapitalInfo(BaseModel):
    id: int
    trade_date: Optional[datetime] = None
    bank_code: Optional[str] = None
    bank_name: Optional[str] = None
    bank_type: Optional[int] = None
    total_deposits: Optional[int] = '0'
    total_loans: Optional[int] = '0'
    non_performing_loan_ratio: Optional[int] = '0'
    loan_loss_provision_ratio: Optional[int] = '0'
    net_interest_margin: Optional[int] = '0'
    capital_adequacy_ratio: Optional[int] = '0'
    tier1_capital_ratio: Optional[int] = '0'
    core_tier1_ratio: Optional[int] = '0'
    data_source: Optional[int] = '1'
    data_frequency: Optional[int] = '1'
    updated_at: Optional[datetime] = None


class UpdateBankCapitalInfoRequest(BaseModel):
    bank_capital_info: UpdateBankCapitalInfo = Field(alias="bankCapitalInfo")


class BatchGetBankCapitalInfosResponse(BaseModel):
    bank_capital_infos: list[BankCapitalInfoDetail] = Field(default_factory=list, alias="bankCapitalInfos")


class BatchCreateBankCapitalInfosRequest(BaseModel):
    bank_capital_infos: list[CreateBankCapitalInfo] = Field(default_factory=list, alias="bankCapitalInfos")


class BatchCreateBankCapitalInfosResponse(BaseModel):
    bank_capital_infos: list[BankCapitalInfo] = Field(default_factory=list, alias="bankCapitalInfos")


class BatchUpdateBankCapitalInfo(BaseModel):
    trade_date: Optional[datetime] = None
    bank_code: Optional[str] = None
    bank_name: Optional[str] = None
    bank_type: Optional[int] = None
    total_deposits: Optional[int] = '0'
    total_loans: Optional[int] = '0'
    non_performing_loan_ratio: Optional[int] = '0'
    loan_loss_provision_ratio: Optional[int] = '0'
    net_interest_margin: Optional[int] = '0'
    capital_adequacy_ratio: Optional[int] = '0'
    tier1_capital_ratio: Optional[int] = '0'
    core_tier1_ratio: Optional[int] = '0'
    data_source: Optional[int] = '1'
    data_frequency: Optional[int] = '1'
    updated_at: Optional[datetime] = None


class BatchUpdateBankCapitalInfosRequest(BaseModel):
    ids: list[int]
    bank_capital_info: BatchUpdateBankCapitalInfo = Field(alias="bankCapitalInfo")


class BatchPatchBankCapitalInfosRequest(BaseModel):
    bank_capital_infos: list[UpdateBankCapitalInfo] = Field(default_factory=list, alias="bankCapitalInfos")


class BatchUpdateBankCapitalInfosResponse(BaseModel):
     bank_capital_infos: list[BankCapitalInfo] = Field(default_factory=list, alias="bankCapitalInfos")


class BatchDeleteBankCapitalInfosRequest(BaseModel):
    ids: list[int]


class ExportBankCapitalInfo(BankCapitalInfo):
    pass


class ExportBankCapitalInfosRequest(BaseModel):
    ids: list[int]


class ImportBankCapitalInfosRequest(BaseModel):
    file: UploadFile


class ImportBankCapitalInfo(CreateBankCapitalInfo):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportBankCapitalInfosResponse(BaseModel):
    bank_capital_infos: list[ImportBankCapitalInfo] = Field(default_factory=list, alias="bankCapitalInfos")